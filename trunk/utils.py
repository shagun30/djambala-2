#-*-coding: utf-8 -*-
"""
/dms/utils.py

.. enthaelt Hilfefunktionen fuer 
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  16.01.2007  check_name
0.03  20.1.2007   base_site_url
0.04  04.02.2007  bei Vortraegen wird der Titel in der breadcrum angezeigt
0.05  01.03.2007  send_control_email
0.06  17.05.2007  show_link - info=''
0.07  01.06.2007  get_folderish_actions ueberarbeitet
0.08  10.09.2007  add_if_app_available
0.09  02.10.2007  manage_site_mode, manage_domain_mode
0.10  03.10.2007  get_site_actions
0.11  17.10.2007  get_link_by_item_container fuer Redirects in Lernarchiven angepasst
0.12  23.10.2007  get_item_container_data_object_by_id
0.13  31.10.2007  PROJECT_FOLDER
0.14  10.11.2007  is_protected
0.15  19.02.2008  clean_data
0.16  27.02.2008  type(data) == ..
0.17  11.03.2008  unzip
"""

import string
import datetime
import types

from django.utils.safestring  import SafeData, mark_safe, SafeUnicode
from django.utils.translation import ugettext as _

from math               import floor
from datetime           import date

from django.utils.translation import ugettext as _

from django.utils.encoding  import smart_unicode
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_URL
from dms.settings       import MY_DOMAINS

from dms.queries        import get_top_item
from dms.queries        import get_menuitems_navmenu_top
from dms.queries        import get_menuitems_navmenu_left
from dms.queries        import is_file_by_item_container
from dms.queries        import get_prev_parent_item_containers
from dms.queries        import get_next_parent_item_containers
from dms.queries        import get_licenses
from dms.queries        import get_site_url
from dms.queries        import get_base_site_url
from dms.queries        import get_faecher
from dms.queries        import get_schularten
from dms.queries        import is_app_available
from dms.queries        import get_item_container_data_object_by_id

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.text_icons     import *

from dms.file.utils     import get_file_url

# -----------------------------------------------------
# E-Mail-Adressen verschluesseln

# Created by jmeile
# Anpassung an zecom: Hans Rauch, 3.12.2002, 04.01-2006

def encode_email(emailvalue, namevalue=None,rClass=None,info=None):
  #Taken from http://www.happysnax.com.au/testemail.php
  #Original comments:
  '''this function creates the hexadecimal equivalent to 
     "document.write('<a href="mailto:emailaddress">name</a>')"
     ie it effectively encrpts this as far as spam-bots are concerned
     the Javascript to unencrypt it simply changes the hex back into ascii
     then executes the code using the 'eval' statement
     /... and ta da ... you've got a normal mailto address displayed in the browser.
     //Written by Jeff Robson of Cynergic Net Solutions www.cynergic.net jeff.robson@cynergic.net'''
  if emailvalue == '' :
    return namevalue
  if namevalue == None :
    namevalue = emailvalue
  if rClass != None :
    cClass = ' class="' + rClass + '"'
  else :
    cClass = ''
  if info != None :
    cInfo = ' title="' + info + '"'
  else :
    cInfo = ''
  new_text = hex_string ( 'document.write(\'<a' + cClass + ' href=\"mailto:'+emailvalue+'\"' + \
                          cInfo + '>'+namevalue+'</a>\')' )
  return '<script type=\"text/javascript\">eval(unescape(\''+new_text+'\'))</script>'

def hex_string(mystring):
  #Taken from http://www.happysnax.com.au/testemail.php
  '''Written by Jeff Robson of Cynergic Net Solutions www.cynergic.net jeff.robson@cynergic.net'''
  newstring=''
  length=len(mystring)
  for i in range(length):
    newstring=newstring+'%'+tohex(ord(mystring[i]))
  return newstring

def tohex(n):
  #Taken from http://www.happysnax.com.au/testemail.php
  '''Written by Jeff Robson of Cynergic Net Solutions www.cynergic.net jeff.robson@cynergic.net'''
  hs='0123456789ABCDEF'
  return hs[int(floor(n/16))]+hs[n%16]

# -----------------------------------------------------
def get_footer_email(object, use_string_1=False, class_link='navLink'):
  """ liefert Namen und Adresse des Autors """
  if smart_unicode(str(type(object))) == "<class 'dms.models.DmsItem'>":
    item = object
  else:
    item = object.item
  if use_string_1:
    return encode_email(item.string_2, item.string_1, 'navLink')
  else:
    name = item.owner.get_full_name()
    if name == u'Unbekannte Person' and item.string_1 != '':
      return encode_email(item.string_2, item.string_1, class_link)
    else:
      return encode_email(item.owner.email, name, class_link)

def get_author_email(author, email):
  """ liefert Namen und Adresse des Autors """
  return encode_email(email, author, 'nav')

# -----------------------------------------------------
def get_tabbed_form(rFormItems, rFormHelp, rHelpName, rFormData,
                    do_tab=True, tab_cluster={}, valign=True, max_cols=1,
                    show_errors=True, has_tabs=True, top_of_form=''):
  """ baut Tabbed-Formulare zusammen: Quelle ??? """
  from dms.form_system        import form_system
  from django.template.loader import get_template
  from django.template        import Context

  if has_tabs:
    t = get_template('utils/yui_tab_base.html')
  else:
    t = get_template('utils/yui_tab_base_no_tabs.html')
  content = ''
  headers = []
  tabs = []
  tab_id = 'tab_'
  tab_no = 0
  for item in rFormItems:
    this_tab_id = tab_id + str(tab_no)
    tab_no += 1
    if has_tabs:
      headers.append ( {'tab_id': this_tab_id, 
                        'text': rFormHelp[item[0]]['title'],
                        'selected': tab_no == 1
                        } )
    tabs.append ( {'tab_id': this_tab_id,
                   'info': rFormHelp[item[0]]['info'],
                   'content': form_system().get_form(item[1], rFormHelp,
                                   rHelpName, rFormData,
                                   tab_cluster, valign, max_cols, show_errors)
                  } )
    c = Context ( {'top_of_form': top_of_form, 'headers': headers, 'tabs': tabs } )
  return t.render(c)

# -----------------------------------------------------
def info_slot_to_header(text) :
  """ wandelt rechten Infoslot in HTML fuer WYSIWYG-Editor um """
  HEADER_START = '<!-- header start -->'
  HEADER_END   = '<!-- header end -->'
  INFO_START   = '<!-- info start -->'
  INFO_END     = '<!-- info end -->'
  ret = ''
  nStart = 0
  nHStart = string.find(text, HEADER_START, nStart)
  while nHStart >= 0 :
    nHEnd = string.find ( text, HEADER_END, nHStart )
    header  = text[nHStart+len(HEADER_START):nHEnd]
    nIStart = string.find ( text, INFO_START, nHEnd )
    nIEnd   = string.find ( text, INFO_END, nIStart )
    info    = text[nIStart+len(INFO_START):nIEnd]
    if header == '':
      ret += '<h4>&nbsp;</h4>\n'
    else:
      ret += '<h4>'+header+'</h4>\n'
    ret += info + '\n'
    nHStart = string.find(text, HEADER_START, nIEnd)
  return ret

# -----------------------------------------------------
def get_section_choices(sections):
  """ wandelt Textzeilen in Liste um """
  ret = []
  if sections == None:
    return ret
  sections = string.splitfields(decode_html(sections), '\n')
  for s in sections :
    s = string.strip(s)
    ret.append((s, s))
  return ret
  #  if s != '':
  #    yield(encode_html(s), s)

# -----------------------------------------------------
def get_parent_section_choices(my_item_container):
  item_container = my_item_container.get_parent()
  return get_section_choices(item_container.container.sections)

# -----------------------------------------------------
def get_license_choices(my_item_container):
  #return get_section_choices(get_licenses())
  ret = []
  licenses = get_licenses()
  for lic in licenses:
    if lic.url != '':
      l = mark_safe(show_link(lic.url, lic.name))
    else:
      l = mark_safe(lic.name)
    ret.append((lic.id, l))
  return ret

# -----------------------------------------------------
def get_fach_choices():
  # --- Liste aller Faecher
  ret = []
  ret.append((-1, '---'))
  faecher = get_faecher()
  for fach in faecher:
    ret.append((fach.id, decode_html(fach.name)))
    #ret.append((decode_html(fach.name), decode_html(fach.name)))
  return ret

# -----------------------------------------------------
def get_schulart_choices():
  # --- Liste aller Faecher
  ret = []
  ret.append((-1, '---'))
  schularten = get_schularten()
  for schulart in schularten:
    ret.append((schulart.id, decode_html(schulart.name)))
  return ret

# -----------------------------------------------------
def check_name(name, is_name_ok):
  """ entfernt Umlaute etc. aus Dateinamen """
  try:
    name = unicode(name, 'utf-8')
  except:
    pass
  name = name[max(string.rfind(name,'/'),
                  string.rfind(name,'\\'),
                  string.rfind(name,':')
                  )+1:]
  name = string.replace(name, u"'", u'_')
  name = string.replace(name, u'ä', u'ae')
  name = string.replace(name, u'ö', u'oe')
  name = string.replace(name, u'ü', u'ue')
  name = string.replace(name, u'Ä', u'Ae')
  name = string.replace(name, u'Ö', u'Oe')
  name = string.replace(name, u'Ü', u'Ue')
  name = string.replace(name, u'ß', u'ss')
  bad_chars  = ' ,;()[]{}*"#%+~!'
  good_chars = '________________'
  TRANSMAP = string.maketrans(bad_chars, good_chars)
  name = name.encode('iso-8859-1')
  name = string.translate(name, TRANSMAP)
  if is_name_ok:
    return name
  html = '.html'
  if name[-5:] != html :
    name += html
  return name

# -----------------------------------------------------
def show_link(url, info='', url_extern=False, url_class='', title=''):
  """ zeigt Verweise an - externe Verweise werden optisch gekennzeichnet """
  if info == '':
    if url.startswith('http://'):
      info += url[7:]
    else:
      info = url
  from dms.settings import MY_DOMAINS
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('utils/show_link.html')
  target = ''
  start  = ''
  is_my_domain = False
  # --- Parameter in URL ausschliessen
  n_pos = url.find('?')
  if n_pos > -1:
    u = url[:n_pos]
  else:
    u = url
  if u.startswith('http://'):
    for domain in MY_DOMAINS:
      if u.find(domain) >= 0 :
        is_my_domain = True
        break
    if is_my_domain :
      if url_extern :
        target = '_extern'
        start  = NEW_WINDOW_ICON
    else :
      target = '_extern'
      start  = EXTERN_ICON
  else :
    # Javascript - das Oeffnen in einem eigenen Fenster erfolgt ueber Javascript
    #target = '_extern'
    start  = NEW_WINDOW_ICON
  if url_class != '' and not url_class.startswith('class='):
    url_class = u' class="%s"' % url_class
  if title != '' and not title.startswith('title='):
    title = u' title="%s"' % title
  c = Context ( {'start': start, 'url' : url, 'class': url_class, 
                 'target': target, 'info': info, 'title': title } )
  return t.render(c)

# -----------------------------------------------------
def get_link_by_item_container(item_container, is_folder=False, folder_is_protected=False):
  """ liefert die entsprechende URL """
  d_extern = ''
  d_info = ''
  d_title = item_container.item.title
  if item_container.item.app.is_folderish or is_folder:
    #d_class = 'class="folderLink" '
    postfix = FOLDER_ICON
  else :
    #d_class = ''
    postfix = ''
  # --- handelt es sich um ein Datei- oder Ordner-Objekt?
  is_file = is_file_by_item_container(item_container)
  is_text = item_container.item.app.name == 'dmsText'
  if string.find(item_container.item.name, '.html') > 0 or is_file or is_text:
    if item_container.item.app.name == 'dmsRedirect':
      d_url = item_container.item.url_more
      if string.find(item_container.item.url_more, 'http://') >= 0:
        is_my_domain = False
        for domain in MY_DOMAINS:
          if string.find(item_container.item.url_more, domain) >= 0:
            is_my_domain = True
            break
        if is_my_domain:
          if item_container.item.url_more_extern:
            d_extern = '_extern'
            d_extern_icon = NEW_WINDOW_ICON
        else :
          d_extern = '_extern'
          d_extern_icon = EXTERN_ICON
    elif is_file:
      if item_container.item.url_more_extern:
        d_extern = '_extern'
        d_extern_icon = NEW_WINDOW_ICON
      d_info = FILE_DETAIL % get_site_url(item_container, item_container.item.name + '/show/')
      d_url = get_file_url(item_container, item_container.container.is_protected())
    else:
      d_url = get_site_url(item_container, item_container.item.name)
  else :
    if item_container.is_data_object:
      d_url = get_site_url(item_container, 'index.html')
    else:
      real_item_container = get_item_container_data_object_by_id(item_container.item.id)
      if real_item_container == None:
        d_url = get_site_url(item_container, 'index.html')
      else:
        d_url = get_site_url(real_item_container[0], 'index.html')
  if d_extern:
    help = _(u'Wird in einem eigenen Fenster geöffnet ...')
    this_link = d_extern_icon + u'<a href="%s" target="d_extern" title="%s">%s</a>' % \
                        (d_url, help, d_title)
  elif item_container.item.app.name == 'dmsRedirect' or not item_container.is_data_object:
    s_info = REDIRECT_ICON + '&nbsp;'
    help = _('Springt zu einer anderen Stelle ...')
    this_link = s_info + u'<a href="%s" title="%s">%s</a>' % (d_url, help, d_title)
  else:
    this_link = u'<a href="%s">%s</a>' % (d_url, d_title)
  # --- geschuetzte Bereiche nur einmal anzeigen
  if not folder_is_protected and item_container.container.is_protected():
    postfix = PROJECT_ICON
  return this_link + d_info + postfix

# -----------------------------------------------------
def show_more ( url, url_extern, info='Mehr ...' ) :
  """ erzeugt einen Verweis fuer "mehr ..." """
  return show_link ( url, info, url_extern )

# -----------------------------------------------------
def get_breadcrumb(item_container, text_only=False, ignore_own_breadcrumb=False):
  """ Navigationszeile zusammenbauen """
  if text_only:
    ret = ''
    length = len(item_container.container.site.base_folder)
    n = 0  # --- Begrenzung der Schachtelungstiefe
    if not item_container.item.app.is_folderish:
      item_container = item_container.get_parent()
    while     item_container != None \
          and (ignore_own_breadcrumb or \
               not item_container.item.app.has_own_breadcrumb) \
          and not item_container.container.is_top_folder \
          and item_container.parent_item_id != -1 \
          and n < 20:
      ret = item_container.container.nav_title + ' | ' + ret
      n += 1
      if n >= 20:
        assert False
      item_container = item_container.get_parent()
    return ret
  else:
    from django.template.loader import get_template
    from django.template import Context
    t = get_template('utils/nav_item.html')
    ret = ''
    length = len(item_container.container.site.base_folder)
    n = 0  # --- Begrenzung der Schachtelungstiefe
    if not item_container.item.app.is_folderish:
      item_container = item_container.get_parent()
    while         item_container != None \
          and (ignore_own_breadcrumb or \
               not item_container.item.app.has_own_breadcrumb) \
          and not item_container.container.is_top_folder \
          and item_container.parent_item_id != -1 \
          and n < 20:
      this_path = item_container.container.path[length:]
      if this_path == '':
        this_path = '/'
      c = Context( {'url'  : item_container.container.site.url + this_path + 'index.html',
                    'title': item_container.item.title,
                    'info' : item_container.container.nav_title,})
      ret = t.render(c) + ret
      n += 1
      if n >= 20:
        assert False
      item_container = item_container.get_parent()
    if item_container != None:
      if item_container.item.app.has_own_breadcrumb :
        c=Context({'url'  : get_site_url(item_container, 'index.html'),
                  'title': item_container.item.title,
                  'info' : item_container.container.nav_title,})
        ret = t.render(c) + ret
        parent_item_container = item_container.get_parent()
        c=Context({'url'  : parent_item_container.get_absolute_url(),
                  'title': _('Zur&uuml;ck zu den normalen Web-Seiten'),
                  'info' : _('Ausgang'),})
      elif item_container.container.is_top_folder:
        c=Context({'url'  : get_site_url(item_container, 'index.html'),
                  'title': item_container.item.title,
                  'info' : item_container.container.nav_title,})
        ret = t.render(c) + ret
        item_container = get_top_item()
        c=Context({'url'  : get_site_url(item_container, 'index.html'),
                  'title': item_container.item.title,
                  'info' : item_container.container.nav_title,})
      else:
        c=Context({'url'  : get_site_url(item_container, 'index.html'),
                  'title': item_container.item.title,
                  'info' : item_container.container.nav_title,})
      ret = t.render(c) + ret
      return ret
    else:
      return 'item_container == None!!!'

# -----------------------------------------------------
def get_prev_next(item_container):
  """ Geschwisterseiten """

  def get_string(line, max_char=30):
    if len(line) < max_char:
      return line
    return line[:max_char] + ' ...'

  items = get_prev_parent_item_containers(item_container)
  p_len = len(items)
  if p_len == 0:
    prev_url  = ''
    prev_info = ''
  else:
    p_item = items[p_len-1].item
    prev_url  = p_item.name
    prev_info = get_string(p_item.title)
  items = get_next_parent_item_containers(item_container)
  if len(items) >0:
    next_url  = items[0].item.name
    next_info = get_string(items[0].item.title)
  else:
    next_url  = ''
    next_info = ''
  return prev_url, prev_info, next_url, next_info

# -----------------------------------------------------
def get_prev_next_line(item_container):
  """ Geschwisterseiten anzeigen """
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('utils/prev_next.html')
  prev_url, prev_info, next_url, next_info = get_prev_next(item_container)
  c = Context({'prev_url'    : prev_url,
               'prev_info'   : prev_info,
               'complete_url': './index.html/show_complete/',
               'next_url'    : next_url,
               'next_info'   : next_info, })
  return t.render(c)

# -----------------------------------------------------
def get_folderish_actions(request, user_perms, item_container, app_name,
                          has_user_folder, dont={}):
  from django.template.loader import get_template
  from django.template import Context
  if not request.user.is_authenticated():
    return ''
  t = get_template('app/manage_options_folderish.html')
  nPos = max ( string.rfind ( request.path, '/add/' ),
               string.rfind ( request.path, '/edit/' ),
               string.rfind ( request.path, '/navigation/' ),
               string.rfind ( request.path, '/navigation_left/' ),
               string.rfind ( request.path, '/navigation_top/' ),
               string.rfind ( request.path, '/manage/' ),
               string.rfind ( request.path, '/manage_browseable/' ),
               string.rfind ( request.path, '/manage_comments/' ),
               string.rfind ( request.path, '/import/' ),
               string.rfind ( request.path, '/export/' ),
               string.rfind ( request.path, '/manage_site/' ),
               string.rfind ( request.path, '/manage_user/' ),
               string.rfind ( request.path, '/sort/' ),
               string.rfind ( request.path, '/empty_folders/' ),
               string.rfind ( request.path, '/find_items/' ),
             )
  if nPos > -1 or dont != {}:
    path = request.path[:nPos]
    show_mode       =  not dont.has_key('show_mode') and user_perms.perm_read
    add_mode        = not dont.has_key('add_mode') and \
                      user_perms.perm_add and item_container.item.has_user_support
    edit_mode       = not dont.has_key('edit_mode') and \
                      user_perms.perm_edit
    # --- Stimmen diese Rechte bei ..own..??
    manage_mode     = not dont.has_key('manage_mode') and \
                      ( user_perms.perm_manage or user_perms.perm_edit_own \
                        or user_perms.perm_manage_own )
    import_mode     = not dont.has_key('import_mode') and \
                      user_perms.perm_manage_folderish
    export_mode     = not dont.has_key('export_mode') and \
                      user_perms.perm_manage_folderish
    browseable_mode = not dont.has_key('browseable_mode') and \
                      user_perms.perm_edit
    comment_mode    = not dont.has_key('comment_mode') and \
                      item_container.item.has_comments and \
                      user_perms.perm_edit
    user_mode       = not dont.has_key('user_mode') and \
                      user_perms.perm_manage_user and has_user_folder
    navigation_mode = not dont.has_key('navigation_mode') and \
                      user_perms.perm_manage_folderish
    navigation_top_mode  = not dont.has_key('navigation_top_mode') and \
                      user_perms.perm_manage_site and \
                      (item_container.container.id == 1 or item_container.container.is_top_folder)
    navigation_left_mode = not dont.has_key('navigation_left_mode') and \
                      user_perms.perm_manage_site and \
                      ( item_container.container.id == 1 or \
                        item_container.item.app.name == 'dmsEduWebquestItem' or \
                        item_container.item.app.name == 'dmsProjectgroup')
    sort_mode       = not dont.has_key('sort_mode') and \
                      user_perms.perm_manage
    empty_mode      = not dont.has_key('empty_mode') and \
                      user_perms.perm_manage
    search_mode     = not dont.has_key('search_mode') and \
                      user_perms.perm_add
  else :
    path = request.path
    show_mode        = False
    add_mode         = False
    edit_mode        = False
    manage_mode      = True
    import_mode      = False
    export_mode      = False
    browseable_mode  = False
    comment_mode     = False
    user_mode        = False
    navigation_mode  = False
    navigation_top_mode  = False
    navigation_left_mode = False
    sort_mode        = False
    empty_mode       = False
    search_mode      = False

  if string.find ( path, 'index.html' ) < 0 :
    path += 'index.html'
  if ( string.find(request.path, '/add/') >= 0 ) :
    edit_mode = False
    import_mode = False
    export_mode = False
    browseable_mode = False
    comment_mode = False
    user_mode = False
    navigation_mode = False
    navigation_left_mode = False
    sort_mode = False
    empty_mode = False
    search_mode = False
  elif ( string.find(request.path, '/edit/') >= 0 ) :
    edit_mode = False
    user_mode = False
  elif ( string.find(request.path, '/manage/') >= 0 ) :
    manage_mode = False
  elif ( string.find(request.path, '/manage_browseable/') >= 0 ) :
    browseable_mode = False
  elif ( string.find(request.path, '/manage_comment/') >= 0 ) :
    import_mode = False
    export_mode = False
    comment_mode = False
    user_mode = False
    navigation_mode = False
    navigation_left_mode = False
    sort_mode = False
  elif ( string.find(request.path, '/sort/') >= 0 ) :
    user_mode = False
    sort_mode = False
  elif ( string.find(request.path, '/empty_folders/') >= 0 ):
    empty_mode = False
  elif ( string.find(request.path, '/navigation/') >= 0 ) :
    user_mode = False
    navigation_mode = False
  elif ( string.find(request.path, '/navigation_top/') >= 0 ) :
    user_mode = False
    navigation_top_mode = False
  elif ( string.find(request.path, '/navigation_left/') >= 0 ) :
    user_mode = False
    navigation_left_mode = False
  c = Context( {'authenticated'       : request.user.is_authenticated(),
                'app_name'            : app_name,
                'show_mode'           : show_mode,
                'add_mode'            : add_mode,
                'edit_mode'           : edit_mode,
                'manage_mode'         : manage_mode,
                'import_mode'         : import_mode,
                'export_mode'         : import_mode,
                'browseable_mode'     : browseable_mode,
                'comment_mode'        : comment_mode,
                'navigation_mode'     : navigation_mode,
                'navigation_top_mode' : navigation_top_mode,
                'navigation_left_mode': navigation_left_mode,
                'sort_mode'           : sort_mode,
                'empty_mode'          : empty_mode,
                'search_mode'         : search_mode,
                'user_mode'           : has_user_folder and user_mode,
                'path'                : get_site_url(item_container, 'index.html'),
                'user_path'           : get_site_url(item_container,
                                                     'acl_users/index.html'),
                'user_perms'          : user_perms,
                'user_name'           : request.user,
                'base_site_url'       : get_base_site_url(),
               } )
  return t.render(c).strip()

# -----------------------------------------------------
def get_item_actions(request, user_perms, item_container, app_name, 
                     item_comments, commands={}):
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/manage_options_item.html')
  show_mode = commands.has_key('show_mode')
  edit_mode = commands.has_key('edit_mode')
  rss_mode  = commands.has_key('rss_mode')
  image_mode = commands.has_key('image_mode')
  export_mode = commands.has_key('export_mode')
  if item_comments != None and item_comments != False and request.user.is_authenticated():
    has_comments = ( string.find(request.path, '/manage_comments/') < 0 )
  else:
    has_comments = False
  if string.find(request.path, '/change_owner/') >= 0:
    manage_site_mode = False
  else:
    manage_site_mode = request.user.is_authenticated() \
                       and user_perms.perm_manage
  c = Context ( { 'authenticated'       : request.user.is_authenticated(),
                  'show_mode'           : show_mode,
                  'edit_mode'           : edit_mode,
                  'export_mode'         : export_mode,
                  'rss_mode'            : rss_mode,
                  'manage_comments_mode': has_comments,
                  'image_mode'          : image_mode,
                  'manage_site_mode'    : manage_site_mode,
                  'user_perms'          : user_perms,
                  'user_name'           : request.user,
                  'path'                : get_site_url(item_container,
                                                       item_container.item.name), } )
  return t.render(c).strip()

# -----------------------------------------------------
def get_site_actions(request, user_perms, item_container, dont={}):
  from django.template.loader import get_template
  from django.template import Context
  if not request.user.is_authenticated():
    return ''
  t = get_template('app/manage_options_site.html')
  nPos = max ( string.rfind ( request.path, '/add/' ),
               string.rfind ( request.path, '/edit/' ),
               string.rfind ( request.path, '/navigation/' ),
               string.rfind ( request.path, '/navigation_left/' ),
               string.rfind ( request.path, '/navigation_top/' ),
               string.rfind ( request.path, '/manage/' ),
               string.rfind ( request.path, '/manage_browseable/' ),
               string.rfind ( request.path, '/manage_comments/' ),
               string.rfind ( request.path, '/import/' ),
               string.rfind ( request.path, '/manage_site/' ),
               string.rfind ( request.path, '/manage_user/' ),
               string.rfind ( request.path, '/sort/' ),
             )
  if nPos > -1 :
    path = request.path[:nPos]
    manage_domain_mode = request.user.is_authenticated() \
                       and not dont.has_key('manage_site_mode') \
                       and user_perms.perm_manage_site \
                       and item_container.item.app.name == 'dmsFolder'
    manage_site_mode = request.user.is_authenticated() \
                       and not dont.has_key('manage_site_mode') \
                       and user_perms.perm_manage
  else :
    path = request.path
    manage_domain_mode = False
    manage_site_mode = False

  if string.find ( path, 'index.html' ) < 0 :
    path += 'index.html'
  if ( string.find(request.path, '/manage_site/') >= 0 ) :
    manage_site_mode = False
    user_mode = False
  elif ( string.find(request.path, '/manage_domain/') >= 0 ) :
    manage_domain_mode = False
    user_mode = False
  c = Context( {'authenticated'       : request.user.is_authenticated(),
                'manage_domain_mode'  : manage_domain_mode,
                'manage_site_mode'    : manage_site_mode,
                'path'                : get_site_url(item_container, 'index.html'),
                'user_path'           : get_site_url(item_container,
                                                     'acl_users/index.html'),
                'user_perms'          : user_perms,
                'user_name'           : request.user,
                'base_site_url'       : get_base_site_url(),
               } )
  return t.render(c).strip()

# -----------------------------------------------------
def get_item_actions(request, user_perms, item_container, app_name, 
                     item_comments, commands={}):
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/manage_options_item.html')
  show_mode = commands.has_key('show_mode')
  edit_mode = commands.has_key('edit_mode')
  rss_mode  = commands.has_key('rss_mode')
  image_mode = commands.has_key('image_mode')
  export_mode = commands.has_key('export_mode')
  if item_comments != None and item_comments != False and request.user.is_authenticated():
    has_comments = ( string.find(request.path, '/manage_comments/') < 0 )
  else:
    has_comments = False
  if string.find(request.path, '/change_owner/') >= 0:
    manage_site_mode = False
  else:
    manage_site_mode = request.user.is_authenticated() \
                       and user_perms.perm_manage_site
  c = Context ( { 'authenticated'       : request.user.is_authenticated(),
                  'show_mode'           : show_mode,
                  'edit_mode'           : edit_mode,
                  'export_mode'         : export_mode,
                  'rss_mode'            : rss_mode,
                  'manage_comments_mode': has_comments,
                  'image_mode'          : image_mode,
                  'manage_site_mode'    : manage_site_mode,
                  'user_perms'          : user_perms,
                  'user_name'           : request.user,
                  'path'                : get_site_url(item_container,
                                                       item_container.item.name), } )
  return t.render(c).strip()

# -----------------------------------------------------
def get_item_add_actions(request, user_perms, item_container, commands):
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/manage_options_item.html')
  if commands == {}:
    show_mode = True
    edit_mode = False
    rss_mode  = False
    image_mode = False
    has_comments = False
  else:
    show_mode = commands.has_key('show_mode')
    edit_mode = commands.has_key('edit_mode')
    rss_mode  = commands.has_key('rss_mode')
    image_mode = commands.has_key('image_mode')
    #if item_comments != None and item_comments != False and request.user.is_authenticated():
    #  has_comments = ( string.find(request.path, '/manage_comments/') < 0 )
    #else:
    has_comments = False
  c = Context ( { 'authenticated'       : request.user.is_authenticated(),
                  'show_mode'           : show_mode,
                  'edit_mode'           : edit_mode,
                  'rss_mode'            : rss_mode,
                  'image_mode'          : image_mode,
                  'manage_comments_mode': has_comments,
                  'user_perms'          : user_perms,
                  'user_name'           : request.user,
                  'path'                : get_site_url(item_container, 'index.html'), } )
  return t.render(c).strip()

# -----------------------------------------------------
def get_navigation_left(item_container):
  """ liefert den linken Navigationsbereich """
  items = get_menuitems_navmenu_left(item_container.container.menu_left_id,
                                     item_container.container.nav_name_left)
  if len(items) > 0:
    return items[0].navigation
  else:
    return '<p>%s<br />%i, %s</p>' % \
           (_('Navigation fehlt!'), item_container.container.menu_left_id, 
                                    item_container.container.nav_name_left)

# -----------------------------------------------------
def get_navigation_top(item_container):
  """ liefert den oberen Navigationsbereich """
  items = get_menuitems_navmenu_top(item_container.container.menu_top_id,
                                    item_container.container.nav_name_top)
  if len(items) > 0:
    return items[0].navigation
  else:
    return _('<p>Navigation fehlt!<br />') + '%i, %s' % \
            (item_container.container.menu_top_id, 
             item_container.container.nav_name_top) + '</p>\n'

# -----------------------------------------------------
def get_german_date(d):
  """ d=2003-02-01 10:11:12 -> 01.02.2003 10:11"""
  arr = string.splitfields(d, ' ')
  Y, M, D = string.splitfields(arr[0], '-')
  h, m, s = string.splitfields(arr[1], ':')
  dt = datetime.datetime(int(Y),int(M),int(D),int(h),int(m))
  return dt.strftime('%d.%m.%Y %H:%M')

# -----------------------------------------------------
def remove_link_icons(t):
  """ entfernt Icons, mit denen Verweise (automatisch) gekennzeichnet werden """
  EXTERN_ICON_OLD = u'<span class="red"><strong>»</strong></span> '
  NEW_WINDOW_OLD = u'<span class="red"><strong>··</strong></span> '
  t = t.replace(EXTERN_ICON_OLD + '<a', '<a')
  t = t.replace(EXTERN_ICON + '<a', '<a')
  t = t.replace(NEW_WINDOW_OLD + '<a', '<a')
  t = t.replace(NEW_WINDOW_ICON + '<a', '<a')
  t = t.replace(MAIL_ICON + '<a', '<a')
  t = t.replace('<span class="red"></span>', '')
  return t

# -----------------------------------------------------
def add_if_app_available(item_container, add_on, name, url, info):
  """
  Welche Applikationsobjekte (in der Management-Sicht) duerfen ergaenzt werden?
  Falls die Applikation <name> erlaubt ist, wird ein dictionary mit <url> und
  <info> bei der Liste <add_on> ergaenzt.
  """
  try:
    if is_app_available(name):
      add_on.append( { 'url' : get_site_url(item_container, url), 'info': info, } )
  except:
    pass

# -----------------------------------------------------
def clean_data(data):
  """ Mehrfacheingaben werden in Listen umgewandelt """
  if type(data) == types.DictType:
    return data
  cleaned_data = {}
  keys = data.keys()
  for key in keys:
    this_item = data.getlist(key)
    if len(this_item) == 1:
      cleaned_data[key] = this_item[0]
    else:
      cleaned_data[key] = this_item
  return cleaned_data

import zipfile, os, time, datetime, os.path
from zipfile import *
from os import *
from os.path import *
from time import mktime

# -----------------------------------------------------
def unzip(zip_file, dest_folder):
  """ aus IT/Developer thescripts, crashonyou, 24.02.2007 """
  zip = zipfile.ZipFile(zip_file, 'r')
  if os.path.exists(dest_folder):
    pass
  else:
    os.makedirs(dest_folder)
  if dest_folder[-1] != '/':
    dest_folder += '/'
  for filename in zip.namelist():
    # --- Folder?
    if filename.endswith('/'):
      if os.path.exists(join(abspath(dest_folder),filename)):
        pass
      else:
        os.makedirs(join(abspath(dest_folder),filename))
    else:
      try:
        os.makedirs(normpath((abspath(dest_folder)+'/'+dirname(filename))))
        try:
          bytes = zip.read(filename)
          #print 'Unzipping file:', filename, 'with', len(bytes), 'bytes..'
          file((join(dest_folder,filename)), 'wb').write(zip.read(filename))
          accesstime = time.time()
          timeTuple=(int(zip.getinfo(filename).date_time[0]),\
                      int(zip.getinfo(filename).date_time[1]),\
                      int(zip.getinfo(filename).date_time[2]),\
                      int(zip.getinfo(filename).date_time[3]) ,\
                      int(zip.getinfo(filename).date_time[4]),\
                      int(zip.getinfo(filename).date_time[5]),\
                      int(0),int(0),int(0))
          modifiedtime = mktime(timeTuple)
          utime((join(dest_folder,filename)), (accesstime,modifiedtime))
        except IOError:
          pass
      except:
        if os.path.exists(normpath((abspath(dest_folder)+'/'+dirname(filename)))):
          try:
            bytes = zip.read(filename)
            #print 'Unzipping file:', filename, 'with', len(bytes), 'bytes..'
            file((join(dest_folder,filename)), 'wb').write(zip.read(filename))
            accesstime = time.time()
            timeTuple=(int(zip.getinfo(filename).date_time[0]),\
                        int(zip.getinfo(filename).date_time[1]),\
                        int(zip.getinfo(filename).date_time[2]),\
                        int(zip.getinfo(filename).date_time[3]) ,\
                        int(zip.getinfo(filename).date_time[4]),\
                        int(zip.getinfo(filename).date_time[5]),\
                        int(0),int(0),int(0))
            modifiedtime = mktime(timeTuple)
            utime((join(dest_folder,filename)), (accesstime,modifiedtime))
          except IOError:
              pass
        else:
          os.makedirs(normpath((abspath(dest_folder)+'/'+dirname(filename))))
  zip.close

# -----------------------------------------------------
def get_choices_new_protected():
  """ offener Zugang vs. nur fuer Community-Mitglieder """
  ret = []
  ret.append( (1, _(u'Nur Community-Mitglieder dürfen neue Beiträge leisten')) )
  ret.append( (-1, _(u'Offener Zugang')) )
  return ret

