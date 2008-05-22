# -*- coding: utf-8 -*-
"""
/dms/edulinkitem/utils.py

.. enthaelt Hilfsfunktionen fuer Verweisese in den Lernarchiven
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.07.2007  Beginn der Arbeit
0.02  30.08.2007  Schlagworte und Faecher
0.04  04.09.2007  get_schlagworte
0.05  07.09.2007  get_description_link
"""

import string

from django.utils.translation import ugettext as _

from dms.queries        import set_extra_data
from dms.queries        import get_extra_data
from dms.queries        import get_lernrestyp_all
from dms.queries        import get_medienformat_all
from dms.queries        import get_schulstufe_all
from dms.queries        import get_schulart_all
from dms.queries        import get_zielgruppe_all
from dms.queries        import get_edu_faecher
from dms.queries        import get_edu_sprachen
from dms.queries        import get_edu_fach_id_by_name
from dms.queries        import get_schulart_id_by_name
from dms.queries        import get_schulstufe_id_by_name
from dms.queries        import get_stemmed
from dms.queries        import delete_stemmed_keyword
from dms.queries        import insert_stemmed_keyword
from dms.utils          import show_link

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

# -----------------------------------------------------
def get_lernrestyp_choices():
  """ liefert die Basis zur Auswahl der Lernressourcen """
  ret = []
  lernrestyp = get_lernrestyp_all()
  for l in lernrestyp:
    ret.append((l.id, decode_html(l.name)))
  return ret

# -----------------------------------------------------
def get_medienformat_choices():
  """ liefert die Basis zur Auswahl des Medienformats """
  ret = []
  medienformat = get_medienformat_all()
  for m in medienformat:
    ret.append((m.id, decode_html(m.name)))
  return ret

# -----------------------------------------------------
def get_schlagworte_by_path(item_container):
  """ extrahiert aus dem Pfad Schlagworte """
  ret_str = ''
  ret = []
  parent_container = item_container.get_parent()
  while parent_container.item.app.name == 'dmsEduFolder':
    ret_str += decode_html(item_container.container.nav_title) + '\n'
    ret.append(item_container.container.nav_title)
    item_container = parent_container
    parent_container = item_container.get_parent()
  return ret_str, ret

# -----------------------------------------------------
def get_fach_list():
  """ liefert die Liste der Faecher """
  ret = []
  faecher = get_edu_faecher()
  for f in faecher:
    ret.append((f.id, decode_html(f.name)))
  return ret

# -----------------------------------------------------
def get_schlagworte_list(itemlist):
  """ extrahiert aus dem Pfad Schlagworte """
  ret = ''
  for s in itemlist:
    ret += s.name + '\n'
  return ret

# -----------------------------------------------------
def get_sprachen_list():
  """ liefert die Liste der moeglichen Sprachen """
  ret = []
  sprachen = get_edu_sprachen()
  for s in sprachen:
    ret.append((s.id, decode_html(s.name)))
  return ret

# -----------------------------------------------------
def get_schularten_list():
  """ liefert die Liste der Schularten/-formen """
  ret = []
  schularten = get_schulart_all()
  for s in schularten:
    ret.append((s.id, decode_html(s.name)))
  return ret

# -----------------------------------------------------
def get_schulstufen_list():
  """ liefert die Liste der Schulstufen """
  ret = []
  schulstufen = get_schulstufe_all()
  for s in schulstufen:
    ret.append((s.id, decode_html(s.name)))
  return ret

# -----------------------------------------------------
def get_zielgruppen_list():
  """ liefert die Liste der Zielgruppen """
  ret = []
  zielgruppen = get_zielgruppe_all()
  for z in zielgruppen:
    ret.append((z.id, decode_html(z.name)))
  return ret

# -----------------------------------------------------
def get_faecher_by_schlagworte(schlagworte):
  """ liefert die in schlagworte enthaltenen Faecher als Liste """
  faecher = []
  for s in schlagworte:
    f_id = get_edu_fach_id_by_name(s)
    if f_id > 0:
      faecher.append(f_id)
  return faecher

# -----------------------------------------------------
def get_schulart_by_schlagworte(schlagworte):
  """ liefert die in <schlagworte> enthaltene Schulart sowie moegliche Schulstufen """
  schularten = []
  schulstufen = []
  for s in schlagworte:
    if s == _(u'Grundschule'):
      schulstufen.append(get_schulstufe_id_by_name(_(u'Primarstufe')))
    elif s == _(u'Sek I'):
      schularten.append(get_schulart_id_by_name(_(u'Hauptschule')))
      schularten.append(get_schulart_id_by_name(_(u'Realschule')))
      schularten.append(get_schulart_id_by_name(_(u'Gymnasium')))
      schulstufen.append(get_schulstufe_id_by_name(_(u'Sekundarstufe I')))
    elif s == _(u'Sek II'):
      schularten.append(get_schulart_id_by_name(_(u'Gymnasium')))
      schulstufen.append(get_schulstufe_id_by_name(_(u'Sekundarstufe II')))
    elif s.find(_(u'Beruf')) >= 0:
      schularten.append(get_schulart_id_by_name(_(u'Beruf')))
      schulstufen.append(get_schulstufe_id_by_name(_(u'Sekundarstufe II')))
  return schularten, schulstufen

# -----------------------------------------------------
def set_extra(lokal_id,
              metadaten_url,
              lern_res_typ,
              autor,
              herausgeber,
              anbieter_herkunft,
              isbn,
              preis,
              titel_lang,
              beschreibung_lang,
              publikations_datum,
              verfalls_datum,
              standards_kmk,
              standards_weitere,
              techn_voraus,
              lernziel,
              lernzeit,
              methodik,
              lehrplan,
              rechte,
              medienformat,
              zertifikat,
              ):
  """ Zusatzdaten speichern """
  return set_extra_data ( lokal_id = lokal_id,
                          metadaten_url = metadaten_url,
                          lern_res_typ = lern_res_typ,
                          autor = autor,
                          herausgeber = herausgeber,
                          anbieter_herkunft = anbieter_herkunft,
                          isbn = isbn,
                          preis = preis,
                          titel_lang = titel_lang,
                          beschreibung_lang = beschreibung_lang,
                          publikations_datum = publikations_datum,
                          verfalls_datum = verfalls_datum,
                          standards_kmk = standards_kmk,
                          standards_weitere = standards_weitere,
                          techn_voraus = techn_voraus,
                          lernziel = lernziel,
                          lernzeit = lernzeit,
                          methodik = methodik,
                          lehrplan = lehrplan,
                          rechte = rechte,
                          medienformat = medienformat,
                          zertifikat = zertifikat
                        )

# -----------------------------------------------------
def get_extra(item_container):
  """ liefert die gepackten Informationen wieder aus """
  data = get_extra_data(item_container)
  return data['lokal_id'], \
         data['metadaten_url'], \
         data['lern_res_typ'], \
         data['autor'], \
         data['herausgeber'], \
         data['anbieter_herkunft'], \
         data['isbn'], \
         data['preis'], \
         data['titel_lang'], \
         data['beschreibung_lang'], \
         data['publikations_datum'], \
         data['verfalls_datum'], \
         data['standards_kmk'], \
         data['standards_weitere'], \
         data['techn_voraus'], \
         data['lernziel'], \
         data['lernzeit'], \
         data['methodik'], \
         data['lehrplan'], \
         data['rechte'], \
         data['medienformat'], \
         data['zertifikat']

# -----------------------------------------------------
def get_schlagworte(new, old):
  """ liefert gestemmte Schlagworte, die ergaenzt bzw. geloescht werden muessen """
  old_list = []
  new_list = []
  old_list_org = []
  new_list_org = []
  if old != None:
    for s in string.splitfields(old, '\n'):
      s = s.strip()
      if s != '':
        s = encode_html(s)
        old_list_org.append(s)
        old_list.append(get_stemmed(s, True))
  for s in string.splitfields(new, '\n'):
    s = s.strip()
    if s != '':
      s = encode_html(s)
      new_list_org.append(s)
      new_list.append(get_stemmed(s, True))
  o = set(old_list)
  n = set(new_list)
  o_org = set(old_list_org)
  n_org = set(new_list_org)
  return list(n.difference(o)), list(o.difference(n)), list(n_org.difference(o_org))

# -----------------------------------------------------
def save_schlagworte(edu_item, new):
  """ .. speichert bzw. loescht die Verweise auf gestemmte Schlagworte """
  schlagworte_insert, \
  schlagworte_delete, \
  schlagworte_insert_org = get_schlagworte(new['schlagwort'], None)
  for schlagwort in schlagworte_insert:
    i = schlagworte_insert.index(schlagwort)
    insert_stemmed_keyword(edu_item, schlagwort, schlagworte_insert_org[i])

# -----------------------------------------------------
def save_modified_schlagworte(edu_item, old, new):
  """ .. speichert bzw. loescht die Verweise auf gestemmte Schlagworte """
  schlagworte_insert, \
  schlagworte_delete, \
  schlagworte_insert_org = get_schlagworte(new['schlagwort'], old['schlagwort'])
  for schlagwort in schlagworte_delete:
    delete_stemmed_keyword(edu_item, schlagwort)
  for schlagwort in schlagworte_insert:
    i = schlagworte_insert.index(schlagwort)
    insert_stemmed_keyword(edu_item, schlagwort, schlagworte_insert_org[i])

# -----------------------------------------------------
def save_modified_multiple_checkbox(old, new, name, obj):
  #item_new = new.getlist(name)
  item_new = new[name]
  item_old = old[name]
  for i in item_old:
    if not str(i) in item_new:
      obj.remove(i)
  for i in item_new:
    if not int(i) in item_old:
      obj.add(i)

# -----------------------------------------------------
def get_description_link(item_container, expand_mode = True):
  """ .. liefert eine verkuerzte Anzeige der Metadaten-URL """
  if item_container.item.app.is_folderish:
    desc_url = item_container.get_absolute_url()
    if expand_mode:
      desc_url += '?show_details=1'
    desc_url_path = '..' + desc_url[desc_url.find('/',7):]
  else:
    desc_url = item_container.get_absolute_url()
    desc_url_path = '..' + desc_url[desc_url.find('/',7):]
  return show_link(desc_url, desc_url_path)