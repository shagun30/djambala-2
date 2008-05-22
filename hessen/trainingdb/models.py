# -*- coding: utf-8 -*-
"""
/dms/hessen/fortbildung/models.py

.. enthaelt das Fortbildungsmodell in SQLalchemy fuer
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.02.2008  Beginn der Arbeit
"""

from dms.settings     import ORG_DB

from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Unicode, Text, Binary, Date, DateTime
from sqlalchemy.databases.mysql import MSDecimal
from sqlalchemy import PassiveDefault
from sqlalchemy import MetaData, ForeignKey, UniqueConstraint

from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------
# Zugangsdaten fuer schul_db

if ORG_DB.has_key('VM_DB'):
  fortbildung_db = ORG_DB['VM_DB']
else:
  fortbildung_db = ''

# -----------------------------------------------------

metadata = MetaData()

# -----------------------------------------------------
# Deklaration der Anbieter-Tabelle
anbieter_table = Table('anbieter_tb', metadata, 
    Column(u'anbieter_id', Integer, primary_key=True, nullable=False), 
    Column(u'anbieter_iq_id', Unicode(length=20), primary_key=True), 
    Column(u'anbieter_name', Unicode(length=240)), 
    Column(u'anbieter_person', Unicode(length=80)), 
    Column(u'anbieter_strasse', Unicode(length=80)), 
    Column(u'anbieter_plz', Unicode(length=15)), 
    Column(u'anbieter_ort', Unicode(length=80)), 
    Column(u'anbieter_telefon', Unicode(length=100)), 
    Column(u'anbieter_fax', Unicode(length=100)), 
    Column(u'anbieter_email', Unicode(length=150)), 
    Column(u'anbieter_url', Unicode(length=150)), 
)

class Anbieter(object):
  """ Klasse Anbieter-Tabelle """
  def __init__(self, id, iq_id, name, person, strasse, plz, ort, telefon, fax, email, url):
    self.anbieter_id = id
    self.anbieter_iq_id = iq_id
    self.anbieter_name = name
    self.anbieter_person = person
    self.anbieter_strasse = strasse
    self.anbieter_plz = plz
    self.anbieter_ort = ort
    self.anbieter_telefon = telefon
    self.anbieter_fax = fax
    self.anbieter_email = email
    self.anbieter_url = url

  def __rep__(self):
    return "<Anbieter('%s', '%s', '%s')>" % (self.anbieter_id, self.anbieter_iq_id, self.anbieter_name)

# -----------------------------------------------------
# Deklaration der Faecher-Tabelle
faecher_table = Table('faecher_tb', metadata, 
    Column(u'fach_id', Integer, primary_key=True),
    Column(u'fach_name', Unicode(length=60)),
)

class Fach(object):
  """ Klasse Faecher-Tabelle """
  def __init__(self, id, name):
    self.fach_id = id
    self.fach_name = name

  def __rep__(self):
    return "<Fach('%s', '%s')>" % (self.fach_id, self.fach_name)

# -----------------------------------------------------
# Deklaration der Gueltigkeits-Tabelle
gueltig_table = Table('gueltig_tb', metadata, 
    Column(u'gueltig_id', Integer, primary_key=True),
    Column(u'gueltig_name', Unicode(length=60)),
)

class Gueltig(object):
  """ Klasse Gueltigkeits-Tabelle """
  def __init__(self, id, name):
    self.gueltig_id = id
    self.gueltig_name = name

  def __rep__(self):
    return "<Gültigkeit('%s', '%s')>" % (self.fach_id, self.fach_name)

# -----------------------------------------------------
# Deklaration der Schularten-Tabelle
schularten_table = Table('schularten_tb', metadata, 
    Column(u'schulart_id', Integer, primary_key=True),
    Column(u'schulart_name', Unicode(length=60)),
)

class Schulart(object):
  """ Klasse Schulart-Tabelle """
  def __init__(self, id, name):
    self.schulart_id = id
    self.schulart_name = name

  def __rep__(self):
    return "<Schulart('%s', '%s')>" % (self.schulart_id, self.schulart_name)

# -----------------------------------------------------
# Deklaration der Veranstaltungsart-Tabelle
v_art_table = Table('v_art_tb', metadata, 
    Column(u'v_art_id', Integer, primary_key=True),
    Column(u'v_art_name', Unicode(length=60)),
)

class Veranstaltungsart(object):
  """ Klasse Veranstaltungsart-Tabelle """
  def __init__(self, id, name):
    self.v_art_id = id
    self.v_art_name = name

  def __rep__(self):
    return "<Veranstaltungsart('%s', '%s')>" % (self.v_art_id, self.v_art_name)

# -----------------------------------------------------
# Deklaration der Zielgruppen-Tabelle
zielgruppen_table = Table('zielgruppen_tb', metadata, 
    Column(u'zielgruppe_id', Integer, primary_key=True),
    Column(u'zielgruppe_name', Unicode(length=60)),
)

class Zielgruppe(object):
  """ Klasse Zielgruppen-Tabelle """
  def __init__(self, id, name):
    self.zielgruppe_id = id
    self.zielgruppe_name = name

  def __rep__(self):
    return "<Zielgruppe('%s', '%s')>" % (self.zielgruppe_id, self.zielgruppe_name)

# -----------------------------------------------------
# Deklaration der Veranstaltungs-Tabelle
veranst_table = Table('veranst_tb', metadata, 
    Column(u'veranst_id', Integer, nullable=False), 
    Column(u'veranst_iq_id', Unicode(length=40), primary_key=True), 
    Column(u'veranst_intern_id', Unicode(length=60), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_anbieter_iq_id', Unicode(length=20), ForeignKey('anbieter_tb.anbieter_iq_id')), 
    Column(u'veranst_punkte', Integer, nullable=False, default=PassiveDefault(0)), 
    Column(u'veranst_schriftl_nachweis', Unicode(length=255), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_thema', Unicode(length=255)), 
    Column(u'veranst_sort_datum', Date(), nullable=False, default=PassiveDefault(u'0000-00-00')), 
    Column(u'veranst_datum_von', DateTime(timezone=False)), 
    Column(u'veranst_datum_bis', DateTime(timezone=False)), 
    Column(u'veranst_vorl_datum', Unicode(length=120), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_anmeldung', Date(), nullable=False, default=PassiveDefault(u'0000-00-00')), 
    Column(u'veranst_dauer', Integer, nullable=False, default=PassiveDefault(0)), 
    Column(u'veranst_feste_teilnehmer', Unicode(length=120), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_dient_zu', Text(), nullable=False), 
    Column(u'veranst_hinweise', Text()), 
    Column(u'veranst_beschreibung', Text(), nullable=False), 
    Column(u'veranst_zusatz', Text(), nullable=False), 
    Column(u'veranst_ort', Unicode(length=255)), 
    Column(u'veranst_vorl_ort', Unicode(length=120), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_kosten', MSDecimal(precision=10, length=2, asdecimal=True), nullable=False, default=PassiveDefault(u'0.00')), 
    Column(u'veranst_url', Unicode(length=120), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_url_text', Unicode(length=200), nullable=False), 
    Column(u'veranst_leitung', Unicode(length=255), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_dozenten', Unicode(length=255), nullable=False, default=PassiveDefault(u'')), 
    Column(u'veranst_v_art_id', Integer, ForeignKey('v_art_tb.v_art_id')), 
    Column(u'veranst_gueltig_id', Integer, ForeignKey('gueltig_tb.gueltig_id')), 
    Column(u'veranst_status', Unicode(length=30), nullable=False, default=PassiveDefault(u'')), 
)

class Veranstaltung(object):
  """ Klasse Veranstaltung-Tabelle """

  def __rep__(self):
    return "<Veranstaltung('%s', '%s')>" % (self.veranst_iq_id, self.veranst_thema)

# -----------------------------------------------------
# Deklaration der Veranstaltung-Fach-Tabelle
veranst_faecher_table = Table('veranst_faecher_vtb', metadata, 
    Column(u'veranst_iq_id', Unicode(length=20), ForeignKey('veranst_tb.veranst_iq_id')),
    Column(u'fach_id', Integer, ForeignKey('faecher_tb.fach_id')),
)

# -----------------------------------------------------
# Deklaration der Veranstaltung-Schularten-Tabelle
veranst_schularten_table = Table('veranst_schularten_vtb', metadata, 
    Column(u'veranst_iq_id', Unicode(length=20), ForeignKey('veranst_tb.veranst_iq_id')),
    Column(u'schulart_id', Integer, ForeignKey('schularten_tb.schulart_id')),
)

# -----------------------------------------------------
# Deklaration der Veranstaltung-Zielgruppen-Tabelle
veranst_zielgruppen_table = Table('veranst_zielgruppen_vtb', metadata, 
    Column(u'veranst_iq_id', Unicode(length=20), ForeignKey('veranst_tb.veranst_iq_id')),
    Column(u'zielgruppe_id', Integer, ForeignKey('zielgruppen_tb.zielgruppe_id')),
)

# -----------------------------------------------------
# Verbindung: Tabelle und ORM-Mapper
mapper(Anbieter, anbieter_table)
mapper(Fach, faecher_table)
mapper(Gueltig, gueltig_table)
mapper(Schulart, schularten_table)
mapper(Veranstaltungsart, v_art_table)
mapper(Zielgruppe, zielgruppen_table)
mapper(Veranstaltung, veranst_table, properties={
        'rel_anbieter': relation(Anbieter),
        'rel_gueltig': relation(Gueltig),
        'rel_fach': relation(Fach, secondary=veranst_faecher_table),
        'rel_schulart': relation(Schulart, secondary=veranst_schularten_table),
        'rel_zielgruppe': relation(Zielgruppe, secondary=veranst_zielgruppen_table),
        'rel_v_art': relation(Veranstaltungsart),
      })

engine = create_engine(fortbildung_db, pool_size=40, pool_recycle=30, strategy='threadlocal')
metadata.create_all(engine)
metadata.bind = engine

#test_table = Table('veranst_tb', metadata, autoload=True)

Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
session = Session()
