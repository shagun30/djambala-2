# -*- coding: utf-8 -*-
"""
/dms/hessen/schooldb/models.py

.. enthaelt das Schul-Modell in SQLalchemy fuer
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  10.02.2008  Beginn der Arbeit
0.02  11.02.2008  ORG_DB
0.03  07.03.2008  Umstellung auf Schulbasisdaten
"""

from dms.settings     import ORG_DB

from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Unicode, Text, Binary, Date
from sqlalchemy import PassiveDefault
from sqlalchemy import MetaData, ForeignKey, UniqueConstraint

from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------
# Zugangsdaten fuer schul_db

if ORG_DB.has_key('SCHUL_DB'):
  schul_db = ORG_DB['SCHUL_DB']
else:
  schul_db = ''

# -----------------------------------------------------

metadata = MetaData()

# -----------------------------------------------------
# Deklaration der Besonderen-Einrichtung-Tabelle
beseinrichtung_table = Table('Key_BesEinr', metadata, 
    Column(u'CodeKey', Unicode(length=8), primary_key=True), 
    Column(u'TextKey', Unicode(length=60)), 
    Column(u'Ver', Binary(256)), 
)

class KeyBesEinrichtung(object):
  """ Klasse zur besonderen-Einrichtung-Tabelle """
  def __init__(self, CodeKey, TextKey, Gruppe, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Ver = Ver

  def __rep__(self):
    return "<BesEinrichtung('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Gemeinde-Tabelle
gemeinde_table = Table('Key_Gemeinde', metadata, 
    Column(u'Gem_Kz', Unicode(length=11), primary_key=True), 
    Column(u'Gemeinde', Unicode(length=60)), 
    Column(u'Ver', Binary(256)),
)

class KeyGemeinde(object):
  """ Klasse zur Gemeinde-Tabelle """
  def __init__(self, Gem_Kz, Gemeinde, Ver):
    self.Gem_Kz = Gem_Kz
    self.Gemeinde = Gemeinde
    self.Ver = Ver

  def __rep__(self):
    return "<Gemeinde('%s', '%s')>" % (self.Gem_Kz, self.Gemeinde)

# -----------------------------------------------------
# Deklaration der Rechtsstellung-Tabelle
rechtsstellung_table = Table('Key_Rechtsstellung', metadata, 
    Column(u'CodeKey', Unicode(length=4), primary_key=True),
    Column(u'TextKey', Unicode(length=60)), 
    Column(u'StatusRS', Integer(length=6), nullable=False, default=PassiveDefault(0)), 
    Column(u'Ver', Binary(256)), 
)

class KeyRechtsstellung(object):
  """ Klasse zur Rechtsstellung-Tabelle """
  def __init__(self, CodeKey, TextKey, StatusRS, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.StatusRS = StatusRS
    self.Ver = Ver

  def __rep__(self):
    return "<Rechtsstellung('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Schulamt-Tabelle
schulamt_table = Table('Key_Schulamt', metadata,
     Column('CodeKey', Unicode(4), primary_key=True),
     Column('TextKey', Unicode(60)),
     Column('RegPraesidium', Unicode(4)),
     Column('Land', Unicode(4)),
     Column('Ver', Binary(256)),
 )

class KeySchulamt(object):
  """ Klasse zur Schulamt-Tabelle """
  def __init__(self, CodeKey, TextKey, RegPraesidium, Land, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.RegPraesidium = RegPraesidium
    self.Land = Land
    self.Ver = Ver

  def __rep__(self):
    return "<Schulamt('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Schultraeger-Tabelle
schultraeger_table = Table('Key_Schultraeger', metadata,
     Column('CodeKey', Unicode(4), primary_key=True),
     Column('TextKey', Unicode(60)),
     Column('Ver', Binary(256)),
 )

class KeySchultraeger(object):
  """ Klasse zur Schultraeger-Tabelle """
  def __init__(self, CodeKey, TextKey, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Ver = Ver

  def __rep__(self):
    return "<Schultraeger('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Schultyp-Tabelle
schultyp_table = Table('Key_Schultyp', metadata, 
    Column(u'CodeKey', Unicode(length=4), primary_key=True), 
    Column(u'TextKey', Unicode(length=60)), 
    Column(u'Gruppe', Unicode(length=4)), 
    Column(u'Ver', Binary(256)),
    )

class KeySchultyp(object):
  """ Klasse zur Schultyp-Tabelle """
  def __init__(self, CodeKey, TextKey, Gruppe, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Gruppe = Gruppe
    self.Ver = Ver

  def __rep__(self):
    return "<Schultyp('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Schulformangebot-Tabelle
sformangebot_table = Table('Key_Sformangebot', metadata,
     Column('CodeKey', Unicode(4), primary_key=True),
     Column('TextKey', Unicode(60)),
     Column('Ver', Binary(256)),
 )

class KeySformangebot(object):
  """ Klasse zur Schulformangebot-Tabelle """
  def __init__(self, CodeKey, TextKey, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Ver = Ver

  def __rep__(self):
    return "<Sformangebot('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Sprachenfolge-Tabelle
sprachenfolge_table = Table('Key_Sprachenfolge', metadata,
     Column('CodeKey', Unicode(4), primary_key=True),
     Column('TextKey', Unicode(60)),
     Column('Ver', Binary(256)),
 )

class KeySprachenfolge(object):
  """ Klasse zur Sprachenfolge-Tabelle """
  def __init__(self, CodeKey, TextKey, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Ver = Ver

  def __rep__(self):
    return "<Sprachenfolge('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Voraussetzung-Tabelle
voraussetzung_table = Table('Key_Voraussetzung', metadata,
     Column('CodeKey', Unicode(4), primary_key=True),
     Column('TextKey', Unicode(60)),
     Column('Ver', Binary(256)),
 )

class KeyVoraussetzung(object):
  """ Klasse zur Voraussetzung-Tabelle """
  def __init__(self, CodeKey, TextKey, Ver):
    self.CodeKey = CodeKey
    self.TextKey = TextKey
    self.Ver = Ver

  def __rep__(self):
    return "<Voraussetzung('%s', '%s')>" % (self.CodeKey, self.TextKey)

# -----------------------------------------------------
# Deklaration der Schulstamm-Tabelle
schulstamm_table = Table('Schulstamm', metadata, 
    Column(u'ID', Unicode(length=40), primary_key=True),
    Column(u'dummy', Unicode(length=40)), 
    Column(u'Schul_Nr', Integer(length=6), primary_key=True, nullable=False, default=PassiveDefault(0)), 
    Column(u'NameSchule', Unicode(length=70)), 
    Column(u'Namenszusatz', Unicode(length=150)), 
    Column(u'Kurzbezeichnung', Unicode(length=20)), 
    Column(u'Schultyp', Unicode(length=4), ForeignKey('Key_Schultyp.CodeKey')), 
    Column(u'Rechtsstellung', Unicode(length=4), ForeignKey('Key_Rechtsstellung.CodeKey')), 
    Column(u'Schultraeger', Unicode(length=4), ForeignKey('Key_Schultraeger.CodeKey')), 
    Column(u'Schulamt', Unicode(length=4), ForeignKey('Key_Schulamt.CodeKey')), 
)

class Schulstamm(object):
  """ Klasse fuer Schulstamm-Daten """
  def __init__(self, ID, Schul_Nr, NameSchule, Namenszusatz, Kurzbezeichnung, Schultyp,
                     Rechtsstellung, Schulamt, Schultraeger):
    self.ID = ID
    self.Schul_Nr = Schul_Nr
    self.NameSchule = NameSchule
    self.Namenszusatz = Namenszusatz
    self.Kurzbezeichnung = Kurzbezeichnung
    self.Rechtsstellung = Rechtsstellung
    self.Schultyp = Schultyp
    self.Schulamt = Schulamt
    self.Schultraeger = Schultraeger

  def __rep__(self):
    return "<Schulstamm('%i', '%s')>" % (self.Schul_Nr, self.NameSchule)

# -----------------------------------------------------
# Deklaration der Schulstelle-Tabelle
schulstelle_table = Table('Schulstelle', metadata, 
    Column(u'ID', Unicode(length=40), primary_key=True),
    Column(u'SchulID', Unicode(length=40), ForeignKey('Schulstamm.ID')), 
    Column(u'Standort_Kz', Integer(length=6), nullable=False, default=PassiveDefault(0)), 
    Column(u'NameStelle', Unicode(length=70)), 
    Column(u'Str_Nr', Unicode(length=40)), 
    Column(u'PLZ', Integer(length=11), nullable=False, default=PassiveDefault(0)), 
    Column(u'Ort', Unicode(length=40)), 
    Column(u'Tel1', Unicode(length=18)), 
    Column(u'Tel2', Unicode(length=18)), 
    Column(u'Fax', Unicode(length=18)), 
    Column(u'Modem', Unicode(length=18)), 
    Column(u'E_Mail', Unicode(length=120)), 
    Column(u'Gem_Kz', Unicode(length=11), ForeignKey('Key_Gemeinde.Gem_Kz')), 
    Column(u'Gruendungsjahr', Unicode(length=4)), 
    Column(u'Letzteerweiterung', Unicode(length=4)), 
    Column(u'Loesch_Datum', Unicode(length=12)), 
)

class Schulstelle(object):
  """ Klasse fuer Schulstelle-Daten """
  def __init__(self, ID, SchulID, Standort_Kz, NameStelle, Str_Nr, PLZ,
                     Ort, Tel1, Tel2, Fax, Modem, Gem_Kz, Gruendungsjahr, Letzteerweiterung,
                     Loesch_Datum):
    self.ID = ID
    self.SchulID = SchulID
    self.Standort_Kz = Standort_Kz
    self.NamensStelle = NamensStelle
    self.Str_Nr = Str_Nr
    self.PLZ = PLZ
    self.Ort = Ort
    self.Tel1 = Tel1
    self.Tel2 = Tel2
    self.Fax = Fax
    self.Modem = Modem
    self.Gem_Kz =Gem_Kz
    self.Gruendungsjahr = Gruendungsjahr
    self.Letzteerweiterung = Letzteerweiterung
    self.Loesch_Datum = Loesch_Datum

  def __rep__(self):
    return "<Schulstelle('%i', '%s')>" % (self.Standort_Kz, self.NameStelle)

# -----------------------------------------------------
# Deklaration der Schulstelle-Besondere-Einrichtungen-Tabelle

schulst_beseinr_table = Table('Schulst_BesEinr', metadata, 
    Column(u'StelleID', Unicode(length=250), ForeignKey('Schulstelle.ID')),
    Column(u'CodeKey', Unicode(length=4), ForeignKey('Key_BesEinr.CodeKey')),
    UniqueConstraint(u'StelleID', u'CodeKey', name='PRIMARY'),
)

# -----------------------------------------------------
# Deklaration der Schulstelle-Schulformangebote-Tabelle

schulst_sformangebot_table = Table('Schulst_Sformangebot', metadata, 
    Column(u'StelleID', Unicode(length=40), ForeignKey('Schulstelle.ID'), index=True),
    Column(u'CodeKey', Unicode(length=4), ForeignKey('Key_Sformangebot.CodeKey'), index=True),
    Column(u'Datum_1', Date()),
    Column(u'Datum_2', Date()),
    Column(u'Datum_3', Date()),
)

# -----------------------------------------------------
# Deklaration der Schulstelle-Sprachenfolge-Tabelle

schulst_sprfolge_table = Table('Schulst_SprFolge', metadata, 
    Column(u'StelleID', Unicode(length=50), ForeignKey('Schulstelle.ID')),
    Column(u'CodeKey', Unicode(length=4), ForeignKey('Key_Sprachenfolge.CodeKey')),
    UniqueConstraint(u'StelleID', u'CodeKey', name='PRIMARY'),
)

# -----------------------------------------------------
# Deklaration der Schulstelle-Kooedukation-Tabelle

schulst_voraussetzung_table = Table('Schulst_Vorausse', metadata, 
    Column(u'StelleID', Unicode(length=250), ForeignKey('Schulstelle.ID')),
    Column(u'CodeKey', Unicode(length=4), ForeignKey('Key_Voraussetzung.CodeKey')),
    UniqueConstraint(u'StelleID', u'CodeKey', name='PRIMARY'),
)

# -----------------------------------------------------
# Deklaration der Erweiterungstabelle Schulbasisdaten
schulbasisdaten_table = Table('Schulbasisdaten', metadata, 
    Column(u'id', Integer(length=11), primary_key=True),
    Column(u'Schul_Nr', Integer(length=11), ForeignKey('Schulstamm.Schul_Nr'), primary_key=True),
    Column(u'Name_Ort', Unicode(length=60)),
    Column(u'Name_Schule', Unicode(length=60)),
    Column(u'Homepage', Unicode(length=120)),
    Column(u'Homepage2', Unicode(length=120)),
    Column(u'Logo_URL', Unicode(length=120)),
    Column(u'Region', Unicode(length=10)),
    Column(u'Profil', Text()),
)

class Schulbasisdaten(object):
  """ Klasse fuer Schulbasisdaten """
  def __init__(self, id, Schul_Nr, Name_Ort, Name_Schule, Homepage, Homepage2,
                     Logo_URL, Region):
    self.id = id
    self.Schul_Nr = Schul_Nr
    self.Name_Ort = Name_Ort
    self.Name_Schule = Name_Schule
    self.Homepage = Homepage
    self.Homepage2 = Homepage2
    self.Logo_URL = Logo_URL
    self.Region = Region

  def __rep__(self):
    return "<Schulbasisdaten('%i', '%s', '%s')>" % (self.Schul_Nr, self.Name_Ort, self.Name_Schule)

# -----------------------------------------------------
# Verbindung: Tabelle und ORM-Mapper
mapper(KeyBesEinrichtung, beseinrichtung_table)
mapper(KeyGemeinde, gemeinde_table)
mapper(KeyRechtsstellung, rechtsstellung_table)
mapper(KeySchulamt, schulamt_table)
mapper(KeySchultraeger, schultraeger_table)
mapper(KeySchultyp, schultyp_table)
mapper(KeySformangebot, sformangebot_table)
mapper(KeySprachenfolge, sprachenfolge_table)
mapper(KeyVoraussetzung, voraussetzung_table)

#mapper(Schulrec, schulrec_table, properties={
#        'rel_schulstamm2': relation(Schulstamm, backref='ref_schulstamm2'),
#      })
mapper(Schulbasisdaten, schulbasisdaten_table, properties={
        'rel_schulstamm2': relation(Schulstamm, backref='ref_schulstamm2'),
      })
mapper(Schulstamm, schulstamm_table, properties={
        'rel_rechtsstellung': relation(KeyRechtsstellung, backref='ref_rechtsstellung'),
        'rel_schultyp': relation(KeySchultyp, backref='ref_schultyp'),
        'rel_schulamt': relation(KeySchulamt, backref='ref_schulamt'),
        'rel_schultraeger': relation(KeySchultraeger, backref='ref_schultraeger'),
        'rel_schulstelle': relation(Schulstelle, backref='ref_schulstelle'),
        'rel_basis': relation(Schulbasisdaten, backref='ref_basis'),
      })
mapper(Schulstelle, schulstelle_table, properties={
        'rel_schulstamm': relation(Schulstamm, backref='ref_schulstamm'),
        'rel_gemeinde': relation(KeyGemeinde, backref='ref_gemeinde'),
        'rel_bes_einrichtung': relation(KeyBesEinrichtung, secondary=schulst_beseinr_table),
        'rel_sformangebot': relation(KeySformangebot, secondary=schulst_sformangebot_table),
        'rel_sprfolge': relation(KeySprachenfolge, secondary=schulst_sprfolge_table),
        'rel_voraussetzung': relation(KeyVoraussetzung, secondary=schulst_voraussetzung_table),
      })

engine = create_engine(schul_db, pool_size=40, pool_recycle=30, strategy='threadlocal')
engine.echo = False
metadata.create_all(engine)
metadata.bind = engine

#test_table = Table('schulrec_tb', metadata, autoload=True)

Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
session = Session()
