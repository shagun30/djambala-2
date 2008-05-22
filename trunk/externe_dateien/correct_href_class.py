#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

Dieses Programm korrigiert Fehler, die beim Import von Texten aus dem dem zecom-System
in Djambala auftreten: Externe Verweise erhalten zwei Doppelpfeile und werden knall-rot
angezeigt.

0.01  30.01.2008  Beginn der Arbeit
"""

from django.utils.encoding  import smart_unicode

from dms.models   import DmsItem

from dms.settings import *
from dms.encode_decode import decode_html

start_of_href = u'<span class="red"><strong>»</strong></span> <a'
wrong_tag = u'<span class="extlink">»</SPAN>'
wrong_tag2 = u'<span class="extlink">»</span>'
dummy = u'__AAAA___'
class_old = u'class="extlink" target="_extern"'
class_new = u'target="_extern"'


def do_correct(text):
  if text.find(start_of_href):
    text = text.replace(class_old, class_new)
    text = text.replace(start_of_href, dummy)
    text = text.replace(start_of_href[:-2], '')
    text = text.replace(wrong_tag, '')
    text = text.replace(wrong_tag2, '')
    text = text.replace(dummy, start_of_href)
  return text

items = DmsItem.objects.all()
for item in items:
  do_save = False
  text = do_correct(item.text)
  text_more = do_correct(item.text_more)
  if text != item.text or text_more != item.text_more:
    #print text
    #print text_more
    print item.id
    
    item.text = text
    item.text_more = text_more
    item.save()