# -*- coding: utf-8 -*-
"""
/dms/newsletter/views_show.py

.. zeigt den Inhalt eines Diskussionsforums an
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.11.2007  Beginn der Arbeit
0.02  04.02.2008  success beim Versand der Newsletter
"""

from urllib             import quote

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from django.template.loader   import get_template
from django.template          import Context

#from django.core.mail         import send_mail
#from django.core.mail         import EmailMultiAlternatives

from dms.queries        import get_folder_filtered_items_date_ordered
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_site_url
from dms.queries        import get_user
from dms.queries        import get_user_by_username
from dms.queries        import get_item_container_by_path_and_name

from dms.settings       import CONTROL_EMAIL

from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_base_vars


from dms.utils          import get_link_by_item_container
from dms.utils_base     import ACL_USERS
from dms.folder.utils   import get_folder_content
from dms.mail           import createhtmlmail

from dms.userfolder.utils import get_all_users

from dms.roles           import UserEditPerms

from dms.newsletter.utils   import get_user_support
from dms.newsletter.utils   import remove_html
from dms.newsletter.utils   import get_recipients
from dms.newsletter.utils   import count_recipients

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_section_view(items, sections, last_modified):
  """ erzeugt die Section-Ansicht der im Newsletter enthaltenen Objekte """
  # Hilfsfunktion fuer newsletter_show und newsletter_send
  tSection = get_template('app/folder/section.html')
  content = ''
  unknown = _(u'Unbekannter Zwischentitel')
  section = '--START--'
  links = []
  comment_counts = get_visible_comment_count_by_item_containers(items)
  for i in items:
    if last_modified < i.last_modified:
      last_modified = i.last_modified
    if section != i.section :
      if section != unknown :
        if section != '--START--' and links != [] :
          cSection = Context ( { 'section': section, 'links': links } )
          content += tSection.render ( cSection)
        if i.section in sections :
          section = i.section
        else :
          section = unknown
        links = []
    if comment_counts[i.item.id]:
      links.append(get_link_by_item_container(i) + ' - %s: %i' % \
                    (_(u'Kommentar(e)'), comment_counts[i.item.id]))
    else:
      links.append(get_link_by_item_container(i))
  if section != '--START--' and links != []:
    cSection = Context ( { 'section': section, 'links': links } )
    content += tSection.render ( cSection)
  return content, last_modified

def newsletter_show(request, item_container):
  """ zeigt den Inhalt eines Newsletters """
  app_name = 'newsletter'
  user_perms = UserEditPerms(request.user.username, request.path)
  if (request.user.is_authenticated() and user_perms.perm_manage):
    manage_site_mode = True
  else:
    manage_site_mode = False
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                  get_user_support(item_container, manage_site_mode), last_modified=last_modified)
  if item_container.item.has_comments:
    vars['comments'] = True
  #assert False
  return render_to_response('app/base_folderish.html', vars)
  
  
def newsletter_select_section(request, item_container):
  """ zeigt eine Liste zur Auswahl der zu versendenden Ausgabe des Newsletters """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main')
  items, sections, d_sections = get_folder_content(item_container)
  sections_not_empty = []
  for sec in sections:
    if len(d_sections[sec])!=0:
        sections_not_empty.append({'unquoted':sec, 'quoted':quote(sec)})
  vars['sections'] = sections_not_empty
  vars['path']     = get_site_url(item_container, 'index.html')
  vars['number_recipients'] = str( count_recipients( item_container))
  return render_to_response('app/newsletter/select_section.html', vars)

def newsletter_send(request, item_container):
  """ Versenden des Newsletters """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main')
  item_containers, sections, d_sections = get_folder_content(item_container)
  my_item_containers = d_sections[request.GET['section']]

  t  = get_template('app/newsletter/mail_header_text.html')
  th = get_template('app/newsletter/mail_header.html')
  c=Context({'header_title' : vars['header_title'],
             'section'      : request.GET['section'],})
  html_text  = th.render(c)
  plain_text = t.render(c)

  t  = get_template('app/newsletter/mail_single_item_text.html')
  th = get_template('app/newsletter/mail_single_item.html')
  for newsitem_container in my_item_containers:
    c=Context({'title'  : newsitem_container.item.title,
               'text'   : newsitem_container.item.text,
               'name'   : newsitem_container.item.string_1,
               'mail'   : newsitem_container.item.string_2,
               'date'   : newsitem_container.get_last_modified(),
               'url_more': newsitem_container.item.url_more,})
    html_text += th.render ( c) + '\n'
    c=Context({'title'  : newsitem_container.item.title,
               'text'   : remove_html(newsitem_container.item.text),
               'name'   : newsitem_container.item.string_1,
               'mail'   : newsitem_container.item.string_2,
               'date'   : newsitem_container.get_last_modified(),
               'url_more': newsitem_container.item.url_more,})
    plain_text += t.render ( c) + '\n'
  my_user = get_user(request.user.username)
  if my_user != None:
    my_name = my_user.get_full_name()
    my_email = my_user.email
  else:
    my_name = ''
    my_email = ''
  t  = get_template('app/newsletter/mail_footer_text.html')
  th = get_template('app/newsletter/mail_footer.html')
  c=Context({'name'    : my_name,
             'mail'    : my_email,
             'infos'   : item_container.get_absolute_url(),})
  html_text  += th.render(c)
  plain_text += t.render(c)
  #
  subject = _(u'[' + vars['header_title'] + '] ' + request.GET['section'])
  from_addr = CONTROL_EMAIL
  
  my_users = get_recipients(item_container)
  import tempfile, os
  from dms.settings       import BULK_EMAIL_PATH
  tempfile.tempdir = BULK_EMAIL_PATH
  try:
    os.mkdir ( tempfile.tempdir)
  except:
    pass
  for usr in my_users:
    u = get_user_by_username(usr.user)
    to_str = 'To: %s\n' % u.email
    from_str = 'From: %s\n' % from_addr
    message = from_str + to_str + createhtmlmail (html_text, plain_text, subject)
    tempNewsletter = tempfile.mktemp()
    import codecs
    f = codecs.open( tempNewsletter, "wb", "utf-8")
    f.write( message)
    f.close()
  app_name = 'newsletter'
  user_perms = UserEditPerms(request.user.username, request.path)
  if (request.user.is_authenticated() and user_perms.perm_manage):
    manage_site_mode = True
  else:
    manage_site_mode = False
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(item_containers, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                  get_user_support(item_container, manage_site_mode), last_modified=last_modified)
  vars['count'] = len(my_users)
  vars['next'] = item_container.get_absolute_url()
  return render_to_response('app/newsletter/success.html', vars)
