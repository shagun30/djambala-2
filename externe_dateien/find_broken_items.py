#!/usr/bin/python
#-*-coding: utf-8 -*-
#
# Vgl. http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.05.2007  vorlaeufiger Abschluss der Arbeit
0.02  20.10.2007  Optimierung des Speicherverbrauchs
"""

import string
import re
import MySQLdb
import time

from dms.queries        import get_site_url

from dms.models   import DmsItemContainer
from dms.utils    import get_breadcrumb
from dms.queries  import get_eduitem
from dms.queries  import get_item_container_by_id
from dms.queries  import get_item_container_by_id

from dms.settings import *
from dms.encode_decode import decode_html

MAX_PROB_TERM_LENGTH = 64

db_mysql = MySQLdb.connect ( host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWORD, db=DATABASE_NAME )
cs = db_mysql.cursor()

n = 0
error_count = 0
select = "SELECT * FROM dms_dmsitemcontainer"
cs.execute(select)
rows = cs.fetchall()
for row in rows:
  ic_id = row[0]
  ic_container_id = row[1]
  ic_item_id = row[2]
  ic_owner_id = row[3]
  ic_is_deleted = row[4]
  ic_is_browseable = row[9]
  if not ic_is_deleted:
    select = "SELECT * FROM dms_dmsitem WHERE id=%i" % ic_item_id
    try:
      cs.execute(select)
    except:
      print select
    row_item = cs.fetchone()
    select = "SELECT * FROM dms_dmscontainer WHERE id=%i" % ic_container_id
    try:
      cs.execute(select)
    except:
      print select
    row_container = cs.fetchone()
    has_container = (row_container != None)
    has_item = (row_item != None)
    if not (has_container and has_item):
      #print "PROBLEM:", ic_id, has_container, has_item
      if not has_container and not has_item:
        delete = "DELETE FROM dms_dmsitemcontainer WHERE id=%i;" % ic_id
        print delete
      elif has_container:
        delete = "DELETE FROM dms_dmsitemcontainer WHERE id=%i;" % ic_id
        print delete
      else:
        delete = "DELETE FROM dms_dmsitemcontainer WHERE id=%i;" % ic_id
        print delete
        delete = "DELETE FROM dms_dmsitem WHERE id=%i;" % ic_item_id
        print delete
      
      error_count += 1
    n += 1
cs.close()
db_mysql.close()

print 'Fehlerhafte Edu-Objekte', error_count, n
