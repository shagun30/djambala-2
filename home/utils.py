# -*- coding: utf-8 -*-
"""
/dms/home/utils.py

.. enthaelt Hilfefunktionen fuer Home-Verzeichnisse
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.04.2008  Beginn der Arbeit
"""

import string

from django.utils.translation import ugettext as _

from dms.utils          import check_name

from dms.queries        import get_site_url
from dms.queries        import get_all_roles
from dms.queries        import get_user_by_username
from dms.queries        import get_min_max_menu_left
from dms.queries        import do_protect_folder
from dms.queries        import save_container_values
from dms.queries        import save_item_values
from dms.queries        import get_role_by_name
from dms.queries        import create_user_url_role
from dms.queries        import get_user_url_role

from dms.queries        import get_quota

from dms.utils_base     import ACL_USERS
from dms.utils_navigation  import save_menus_left

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_role_choices(my_role):
  """ wandelt Textzeilen in Liste um """
  roles = get_all_roles(my_role)
  for r in roles :
    yield ( r.id, u'%s (%s)' % (r.description, r.name) )

# ----------------------------------------------------------------
def get_user_support(item_container, username):
  """ """
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/home/user_support.html')
  user = get_user_by_username(username)
  quota = get_quota(user)
  cSection = Context ({ 'path': get_site_url(item_container, ''),
                        'quota_exceeded': quota.value >= quota.max
                      })
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_menu_left_from_sections(item_container, name, sections, folders):
    url = item_container.get_absolute_url()
    if name != '':
      url = url.replace('index.html', '') + name + '/index.html'
    s_name = 'Start'
    s_info = 'Startseite'
    text = u'0 | %s | %s | %s | %s | <b><i><span class="red">::</span></i></b>\n999\n' % \
           (s_name.lower(), url, s_name, s_info)
    objs = string.splitfields(sections, '\n')
    #assert False
    for obj in objs:
      s_name = obj.strip()
      if s_name in folders:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s%s/index.html | %s\n' % \
                ( s_obj, url.replace('index.html', ''), s_name, s_name)
      elif s_name.lower() in folders:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s%s/index.html | %s\n' % \
                ( s_obj, url.replace('index.html', ''), s_name.lower(), s_name)
      else:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s?section=%s | %s\n' % ( s_obj, url, s_name, s_name)
    return text

# -----------------------------------------------------
#@transaction.commit_manually
def create_home(username, item_container):
  user = get_user_by_username(username)
  new = {}
  """ Home-Verzeichnis anlegen """
  new['name'] = username
  home_str = _(u'Home-Verzeichnis: ')
  new['title'] = '%s%s' % (home_str, user.get_full_name())
  new['min_role_id'] = 40 # manager
  n_min, n_max = get_min_max_menu_left()
  menu_left_id = 1 + max(abs(n_min), n_max)
  new['text'] = '<p>%s %s</p>\n' % (
                _(u'Dieser private Bereich darf ausschließlich im Rahmen pädagogisch-unterrichtlicher'),
                _(u'Fragestellungen genutzt werden!'))
  new['sections'] = _(u'Organisation\nDateien\n')
  text = get_menu_left_from_sections(item_container, username, new['sections'],
                                      ['organisation', 'dateien'])
  save_menus_left(menu_left_id, text)
  new['has_user_support'] = True
  new['is_moderated'] = False
  new['nav_title'] = _(u'Home')
  new['menu_left_id'] = menu_left_id
  new['nav_name_left'] = 'start|'
  new['string_2'] = '/organisation/events/'
  home_item_container = save_container_values(user,
                                      'dmsHome', username, new, item_container)
  home_item_container.is_changeable = False
  home_item_container.is_browseable = False
  home_item_container.save()
  new['text'] = ''
  # --- Dateien
  new['name'] = name = _(u'dateien')
  new['has_user_support'] = True
  new['is_moderated'] = False
  new['title'] = _(u'Dateien')
  new['nav_title'] = _(u'Dateien')
  new['section'] = _(u'Dateien')
  new['sections'] = ''
  new['nav_name_left'] = 'start|dateien'
  mat_item_container = save_container_values(user,
                        'dmsFolderFS', name, new, home_item_container)
  do_protect_folder(home_item_container, mat_item_container, True)
  # --- Termine
  new['name'] = name = _(u'organisation')
  new['has_user_support'] = True
  new['is_moderated'] = False
  new['title'] = _(u'Organisation')
  new['nav_title'] = _(u'Organisation')
  new['section'] = _(u'Organisation')
  new['sections'] = 'Termine\n'
  new['nav_name_left'] = 'start|organisation'
  org_item_container = save_container_values(user,
                       'dmsFolder', name, new, home_item_container)
  new['name'] = name = _(u'events')
  new['title'] = _(u'Terminkalender')
  new['nav_title'] = _(u'Termine')
  new['section'] = _(u'Kooperation')
  new['nav_name_left'] = 'start|organisation'
  item_container = save_container_values(user,
                        'dmsEventBoard', name, new, org_item_container)
  new['name'] = name = _(u'todo')
  new['title'] = _(u'To-Do-Liste')
  new['nav_title'] = _(u'To-Do-Liste')
  new['section'] = _(u'Kooperation')
  new['nav_name_left'] = 'start|organisation'
  item_container = save_container_values(user,
                        'dmsToDoList', name, new, org_item_container)
  # Wert sichern
  new={}
  new['title'] = _(u'User-Verwaltung')
  new['nav_title'] = new['title']
  new['is_browseable'] = False
  new['min_role_id'] = 2000
  acl_item_container = save_container_values(user,
                  'dmsUserFolder', ACL_USERS, new, home_item_container)
  # User eintragen
  items = get_user_url_role(user, home_item_container.container)
  if len(items) == 0:
    create_user_url_role(user, home_item_container.container, get_role_by_name('co_manager'))
  else:
    item = items[0]
    item.role_id = get_role_by_name('co_manager').id
    item.save()

  do_protect_folder(home_item_container, acl_item_container, True)
  #transaction.commit()

