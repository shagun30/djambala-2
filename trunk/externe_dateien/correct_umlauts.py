#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.04.2008  Beginn der Arbeit
0.02  23.04.2008  DmsGroup
"""

from dms.auth.models    import User
from dms.models         import DmsGroup
from dms.models         import DmsOrg
from dms.models         import DmsOrgGroup
from dms.encode_decode  import decode_html

from dms.settings import *

orgs = DmsOrg.objects.all()
for org in orgs:
  org_id = org.org_id
  organisation = decode_html(org.organisation)
  sub_organisation = decode_html(org.sub_organisation)
  street = decode_html(org.street)
  town = decode_html(org.town)
  if organisation != org.organisation or \
     sub_organisation != org.sub_organisation or \
     street != org.street or \
     town != org.town:
    org.organisation = organisation
    org.sub_organisation = sub_organisation
    org.street = street
    org.town = town
    org.save()
    print org_id, organisation, sub_organisation, street, town

users = User.objects.all()
for user in users:
  id = user.id
  title = decode_html(user.title)
  first_name = decode_html(user.first_name)
  last_name = decode_html(user.last_name)
  if title != user.title or \
     first_name != user.first_name or \
     last_name != user.last_name:
    user.title = title
    user.first_name = first_name
    user.last_name = last_name
    print id, title, first_name, last_name
    user.save()

groups = DmsGroup.objects.all()
for group in groups:
  id = group.id
  description = decode_html(group.description)
  if description != group.description:
    group.description = description
    print id, group
    group.save()
org_groups = DmsOrgGroup.objects.all()
for org_group in org_groups:
  contains = decode_html(org_group.contains)
  if contains != org_group.contains:
    org_group.contains = contains
    print id, org_group
    org_group.save()