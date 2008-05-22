#-*-coding: utf-8 -*-
"""
/dms/eduwebquestitem/views_navigation_left.py

.. enthaelt den View zum Aendern des linken Navigationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  20.09.2007  Beginn der Arbeit
0.02  21.09.2007  Daten werden gespeichert
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_site_url
from dms.queries        import get_min_max_menu_left
from dms.queries        import delete_menuitem_navmenu_left

from dms.utils_navigation        import save_menus_left

from dms.folder.utils   import get_folder_content

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_menu_left_webquest(item_containers, item_container):
  """ .. liefert das Webquest-Menu """
  start_name = u'webquest'
  content = '0 | %s | %s | Webquest | Startseite | %s\n' % \
            (start_name, item_container.get_absolute_url(), 
              '<b><i><span class="red">::</span></i></b>')
  content += '999\n'
  for i in item_containers:
    if i.item.app.name in ['dmsDocument', 'dmsPool']:
      content += '1 | %s | %s | %s\n' % \
                (i.item.name, i.get_absolute_url(), i.item.title)
  return content

# -----------------------------------------------------
def create_new_menu_webquest(item_container):
  item_containers, sections, d_sections = get_folder_content(item_container)
  n_min, n_max = get_min_max_menu_left()
  menu_left_id = 1 + max(abs(n_min), n_max)
  text = get_menu_left_webquest(item_containers, item_container)
  save_menus_left(menu_left_id, text)
  item_container.container.menu_left_id = menu_left_id
  item_container.container.nav_name_left = 'webquest|'
  item_container.container.save()
  for ic in item_containers:
    if ic.item.app.name == 'dmsPool':
      ic.container.menu_left_id = menu_left_id
      ic.container.nav_name_left = _(u'webquest|') + ic.item.name
      ic.container.save()
  return menu_left_id

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def eduwebquestitem_navigation_left(request, item_container):
  """ Eigenschaften des Ordners aendern """
  menu_id = item_container.container.menu_left_id
  delete_menuitem_navmenu_left(menu_id)
  #sub_menu = item_container.container.nav_name_left
  menu_id_new = create_new_menu_webquest(item_container)
  item_container.container.menu_id = menu_id_new
  item_container.container.save()
  return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
