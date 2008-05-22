# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/views_show.py

.. zeigt die Inhalte der Fortbildungsdatenbank an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.02.2008  Beginn der Arbeit
0.02  20.02.2008  gueltig
"""

from django.template.loader import get_template
from django.template    import Context
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.shortcuts   import render_to_response
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.hessen.trainingdb.queries    import get_fach_list
from dms.hessen.trainingdb.queries    import get_gueltig_list
from dms.hessen.trainingdb.queries    import get_schulart_list
from dms.hessen.trainingdb.queries    import get_zielgruppe_list
from dms.hessen.trainingdb.queries    import get_anbieter_list
from dms.hessen.trainingdb.queries    import get_veranstaltung_count
from dms.hessen.trainingdb.queries    import get_veranstaltungen_by_filter
from dms.hessen.trainingdb.queries    import get_schularten_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_zielgruppen_by_veranst_iq_id

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

def has_search_items(data):
  """ wurden Einträge in Formular vorgenommen? """
  has_data = False
  if data == {}:
    return has_data
  has_data = has_data or (data.has_key('training_fach'))
  has_data = has_data or (data.has_key('training_text') and data['training_text']!='')
  has_data = has_data or (data.has_key('training_schulart'))
  has_data = has_data or (data.has_key('training_zielgruppe') and data.has_key('training_zielgruppe'))
  has_data = has_data or (data.has_key('training_iq_nummer') and data['training_iq_nummer']!='')
  has_data = has_data or (data.has_key('training_intern_nummer') and data['training_intern_nummer']!='')
  has_data = has_data or (data.has_key('training_anbieter') and data['training_anbieter']!='')
  return has_data

def get_form_list(items):
  """ """
  ret = []
  for item in items:
    ret.append( (item.CodeKey, item.TextKey) )
  return ret

def get_fach_choices(item_container):
  """ liefert die Liste der moeglichen Faecher """
  ret = []
  ret.append((-1, '---'))
  faecher = get_fach_list(item_container)
  for fach in faecher:
    ret.append((fach.fach_id, fach.fach_name))
  return ret

def get_gueltig_choices():
  """ liefert die Liste der moeglichen Gültigkeitsbereiche """
  ret = []
  ret.append((-1, '---'))
  gueltigs = get_gueltig_list()
  for gueltig in gueltigs:
    ret.append((gueltig.gueltig_id, gueltig.gueltig_name))
  return ret

def get_schulart_choices(item_container):
  """ liefert die Liste der moeglichen Schularten """
  ret = []
  ret.append((-1, '---'))
  schularten = get_schulart_list(item_container)
  for schulart in schularten:
    ret.append((schulart.schulart_id, schulart.schulart_name))
  return ret

def get_zielgruppe_choices(item_container):
  """ liefert die Liste der moeglichen Zielgruppen """
  ret = []
  ret.append((-1, '---'))
  zielgruppen = get_zielgruppe_list(item_container)
  for zielgruppe in zielgruppen:
    ret.append((zielgruppe.zielgruppe_id, zielgruppe.zielgruppe_name))
  return ret

def get_anbieter_choices(item_container):
  """ liefert die Liste der moeglichen Anbieter """
  ret = []
  ret.append((-1, '---'))
  anbieters = get_anbieter_list(item_container)
  for anbieter in anbieters:
    ret.append((anbieter.anbieter_iq_id, anbieter.anbieter_name[:60]))
  return ret

# -----------------------------------------------------
def get_datum(item):
  """ liefert das zusammengesetzte Datum """
  if item[0].veranst_datum_von != None:
    von_datum = item[0].veranst_datum_von.strftime('%d.%m.%Y')
    try:
      bis_datum = item[0].veranst_datum_bis.strftime('%d.%m.%Y')
    except:
      bis_datum = von_datum
    von_zeit = item[0].veranst_datum_von.strftime('%H:%M')
    try:
      bis_zeit = item[0].veranst_datum_bis.strftime('%H:%M')
    except:
      bis_zeit = von_zeit
    datum = von_datum
    if von_zeit != '00:00':
      datum += '/' + von_zeit
    if von_datum != bis_datum:
      datum += ' - ' + bis_datum
      if bis_zeit != '00:00':
        datum += '/' + bis_zeit
    elif von_zeit != bis_zeit and bis_zeit != '00:00':
      datum += '-' + bis_zeit
  else:
    datum = 'Abrufangebot'
  return datum

# -----------------------------------------------------
def get_schularten_str(items):
  ret = ''
  for item in items:
    if ret != '':
      ret += ' &middot; '
    ret += item[1].schulart_name
  return mark_safe(ret)

# -----------------------------------------------------
def get_zielgruppen_str(items):
  ret = ''
  for item in items:
    if ret != '':
      ret += ' &middot; '
    ret += item[1].zielgruppe_name
  return mark_safe(ret)

# -----------------------------------------------------
def get_faecher_str(items):
  ret = ''
  for item in items:
    if ret != '':
      ret += ' &middot; '
    ret += item[1].fach_name
  return mark_safe(ret)

