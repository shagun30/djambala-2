#-*-coding: utf-8 -*-
"""
/dms/folderschool/views_navigation_left.py

.. enthaelt den View zum Aendern des linken Navigationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_site_url
from dms.queries        import get_min_max_menu_left
from dms.queries        import delete_menuitem_navmenu_left
from dms.queries        import get_item_container_by_parent_item_id

from dms.utils_navigation        import save_menus_left
from dms.folderschool.utils      import get_menu_left_from_sections

from dms.folder.utils   import get_folder_content

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def folderschool_navigation_left(request, item_container):
  """ linkes Menu aendern aendern """
  ic = get_item_container_by_parent_item_id(item_container.item.id)
  folders = []
  for i in ic:
    if i.item.app.is_folderish and not i.item.app.is_userfolder:
      folders.append(i.item.name)
  text = get_menu_left_from_sections(item_container, '', item_container.container.sections, folders)
  save_menus_left(item_container.container.menu_left_id, text)
  return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
