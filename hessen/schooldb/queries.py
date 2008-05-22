# -*- coding: utf-8 -*-
"""
/dms/hessen/schooldb/queries.py

.. enthaelt Zugriffsmethoden fuer das Schul-Modell in SQLalchemy fuer
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  10.02.2008  Beginn der Arbeit
0.02  13.02.2008  get_schulen_by_filter
"""

import types 

from sqlalchemy.sql import and_, not_, or_
from sqlalchemy.sql import select, text

from dms.hessen.schooldb.models import session
from dms.hessen.schooldb.models import KeyBesEinrichtung
from dms.hessen.schooldb.models import KeyRechtsstellung
from dms.hessen.schooldb.models import KeySchulamt
from dms.hessen.schooldb.models import KeySchultraeger
from dms.hessen.schooldb.models import KeySchultyp
from dms.hessen.schooldb.models import KeySformangebot
from dms.hessen.schooldb.models import KeySprachenfolge
from dms.hessen.schooldb.models import KeyVoraussetzung

from dms.hessen.schooldb.models import Schulbasisdaten
from dms.hessen.schooldb.models import Schulstamm
from dms.hessen.schooldb.models import Schulstelle

from dms.utils    import clean_data

#from dms.hessen.schooldb.models import test_table

# -----------------------------------------------------
def get_bes_einrichtung_all():
  """ liefert alle besonderen Einrichtungen """
  return session.query(KeyBesEinrichtung).filter_by(Ver='').\
         order_by(KeyBesEinrichtung.TextKey)

# -----------------------------------------------------
def get_rechtsstellung_all():
  """ liefert die möglichen Rechtsstellungen """
  return session.query(KeyRechtsstellung).filter_by(Ver='').\
         order_by(KeyRechtsstellung.TextKey)

# -----------------------------------------------------
def get_schulamt_all():
  """ liefert alle Schulaemter """
  return session.query(KeySchulamt).filter_by(Ver='').\
         order_by(KeySchulamt.TextKey)

# -----------------------------------------------------
def get_schultraeger_all():
  """ liefert alle Schultraeger """
  return session.query(KeySchultraeger).filter_by(Ver='').\
         order_by(KeySchultraeger.TextKey)

# -----------------------------------------------------
def get_schultyp_all():
  """ liefert alle Schultraeger """
  return session.query(KeySchultyp).\
         filter(and_(not_(KeySchultyp.Gruppe=='HKM'),
                     not_(KeySchultyp.Gruppe=='SONS'),
                     not_(KeySchultyp.Gruppe=='ST'))).\
         order_by(KeySchultyp.TextKey)

# -----------------------------------------------------
def get_sformangebot_all():
  """ liefert alle Schultraeger """
  return session.query(KeySformangebot).filter_by(Ver='').\
         order_by(KeySformangebot.TextKey)

# -----------------------------------------------------
def get_sprachenfolge_all():
  """ liefert die moeglichen Sprachenfolgen """
  return session.query(KeySprachenfolge).filter_by(Ver='').\
         order_by(KeySprachenfolge.TextKey)

# -----------------------------------------------------
def get_voraussetzung_all():
  """ liefert die moeglichen Sprachenfolgen """
  return session.query(KeyVoraussetzung).filter_by(Ver='').\
         order_by(KeyVoraussetzung.TextKey)

# -----------------------------------------------------
def get_schulen_all():
  """ liefert alle moeglichen Schulen """
  return session.query(Schulstamm).\
         order_by(Schulstamm.Schul_Nr)

# -----------------------------------------------------
def get_schulen_by_filter(data):
  """ liefert die zu data passenden Schulen """
  if data == {}:
    return []
  data = clean_data(data)
  query = session.query(Schulstamm).add_entity(Schulstelle).join('rel_schulstelle')
  # --- Filter fuer Schulstelle
  query = query.filter_by(Standort_Kz=0).filter_by(Loesch_Datum='')
  if data.has_key('schul_ort') and data['schul_ort'] != '':
    query = query.filter(Schulstelle.Ort.like(data['schul_ort']+u'%'))
  if data.has_key('schul_plz') and data['schul_plz'] != '':
    query = query.filter_by(PLZ=data['schul_plz'])
  # ---- Zusatzmerkmale
  if data.has_key('schul_beseinr') and data['schul_beseinr'] != '-1':
    s = data['schul_beseinr']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter(Schulstelle.rel_bes_einrichtung.any(CodeKey=s))
    else:
      query = query.filter(Schulstelle.rel_bes_einrichtung.any(KeyBesEinrichtung.CodeKey.in_(s)))
  if data.has_key('schul_sformangebot') and data['schul_sformangebot'] != '-1':
    s = data['schul_sformangebot']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter(Schulstelle.rel_sformangebot.any(CodeKey=s))
    else:
      query = query.filter(Schulstelle.rel_sformangebot.any(KeySformangebot.CodeKey.in_(s)))
  if data.has_key('schul_sprfolge') and data['schul_sprfolge'] != '-1':
    s = data['schul_sprfolge']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter(Schulstelle.rel_sprfolge.any(CodeKey=s))
    else:
      query = query.filter(Schulstelle.rel_sprfolge.any(KeySprachenfolge.CodeKey.in_(s)))
  if data.has_key('schul_voraussetzung') and data['schul_voraussetzung'] != '-1':
    s = data['schul_voraussetzung']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter(Schulstelle.rel_voraussetzung.any(CodeKey=s))
    else:
      query = query.filter(Schulstelle.rel_voraussetzung.any(KeyVoraussetzung.CodeKey.in_(s)))

  # --- Schulstamm
  query = query.reset_joinpoint()
  # --- Studienseminare etc. ausschliessen
  query = query.order_by(Schulstamm.NameSchule).filter(not_(Schulstamm.Schulamt==u'LH'))
  if data.has_key('schul_name') and data['schul_name'] != '':
    query = query.filter(Schulstamm.NameSchule.like(data['schul_name']+u'%'))
  if data.has_key('schul_nr') and data['schul_nr'] != '':
    query = query.filter_by(Schul_Nr=data['schul_nr'])
  if data.has_key('schul_typ') and data['schul_typ'] != '-1':
    s = data['schul_typ']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter_by(Schultyp=s)
    else:
      query = query.filter(Schulstamm.Schultyp.in_(s))
  if data.has_key('schul_amt') and data['schul_amt'] != '-1':
    s = data['schul_amt']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter_by(Schulamt=s)
    else:
      query = query.filter(Schulstamm.Schulamt.in_(s))
  if data.has_key('schul_traeger') and data['schul_traeger'] != '-1':
    s = data['schul_traeger']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter_by(Schultraeger=s)
    else:
      query = query.filter(Schulstamm.Schultraeger.in_(s))
  if data.has_key('schul_rechtsstellung') and data['schul_rechtsstellung'] != '-1':
    s = data['schul_rechtsstellung']
    if type(s) in [types.StringType, types.UnicodeType]:
      query = query.filter_by(Rechtsstellung=s)
    else:
      query = query.filter(Schulstamm.Rechtsstellung.in_(s))

  # --- Schulbasisdaten
  query = query.join('rel_basis')
  if data.has_key('region') and data['region'] != '':
    query = query.filter_by(Region=data['region'])
  return query.all()

# -----------------------------------------------------
def get_schule_by_schul_nr(schul_nr):
  """ liefert Einzelschule """
  if schul_nr < 0:
    return []
  query = session.query(Schulstelle).add_entity(Schulstamm).join('rel_schulstamm')
  query = query.filter_by(Schul_Nr=schul_nr)
  query = query.add_entity(Schulbasisdaten)
  query = query.filter(Schulstamm.Schul_Nr==Schulbasisdaten.Schul_Nr)
  return query.all()

# -----------------------------------------------------
def get_sprachenfolge_by_stelle_id(stelle_id):
  """ liefert die Sprachenfolge der betreffenden Schulstelle """
  query = session.query(Schulstelle).filter_by(ID=stelle_id)
  query = query.add_entity(KeySprachenfolge).join('rel_sprfolge')
  return query.all()

# -----------------------------------------------------
def get_bes_einrichtung_by_stelle_id(stelle_id):
  """ liefert die besonderen Einrichtungen der Schulstelle """
  query = session.query(Schulstelle).filter_by(ID=stelle_id)
  query = query.add_entity(KeyBesEinrichtung).join('rel_bes_einrichtung')
  return query.all()

# -----------------------------------------------------
def get_sformangebot_by_stelle_id(stelle_id):
  """ liefert die Schulformangebote der Schulstelle """
  query = session.query(Schulstelle).filter_by(ID=stelle_id)
  query = query.add_entity(KeySformangebot).join('rel_sformangebot')
  return query.all()

# -----------------------------------------------------
def get_schulbasisdaten_by_schul_nr(schul_nr):
  """ liefert die schulbasisdaten der betreffenden Schule """
  query = session.query(Schulbasisdaten).filter_by(Schul_Nr=schul_nr)
  return query.one()

# -----------------------------------------------------
def get_schulen_by_ort(ort):
  """ liefert die zu ort passenden Schulen """
  if ort == '':
    return []
  query = session.query(Schulstelle).add_entity(Schulstamm).join('rel_schulstamm')
  # --- Filter fuer Schulstamm
  # Studienseminare etc. ausschliessen
  query = query.order_by(Schulstamm.NameSchule).filter(not_(Schulstamm.Schulamt==u'LH'))
  query = query.reset_joinpoint().filter_by(Standort_Kz=0).filter_by(Loesch_Datum='')
  query = query.filter(Schulstelle.Ort.like(ort+u'%'))
  return query.all()

# -----------------------------------------------------
def get_regionen_all():
  """ liefert die vorhandenen Bildungsregionen """
  query = 'SELECT DISTINCT Region FROM Schulbasisdaten=sb ORDER BY Region'
  return session.execute(query)

# -----------------------------------------------------
def get_regionschulen_by_region(region):
  """ liefert die Schulen der Bildungsregion region """
  if region == '':
    return []
  query = """SELECT
    sta.NameSchule, ste.Ort, st.TextKey, sta.Schul_Nr, sb.Name_Ort, sb.Name_Schule
FROM
    Schulstamm=sta
    ,Schulstelle=ste
    ,Key_Schultyp=st
    ,Schulbasisdaten=sb
WHERE
    sb.Region='%s' AND
    sta.ID=ste.SchulID AND
    sta.Schul_Nr=sb.Schul_Nr AND
    sta.Schultyp=st.CodeKey AND
    ste.Standort_Kz=0 AND
    ste.Loesch_Datum=''
""" % region
  return session.execute(query)
