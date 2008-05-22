#!/usr/bin/python
#-*-coding: utf-8 -*-
#
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.10.2007  Beginn der Arbeit
"""

import string

from dms.queries        import get_site_url

from dms.models   import DmsItemContainer
from dms.settings import *

modified = 0
item_containers = DmsItemContainer.objects.filter(container__path__startswith='/unterricht/lernarchiv/lehrplaene/')
for ic in item_containers:
  if ic.item.is_exchangeable:
    ic.item.is_exchangeable = False
    ic.item.save()
    modified += 1
  if ic.item.image_url == '':
    ic.item.image_url = 'http://download.bildung.hessen.de/unterricht/lernarchiv/logo_thumbs/hessen.gif'
    ic.item.image_url_url = 'http://www.kultusministerium.hessen.de/'
    ic.item.image_extern = True
    ic.item.save()
    
print len(item_containers), modified

item_containers = DmsItemContainer.objects.filter(container__path__contains='/hs/')
for ic in item_containers:
  if ic.item.is_exchangeable:
    ic.item.is_exchangeable = False
    ic.item.save()
    modified += 1

print len(item_containers), modified

item_containers = DmsItemContainer.objects.filter(container__path__contains='/rs/')
for ic in item_containers:
  if ic.item.is_exchangeable:
    ic.item.is_exchangeable = False
    ic.item.save()
    modified += 1

print len(item_containers), modified

item_containers = DmsItemContainer.objects.filter(container__path__contains='/gym/')
for ic in item_containers:
  if ic.item.is_exchangeable:
    ic.item.is_exchangeable = False
    ic.item.save()
    modified += 1

print len(item_containers), modified

item_containers = DmsItemContainer.objects.filter(container__path__contains='/gym_g9/')
for ic in item_containers:
  if ic.item.is_exchangeable:
    ic.item.is_exchangeable = False
    ic.item.save()
    modified += 1

print len(item_containers), modified

