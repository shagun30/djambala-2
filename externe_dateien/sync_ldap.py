#!/usr/bin/python
#-*-coding: utf-8 -*-
#
"""
Hans Rauch
hans.rauch@gmx.net

Dieses Skript synchronisiert die User in auth mit der LDAP-Datenbank

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.10.2007  Beginn der Arbeit
0.02  03.12.2007  Synchronisation durchfuehren
0.03  05.12.2007  Loeschoperation
"""

import ldap
import re
import time

from dms.settings import *

from dms.queries            import get_all_users
from dms.queries            import get_user
from dms.auth.auth_ldap     import ldap_user_class
from dms.encode_decode      import decode_html


"""
# Vergleich der Performance fuer einfache Abfrage
start = time.time()
community = 'community'
my_ldap = ldap_user_class(LDAP_HOST, LDAP_DN, LDAP_USER, LDAP_PASSWD)
user = my_ldap.get_single_user('h.rauch', ou=community )
print 'LDAP', time.time() - start

start = time.time()
user = get_user('h.rauch')
print 'MySQL', time.time() - start
"""

ou = 'community'
my_ldap = ldap_user_class(LDAP_HOST, LDAP_PORT, LDAP_DN, LDAP_AUTH_USER, LDAP_AUTH_USER_PASSWORD)
users = get_all_users()

# --- ergaenzen auth -> ldap
for user_org in users:
  id = user_org.id
  user = user_org.user
  username = user.username
  sex = user.sex
  title = user.title
  first_name = user.first_name
  last_name = user.last_name
  email = user.email
  password = user.password
  is_active = user.is_active
  is_superuser = user.is_superuser
  last_login = user.last_login
  date_joined = user.date_joined
  org_id = user_org.org_id
  cn = last_name + ', ' + first_name
  uid = username
  pwd = password
  descr = cn
  if not my_ldap.get_single_user(username, ou):
    if not my_ldap.add_user(cn, uid, ou, pwd, descr, org_id, True):
      print uid, cn

ou = 'groups'
users = my_ldap.get_user_list('*', ou)
# --- gegebenenfalls in ldap-groups loeschen
for u in users:
  try:
    user = get_user(u)
  except:
    my_ldap.del_user(u, ou)
    print u

ou = 'community'
users = my_ldap.get_user_list('*', ou)
# --- gegebenenfalls in ldap-community loeschen
for u in users:
  try:
    user = get_user(u)
  except:
    my_ldap.del_user(u, ou)
    print u
