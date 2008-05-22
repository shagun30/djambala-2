#!/usr/bin/python
#-*-coding: utf-8 -*-
#
# Standardm
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.01.2008  Beginn der Arbeit
"""

from dms.models  import DmsItemContainer
from dms.queries import get_min_max_menu_left
from dms.queries        import get_item_container_by_parent_item_id

from dms.projectgroup.utils   import get_menu_left_from_sections
from dms.utils_navigation     import save_menus_left

item_containers = DmsItemContainer.objects.filter(item__app__name='dmsProjectgroup').\
                                           filter(container__menu_left_id=1)

for ic in item_containers:
  print ic.item.name, ic.container.path, ic.container.menu_left_id
  n_min, n_max = get_min_max_menu_left()
  menu_left_id = 1 + max(abs(n_min), n_max)
  ics = get_item_container_by_parent_item_id(ic.item.id)
  folders = []
  for i in ics:
    if i.item.app.is_folderish and not i.item.app.is_userfolder:
      folders.append(i.item.name)
  text = get_menu_left_from_sections(ic, '', ic.container.sections, folders)
  """
  sections = u'Kommunikation\nKooperation\nDokumente\n'
  text = get_menu_left_from_sections(ic, ic.item.name, sections,
                                    ['kommunikation', 'dokumente', 'kooperation'])
  """
  save_menus_left(menu_left_id, text)
  print menu_left_id
  ic.container.menu_left_id = menu_left_id
  ic.container.nav_name_left = 'start|'
  ic.container.save()
