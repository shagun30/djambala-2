#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2008  Beginn der Arbeit
"""

from dms.survey.models    import DmsSurveyInput
from dms.survey.models    import DmsSurveyText

from dms.settings import *

items = DmsSurveyInput.objects.all()
for item in items:
  value = item.value.strip()
  if value != item.value:
    item.value = value
    item.save()
items = DmsSurveyText.objects.all()
for item in items:
  value = item.value.strip()
  if value != item.value:
    item.value = value
    item.save()
