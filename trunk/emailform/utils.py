# -*- coding: utf-8 -*-
"""
/dms/emailform/utils.py

.. enthaelt Hilfefunktionen fuer das E-Mail-Formular
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.11.2007  Beginn der Arbeit
"""

import string
import xml.dom.minidom

from django.utils.translation import ugettext as _

# -----------------------------------------------------
def get_form_items(item_container):
  """ liefert eine Liste der Eingabefelder """

  def getText(nodelist):
    """ liefert den Inhalt eines Datenelements """
    rc = ""
    for node in nodelist:
      if node.nodeType in [ node.TEXT_NODE, node.CDATA_SECTION_NODE]:
        rc += node.data
    return rc
    #return convert_line(rc)

  def getItem(rSatz, rName, default=''):
    """ liefert der Inhalt des Datenelements oder <default> """
    try:
      nameObj = rSatz.getElementsByTagName(rName)[0]
      return getText(nameObj.childNodes)
    except:
      return default

  def getListItems(rSatz, rName, default=[]):
    """ liefert eine Liste mit Werten von <rName> bzw. default """
    items = rSatz.getElementsByTagName(rName)
    temp = []
    for i in items :
      temp.append(getText(i.childNodes))
    if temp == []:
      return default
    return temp

  def handle(rDom):
    """ wertet das Formular aus"""
    form_list = []
    saetze = rDom.getElementsByTagName("element")
    for satz in saetze:
      new = {}
      new['name'] = getItem(satz,'name')
      new['form_type'] = getItem(satz,'form_type')
      if new['name'] != '' and new['form_type'] != '':
        new['header'] = getItem(satz,'header', _(u'Unbekannte Überschrift'))
        new['required'] = bool(getItem(satz,'required', 1))
        if new['form_type'] == 'input':
          new['default'] = getItem(satz,'default', '')
          new['maxchars'] = int(getItem(satz,'maxchars', 60))
          new['length'] = int(getItem(satz,'length', 40))
        elif new['form_type'] == 'text':
          new['default'] = getItem(satz,'default', '')
          new['cols'] = int(getItem(satz,'cols', 40))
          new['rows'] = int(getItem(satz,'rows', 10))
        elif new['form_type'] in ['radio', 'checkbox', 'select']:
          new['options'] = getListItems(satz, 'option', [])
          if new['form_type'] == 'radio':
            new['checked'] = getItem(satz,'checked', -1)
          elif new['form_type'] == 'checkbox':
            new['checked'] = getListItems(satz,'checked', [])
          else:
            new['size'] = int(getItem(satz,'size', 4))
            new['multiple'] = bool(getItem(satz, 'multiple', 0))
            new['selected'] = getListItems(satz,'selected', [])
        form_list.append(new)
    return form_list

  content = item_container.item.text_more.replace('<p>', '').replace('</p>', '')
  if content.find('<?xml') < 0:
    content = """<?xml version="1.0" encoding="ISO-8859-15"?>
<!DOCTYPE lieferung SYSTEM "http://www.bildungsserver.de/lieferung/lieferung.dtd">
<formular>""" + content + '</formular>'
  dom = xml.dom.minidom.parseString(content)
  ret = handle(dom)
  dom.unlink()
  return ret