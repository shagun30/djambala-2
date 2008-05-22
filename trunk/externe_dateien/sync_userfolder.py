#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.12.2007  Beginn der Arbeit
"""

import string
import re
import MySQLdb
import time

from dms.settings import *

from dms.queries            import get_all_users

from dms.encode_decode import decode_html

HOST   = DATABASE_HOST
USER   = DATABASE_USER
PASSWD = DATABASE_PASSWORD
DB     = 'user_folder_db'

def _doSqlQuery(cs, query):
  """ SQL-Anfrage durchfuehren """
  cs.execute(query)
  rows = cs.fetchall()
  return rows

def does_exist(cs, username):
  select = "SELECT user FROM pers_tb WHERE user='%s'" % username
  return len(_doSqlQuery(cs, select)) > 0

users = get_all_users()

db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
cs  = db.cursor()
total = 0
n = 0
for u in users:
  username = u.user.username
  total += 1
  if not does_exist(cs, username):
    u.delete()
    print username
    n += 1
cs.close ()
db.close()
print n, total
