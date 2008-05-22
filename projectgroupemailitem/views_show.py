# -*- coding: utf-8 -*-
"""
/dms/projectgroupemailitem/views_show.py

.. zeigt den Inhalt eines Rundschreibens an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.02.2008  Beginn der Arbeit
0.02  05.02.2008  do_send
"""

import tempfile, os

from django.shortcuts   import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.settings       import BULK_EMAIL_PATH
from dms.settings       import CONTROL_EMAIL
from dms.roles          import require_permission
from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment
from dms.newsletter.utils   import remove_html
from dms.newsletter.utils   import check_userfolder
from dms.userfolder.utils   import get_all_users_with_email
from dms.mail               import createhtmlmail

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage')
def projectgroupemailitem_send(request, item_container, parent):
  """ Rundschreiben versenden """
  t  = get_template('app/newsletter/mail_header_text.html')
  th = get_template('app/newsletter/mail_header.html')
  c=Context({'header_title' : parent.item.title,
             'section'      : item_container.section,})
  html_text  = th.render(c)
  plain_text = t.render(c)

  t  = get_template('app/newsletter/mail_single_item_text.html')
  th = get_template('app/newsletter/mail_single_item.html')
  c=Context({'title'   : item_container.item.title,
              'text'   : item_container.item.text,
              'name'   : item_container.item.string_1,
              'mail'   : item_container.item.string_2,
              'date'   : item_container.get_last_modified(),
              'url_more': item_container.item.url_more,})
  html_text += th.render ( c) + '\n'
  c=Context({'title'  : item_container.item.title,
              'text'   : remove_html(item_container.item.text),
              'name'   : item_container.item.string_1,
              'mail'   : item_container.item.string_2,
              'date'   : item_container.get_last_modified(),
              'url_more': item_container.item.url_more,})
  plain_text += t.render ( c) + '\n'
  t  = get_template('app/newsletter/mail_footer_text.html')
  th = get_template('app/newsletter/mail_footer.html')
  c=Context({'name'    : request.user.get_full_name(),
             'mail'    : request.user.email,
             'infos'   : item_container.get_absolute_url(),})
  html_text  += th.render(c)
  plain_text += t.render(c)

  subject = u'[%s] %s' % (parent.item.title, item_container.section)
  from_addr = CONTROL_EMAIL
  ic = item_container
  while not check_userfolder(ic):
    ic = ic.get_parent()
  users = get_all_users_with_email(ic)
  tempfile.tempdir = BULK_EMAIL_PATH
  try:
    os.mkdir ( tempfile.tempdir)
  except:
    pass
  for user in users:
    to_str = 'To: %s\n' % user.user.email
    from_str = 'From: %s\n' % from_addr
    message = from_str + to_str + createhtmlmail (html_text, plain_text, subject)
    tempNewsletter = tempfile.mktemp()
    import codecs
    f = codecs.open( tempNewsletter, "wb", "utf-8")
    f.write( message)
    f.close()
  app_name = 'projectgroupemailitem'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['count'] = len(users)
  vars['next'] = parent.get_absolute_url()
  return render_to_response('app/newsletter/success.html', vars)

# -----------------------------------------------------
def projectgroupemailitem_show(request,item_container):
  """ zeigt den Inhalt eines Beitrags zum Newsletter """
  app_name = 'projectgroupemailitem'
  parent = item_container.get_parent()
  if request.POST.has_key('do_send') and request.POST['do_send']:
    return projectgroupemailitem_send(request, item_container, parent)
  else:
    if parent.item.has_comments:
      comments = item_comment(request, item_container=item_container)
    else:
      comments = ''
    vars = get_item_vars_show(request, item_container, app_name)
    vars['comments'] = comments
    vars['author']           = item_container.item.owner.username
    vars['author_full_name'] =item_container.item.owner.get_full_name()
    return render_to_response ( 'app/projectgroupemail/show_item.html', vars )
