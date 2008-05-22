#!/usr/bin/python
#-*-coding: utf-8 -*-
#
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.11.2007  Beginn der Arbeit
"""

import string
import re
import time

from dms.settings import *

from dms.models       import DmsItemContainer, DmsItem, DmsApp, DmsContainer
from dms.queries      import mkdir_fs

from dms.encode_decode import decode_html

item_containers = DmsItemContainer.objects.filter(item__app__is_folderish=1)

for item_container in item_containers:
  mkdir_fs(item_container)
  p = item_container.container.path
  print p
