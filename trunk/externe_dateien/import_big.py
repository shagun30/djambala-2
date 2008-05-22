#!/usr/bin/python
#-*-coding: utf-8 -*-
#
# grosse XML-Dateien importieren
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.03.2008  Beginn der Arbeit
"""

import sys

from dms.models           import DmsItemContainer
from dms.queries          import get_item_container_by_path_and_name
from dms.queries          import get_user_by_id

from dms.import_dms.utils import convert_xml_to_sql

base_target = '/medien/%s/'
base_source = '/data/home/hrauch/backup_zecom/medien/%s'

target = 'internes_medien'
source = 'xml_export_internes.xml'

# 1. Import-Pfad
item_container = get_item_container_by_path_and_name(base_target % target, '')
#print item_container.item.name
# 2. Datei oeffnen
f = open(base_source % source, 'r')
content = f.read()
f.close()
# 3. user - 2 = h.rauch
user = get_user_by_id(2)

print "Anfang"
convert_xml_to_sql(user, content, item_container)
print "Ende"
