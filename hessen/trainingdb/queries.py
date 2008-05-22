# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/queries.py

.. enthaelt Zugriffsmethoden fuer das Fortbilungs-Modell in SQLalchemy fuer
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.02.2008  Beginn der Arbeit
0.02  04.03.2008  get_fach_by_name
0.03  06.03.2008  +/- bei Volltextsuche
"""

import types 
import string

from sqlalchemy.sql import and_, not_, or_
from sqlalchemy.sql import select, text
from sqlalchemy.orm import eagerload

from dms.hessen.trainingdb.models import Session
from dms.hessen.trainingdb.models import session
from dms.hessen.trainingdb.models import Fach
from dms.hessen.trainingdb.models import Schulart
from dms.hessen.trainingdb.models import Zielgruppe
from dms.hessen.trainingdb.models import Anbieter
from dms.hessen.trainingdb.models import Veranstaltung
from dms.hessen.trainingdb.models import Veranstaltungsart

from dms.hessen.trainingdb.models import anbieter_table
from dms.hessen.trainingdb.models import faecher_table
from dms.hessen.trainingdb.models import veranst_faecher_table
from dms.hessen.trainingdb.models import gueltig_table
from dms.hessen.trainingdb.models import schularten_table
from dms.hessen.trainingdb.models import veranst_schularten_table
from dms.hessen.trainingdb.models import zielgruppen_table
from dms.hessen.trainingdb.models import veranst_zielgruppen_table
from dms.hessen.trainingdb.models import veranst_table

from dms.utils    import clean_data

#from dms.hessen.trainingdb.models import test_table

# -----------------------------------------------------
def do_transmit(s):
  """ wertet die Session aus """
  session = Session()
  session.begin()
  try:
    result = session.execute(s)
    session.commit()
    return result
  except:
    session.rollback()
    return None

# -----------------------------------------------------
def get_fach_list(item_container):
  """ liefert die Liste der moeglichen Faecher """
  #return session.query(Fach).order_by(Fach.fach_name)
  if item_container.item.integer_1 < 1:
    s = select([faecher_table],
              faecher_table.c.fach_id==veranst_faecher_table.c.fach_id)
  else:
    s = select([faecher_table],
              and_(faecher_table.c.fach_id==veranst_faecher_table.c.fach_id,
                   veranst_faecher_table.c.veranst_iq_id==veranst_table.c.veranst_iq_id,
                   veranst_table.c.veranst_gueltig_id==item_container.item.integer_1)
                  )
  s = s.distinct().order_by(faecher_table.c.fach_name)
  return do_transmit(s)

# -----------------------------------------------------
def get_gueltig_list():
  """ liefert die Liste der Gueltigkeitsbereiche """
  s = select([gueltig_table],
             gueltig_table.c.gueltig_id==veranst_table.c.veranst_gueltig_id)
  s = s.distinct().order_by(gueltig_table.c.gueltig_name)
  return do_transmit(s)

# -----------------------------------------------------
def get_schulart_list(item_container):
  """ liefert die Liste der moeglichen Schularten """
  #return session.query(Schulart).order_by(Schulart.schulart_name)
  if item_container.item.integer_1 < 1:
    s = select([schularten_table],
              schularten_table.c.schulart_id==veranst_schularten_table.c.schulart_id)
  else:
    s = select([schularten_table],
              and_(schularten_table.c.schulart_id==veranst_schularten_table.c.schulart_id,
                   veranst_schularten_table.c.veranst_iq_id==veranst_table.c.veranst_iq_id,
                   veranst_table.c.veranst_gueltig_id==item_container.item.integer_1)
                  )
  s = s.distinct().order_by(schularten_table.c.schulart_name)
  return do_transmit(s)

# -----------------------------------------------------
def get_zielgruppe_list(item_container):
  """ liefert die Liste der moeglichen Zielgruppen """
  #return session.query(Zielgruppe).order_by(Zielgruppe.zielgruppe_name)
  if item_container.item.integer_1 < 1:
    s = select([zielgruppen_table],
              zielgruppen_table.c.zielgruppe_id==veranst_zielgruppen_table.c.zielgruppe_id)
  else:
    s = select([zielgruppen_table],
              and_(zielgruppen_table.c.zielgruppe_id==veranst_zielgruppen_table.c.zielgruppe_id,
                   veranst_zielgruppen_table.c.veranst_iq_id==veranst_table.c.veranst_iq_id,
                   veranst_table.c.veranst_gueltig_id==item_container.item.integer_1)
                  )
  s = s.distinct().order_by(zielgruppen_table.c.zielgruppe_name)
  return do_transmit(s)

# -----------------------------------------------------
def get_anbieter_list(item_container):
  """ liefert die Liste der moeglichen Anbieter """
  #return session.query(Anbieter).order_by(Anbieter.anbieter_name)
  if item_container.item.integer_1 < 1:
    s = select([anbieter_table],
                anbieter_table.c.anbieter_iq_id==veranst_table.c.veranst_anbieter_iq_id)
  else:
    s = select([anbieter_table],
                and_(anbieter_table.c.anbieter_iq_id==veranst_table.c.veranst_anbieter_iq_id,
                     veranst_table.c.veranst_gueltig_id==item_container.item.integer_1)
                    )
  s = s.distinct().order_by(anbieter_table.c.anbieter_name)
  return do_transmit(s)

def get_anbieter_by_iq_id(anbieter_iq_id):
  """ liefert den zu anbieter_iq_id passenden Anbieter """
  query = session.query(Anbieter).filter_by(anbieter_iq_id=anbieter_iq_id)
  return query.one()

# -----------------------------------------------------
def get_veranstaltung_count(item_container):
  """ liefert die Liste der moeglichen Anbieter """
  if item_container.item.integer_1 < 1:
    return session.query(Veranstaltung).count()
  else:
    return session.query(Veranstaltung).\
                   filter_by(veranst_gueltig_id=item_container.item.integer_1).count()

# -----------------------------------------------------
def get_veranstaltung_by_iq_id(veranst_iq_id):
  """ liefert eine Einzelveranstaltung """
  #query = session.query(Veranstaltung).join('rel_anbieter').add_entity(Anbieter)
  query = session.query(Veranstaltung).add_entity(Anbieter).join('rel_anbieter')
  query = query.add_entity(Veranstaltungsart).join('rel_v_art')
  query = query.reset_joinpoint()
  query = query.filter_by(veranst_iq_id=veranst_iq_id)
  try:
    return query.one()
  except:
    return None

# -----------------------------------------------------
def get_veranstaltungen_by_filter(data):
  """ liefert die zu data passenden Veranstaltungen """
  if data == {}:
    return []
  data = clean_data(data)
  query = ''
  # --- SELECT
  _select = """SELECT
    DISTINCT v.veranst_iq_id, v.veranst_thema, v.veranst_kosten, v.veranst_datum_von, a.anbieter_name
"""
  _from = """FROM
    veranst_tb=v
    ,anbieter_tb=a
    ,v_art_tb=va
    ,gueltig_tb=g
"""
  # --- FROM
  iq_id_mode = (data.has_key('training_iq_nummer') and data['training_iq_nummer'] != '')
  intern_id_mode = (data.has_key('training_intern_nummer') and data['training_intern_nummer'] != '')
  if not iq_id_mode and not intern_id_mode:
    if data.has_key('training_fach') and int(data['training_fach']) != -1:
      _from += """    ,faecher_tb=f
      ,veranst_faecher_vtb=vf """
    if data.has_key('training_schulart') and int(data['training_schulart']) != -1:
      _from += """    ,schularten_tb=s
      ,veranst_schularten_vtb=vs """
    if data.has_key('training_zielgruppe') and int(data['training_zielgruppe']) != -1:
      _from += """    ,zielgruppen_tb=z
      ,veranst_zielgruppen_vtb=vz """

  # --- WHERE
  _where = """ WHERE
    a.anbieter_iq_id=v.veranst_anbieter_iq_id
    and va.v_art_id=v.veranst_v_art_id
    and g.gueltig_id=v.veranst_gueltig_id """
  if iq_id_mode:
    _where += """     and v.veranst_iq_id='%s' """ % data['training_iq_nummer']
  elif intern_id_mode:
    _where += """     and v.veranst_intern_id='%s' """ % data['training_intern_nummer']
  else:
    if data.has_key('training_gueltig') and int(data['training_gueltig']) != -1:
      _where += """    and v.veranst_gueltig_id=%i """ % int(data['training_gueltig'])
    if data.has_key('training_fach') and int(data['training_fach']) != -1:
      _where += """    and f.fach_id=%i
      and f.fach_id=vf.fach_id
      and vf.veranst_iq_id=v.veranst_iq_id """ % int(data['training_fach'])
    if data.has_key('training_anbieter') and data['training_anbieter'] != '' \
    and data['training_anbieter'] != '-1':
      _where += """    and v.veranst_anbieter_iq_id='%s' """ % data['training_anbieter']
    if data.has_key('training_schulart') and int(data['training_schulart']) != -1:
      _where += """    and s.schulart_id=vs.schulart_id 
      and s.schulart_id=%i
      and vs.veranst_iq_id=v.veranst_iq_id """ % int(data['training_schulart'])
    if data.has_key('training_zielgruppe') and int(data['training_zielgruppe']) != -1:
      _where += """    and z.zielgruppe_id=vz.zielgruppe_id 
      and z.zielgruppe_id=%i
      and vz.veranst_iq_id=v.veranst_iq_id """ % int(data['training_zielgruppe'])
    if data.has_key('training_text') and data['training_text'] != '':
      my_text = data['training_text'].strip()
      if len(data['training_text'])>3:
        boolean_mode = ' in boolean mode'
        words = string.splitfields(my_text)
        if len(words) > 1:
          my_text = ''
          for word in words:
            if my_text != '':
              my_text += ' '
            if word[0] == '+' or word[0] == '-':
              my_text += word
            else:
              my_text += '+' + word
      else:
        boolean_mode = ''
      _where += """    and
        match 
        ( 
              veranst_thema,
              veranst_dient_zu,
              veranst_hinweise,
              veranst_beschreibung,
              veranst_zusatz,
              veranst_ort,
              veranst_leitung,
              veranst_dozenten
        )
        against
        ( '%s' %s ) """ % (my_text, boolean_mode)
  # --- ORDER_BY
  _order = """ORDER BY veranst_thema, veranst_datum_von """
  s = text(_select + _from + _where + _order)
  return do_transmit(s)

# -----------------------------------------------------
def get_schularten_by_veranst_iq_id(veranst_iq_id):
  """ liefert die Liste der zu der Veranstaltung veranst_iq_id passenden Schularten """
  query = session.query(Veranstaltung).add_entity(Schulart).join('rel_schulart')
  query = query.reset_joinpoint()
  query = query.filter_by(veranst_iq_id=veranst_iq_id)
  return query.all()

# -----------------------------------------------------
def get_zielgruppen_by_veranst_iq_id(veranst_iq_id):
  """ liefert die Liste der zu der Veranstaltung veranst_iq_id passenden Zielgruppen """
  query = session.query(Veranstaltung).add_entity(Zielgruppe).join('rel_zielgruppe')
  query = query.reset_joinpoint()
  query = query.filter_by(veranst_iq_id=veranst_iq_id)
  return query.all()

# -----------------------------------------------------
def get_faecher_by_veranst_iq_id(veranst_iq_id):
  """ liefert die Liste der zu der Veranstaltung veranst_iq_id passenden Faecher """
  query = session.query(Veranstaltung).add_entity(Fach).join('rel_fach')
  query = query.reset_joinpoint()
  query = query.filter_by(veranst_iq_id=veranst_iq_id)
  return query.all()

# -----------------------------------------------------
def get_fach_by_name(name):
  """ liefert das Fach zu name """
  query = session.query(Fach).filter_by(fach_name=name)
  try:
    return query.one()
  except:
    return None

# -----------------------------------------------------
def get_schulart_by_name(name):
  """ liefert das Fach zu name """
  query = session.query(Schulart).filter_by(schulart_name=name)
  try:
    return query.one()
  except:
    return None

