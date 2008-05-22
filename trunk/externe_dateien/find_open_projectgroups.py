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

0.01  07.04.2008  Beginn der Arbeit
"""

from dms.models  import DmsItemContainer
from dms.models  import DmsContainer

from dms.projectgroup.utils   import get_menu_left_from_sections
from dms.utils_navigation     import save_menus_left

item_containers = DmsItemContainer.objects.filter(item__app__name='dmsProjectgroup').\
                                           filter(container__min_role_id=2000)

for ic in item_containers:
  print ic.item.name, ic.container.path
  containers = DmsContainer.objects.filter(path__startswith=ic.container.path).\
                                    exclude(path__contains='acl_users')
  for c in containers:
    c.min_role_id = 50
    c.save()
