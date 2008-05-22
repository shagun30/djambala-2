#!/usr/bin/python
#-*-coding: utf-8 -*-
#
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.10.2007  Beginn der Arbeit
"""

import string
import re
import MySQLdb
import time

from dms.settings import *

from dms.queries            import get_edu_faecher
from dms.queries            import get_item_by_url_more
from dms.elixier.queries    import get_elixier_data
from dms.elixier.queries    import get_elixier_items
from dms.elixier.queries    import get_elixier_item_status
from dms.elixier.queries    import set_elixier_item_status
from dms.elixier.queries    import set_elixier_item_fach_sachgebiet
from dms.elixier.queries    import append_elixier_item_status
from dms.elixier.queries    import get_elixier_org_by_id_local

from dms.encode_decode import decode_html

faecher = get_edu_faecher()

# --- synchroniere ElixierOrg mit ElixierItem
items = get_elixier_data()
for item in items:
  fach_sachgebiet = -1
  for fach in faecher:
    if item.fach_sachgebiet.find(fach.name) >= 0:
      fach_sachgebiet = fach.id
      break
  if item.url_ressource != '':
    does_exist = (get_item_by_url_more(item.url_ressource) != None)
  else:
    does_exist = False
  item_status = get_elixier_item_status(item.id_local)
  print item.id,
  if item_status == None:
    if does_exist:
      status = 1
    else:
      status = 0
    append_elixier_item_status(item.id_local, status, fach_sachgebiet)
    print '+'
  else:
    set_elixier_item_fach_sachgebiet(item_status, fach_sachgebiet)
    if does_exist:
      set_elixier_item_status(item_status, 1)
    print '.'

print "Kontrolle, ob alle Items in ElixierItem auch in ElixierOrg vorkommen"
print
# --- synchroniere ElixierIten mit ElixierOrg
items = get_elixier_items()
for item in items:
  if get_elixier_org_by_id_local(item.id_local) == None:
    print item.id_local, ' wurde geloescht'
    item.delete()
