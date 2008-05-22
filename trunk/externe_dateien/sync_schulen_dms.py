#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

0. aktuelle Schuldaten aufspielen
   PROBLEM: passwd
1. neue Schulen aufnehmen
   schul_db -> schul_db.Schulbasisdaten
   schul_db -> DmsOrg

händische Kontrolle; die nächsten Punkte erst wenn Schritt 1 abgeschlossen ist!!!!!

2. Schuldaten aktualisieren
   schul_db -> DmsOrg
3. nicht mehr vorhandene Schulen loeschen
   schul_db -> DmsOrg
   schul_db -> schul_db.Schulbasisdaten
   PROBLEM: Gibt es Community-Mitglieder dieser Institutionen?

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.04.2008  Beginn der Arbeit
"""

import string
import re
import time

from dms.settings import *
from dms.models   import DmsOrg

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

#from dms.hessen.schooldb.queries    import get_schulen_all
from dms.hessen.schooldb.queries    import get_schule_by_schul_nr

from dms.queries    import get_org_by_org_id

def set_org(org_id, organisation, sub_organisation, street, zip, town, phone, fax, email, homepage):
  """ aendert die Daten von org_id """
  org = get_org_by_org_id(org_id)
  if org != None:
    org.organisation = organisation
    org.sub_organisation = sub_organisation
    org.street = street
    org.zip = zip
    org.town = town
    org.phone = phone
    org.fax = fax
    org.email = email
    org.homepage = homepage
    org.save()
  else:
    org = DmsOrg()
    org.org_id = org_id
    org.organisation = organisation
    org.sub_organisation = sub_organisation
    org.street = street
    org.zip = zip
    org.town = town
    org.phone = phone
    org.fax = fax
    org.email = email
    org.homepage = homepage
    org.save()
    print 'Org existierte nicht: %i' % org_id

def get_schulen_all():
  """ liefert alle Schulen """
  query = session.query(Schulstelle).add_entity(Schulstamm).join('rel_schulstamm')
  # Studienseminare etc. ausschliessen
  query = query.order_by(Schulstamm.NameSchule).filter(not_(Schulstamm.Schulamt==u'LH'))
  query = query.reset_joinpoint().filter_by(Standort_Kz=0).filter_by(Loesch_Datum='')
  return query.all()

def get_schule_by_schul_nr_simple(schul_nr):
  """ liefert Einzelschule """
  if schul_nr < 0:
    return []
  query = session.query(Schulstelle).add_entity(Schulstamm).join('rel_schulstamm')
  query = query.filter_by(Schul_Nr=schul_nr)
  return query.all()

def get_schulbasis_by_schul_nr(schul_nr):
  """ liefert Einzelschule """
  #if schul_nr < 0:
  #  return []
  query = session.query(Schulbasisdaten)
  query = query.filter_by(Schul_Nr=schul_nr)
  return query.all()

# ------------------------------------------------------
#
# Schritt 1: Kontrolle, ob alle Schulen in Schulbasisdaten-Tabelle vorhanden sind
#
# ------------------------------------------------------

check_01 = True
print "Schritt 1: Kontrolle, ob alle Schulen in Schulbasisdaten-Tabelle vorhanden sind"
for s in get_schulen_all():
  schul_nr = s[1].Schul_Nr
  school = get_schule_by_schul_nr_simple(schul_nr)
  schulstelle = school[0][0]
  schulstamm = school[0][1]
  b = get_schulbasis_by_schul_nr(schul_nr)
  if len(b) == 0:
    check_01 = False
    insert = "INSERT INTO Schulbasisdaten VALUES(0, %i,'%s','%s','%s','%s','%s','%s','%s');" % \
             (schul_nr, schulstelle.Ort.lower(), schulstamm.NameSchule.lower(), '', '', '', schulstamm.Schulamt, '')
    print insert

# ------------------------------------------------------
#
# Schritt 2: Aktualisierung der Daten in DmsOrg
#
# ------------------------------------------------------

if check_01:
  print "Schritt 2: Aktualisierung der Daten in DmsOrg"
  for s in get_schulen_all():
    schul_nr = s[1].Schul_Nr
    school = get_schule_by_schul_nr(schul_nr)
    if len(school) == 0:
      print "PROBLEM", schul_nr
    else:
      #print len(school), school
      schulstelle = school[0][0]
      schulstamm = school[0][1]
      basisdaten = school[0][2]
      if schulstelle.Loesch_Datum == '':
        set_org(schul_nr, schulstamm.NameSchule, '', schulstelle.Str_Nr, schulstelle.PLZ, schulstelle.Ort,
                schulstelle.Tel1, schulstelle.Fax, schulstelle.E_Mail, basisdaten.Homepage)

# ------------------------------------------------------
#
# Schritt 2: Aktualisierung der Daten in DmsOrg
#
# ------------------------------------------------------

if check_01:
  print "Schritt 3: Gelöschte Schulen in DmsOrg ebenfalls löschen"
  print "Fehlt noch!"
