#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  25.01.2008  Beginn der Arbeit
"""

from django.utils.encoding  import smart_unicode

from dms.models   import DmsOrg, DmsOrgGroup, User

from dms.models   import DmsItem, DmsItemContainer, DmsContainer
from dms.edufolder.models   import DmsEduItem, DmsEduOrg
from dms.edufolder.models   import DmsEduFachSachgebiet, DmsEduLernResTyp, DmsEduMedienformat
from dms.edufolder.models   import DmsEduObjekt, DmsEduSchlagwort, DmsEduSchlagwortStem
from dms.edufolder.models   import DmsEduSchulart, DmsEduSchulstufe, DmsEduSprache
from dms.edufolder.models   import DmsEduZielgruppe

from dms.elixier.models     import DmsElixierBildungsebene, DmsElixierFach, DmsElixierMedienformat
from dms.elixier.models     import DmsElixierSchlagwort, DmsElixierOrg

from dms.settings import *
from dms.encode_decode import decode_html


def do_correct_auth_org():
  auths = DmsOrg.objects.all()
  for a in auths:
    organisation = a.organisation
    organisation_new = decode_html(organisation)
    sub_organisation = a.sub_organisation
    sub_organisation_new = decode_html(sub_organisation)
    street = a.street
    street_new = decode_html(street)
    if organisation != organisation_new or sub_organisation != sub_organisation_new or \
       street != street_new:
      print '*',
      a.organisation = organisation_new
      a.sub_organisation = sub_organisation_new
      a.street = street_new
      try:
        a.save()
      except:
        print
        print 'org', a.id

def do_correct_auth_org_group():
  auths = DmsOrgGroup.objects.all()
  for a in auths:
    name = a.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      a.name = name_new
      try:
        a.save()
      except:
        print
        print 'org_group', a.id

def do_correct_auth_user():
  auths = User.objects.all()
  for a in auths:
    first_name = a.first_name
    first_name_new = decode_html(first_name)
    last_name = a.last_name
    last_name_new = decode_html(last_name)
    if first_name != first_name_new or last_name != last_name_new:
      print '*',
      a.first_name = first_name_new
      a.last_name = last_name_new
      try:
        a.save()
      except:
        print
        print 'user', a.id

def do_correct_items():
  items = DmsItem.objects.all()
  for item in items:
    print 'item', item.id,
    title = item.title
    title_new = decode_html(title)
    sub_title = item.sub_title
    sub_title_new = decode_html(sub_title)
    text = item.text
    text_new = decode_html(text)
    text_more = item.text_more
    text_more_new = decode_html(text_more)
    info_slot_right = item.info_slot_right
    info_slot_right_new = decode_html(info_slot_right)
    string_1 = item.string_1
    string_1_new = decode_html(string_1)
    string_2 = item.string_2
    string_2_new = decode_html(string_2)
    if title != title_new or sub_title !=sub_title_new or text != text_new or text_more != text_more_new \
      or info_slot_right != info_slot_right_new or string_1 != string_1_new or string_2 != string_2_new:
      print title_new
      item.title = title_new
      item.sub_title = sub_title_new
      item.text = text_new
      item.text_more = text_more_new
      item.info_slot_right = info_slot_right_new
      item.string_1 = string_1_new
      item.string_2 = string_2_new
      item.save()
    else:
      print

def do_correct_item_containers():
  ics = DmsItemContainer.objects.all()
  for ic in ics:
    print 'item_container', ic.id,
    section = ic.section
    section_new = decode_html(section)
    if section != section_new:
      print section_new
      ic.section = section_new
      ic.save()
    else:
      print

def do_correct_containers():
  cs = DmsContainer.objects.all()
  for c in cs:
    print 'container', c.id,
    sections = c.sections
    sections_new = decode_html(sections)
    if sections != sections_new:
      print sections_new
      c.sections = sections_new
      c.save()
    else:
      print

def do_correct_edu_items():
  edu_items = DmsEduItem.objects.all()
  for edu in edu_items:
    autor = edu.autor
    autor_new = decode_html(autor)
    herausgeber = edu.herausgeber
    herausgeber_new = decode_html(herausgeber)
    anbieter_herkunft = edu.anbieter_herkunft
    anbieter_herkunft_new = decode_html(anbieter_herkunft)
    preis = edu.preis
    preis_new = decode_html(preis)
    titel_lang = edu.titel_lang
    titel_lang_new = decode_html(titel_lang)
    beschreibung_lang = edu.beschreibung_lang
    beschreibung_lang_new = decode_html(beschreibung_lang)
    if autor != autor_new or herausgeber != herausgeber_new or anbieter_herkunft != anbieter_herkunft_new \
       or preis != preis_new or titel_lang != titel_lang_new or beschreibung_lang != beschreibung_lang_new:
      print '*',
      edu.autor = autor_new
      edu.herausgeber = herausgeber_new
      edu.anbieter_herkunft = anbieter_herkunft_new
      edu.preis = preis_new
      edu.titel_lang = titel_lang_new
      edu.beschreibung_lang = beschreibung_lang_new
      try:
        edu.save()
      except:
        print
        print 'edu_item', edu.id

def do_correct_edu_orgs():
  edu_items = DmsEduOrg.objects.all()
  for edu in edu_items:
    beschreibung = edu.beschreibung
    beschreibung_new = decode_html(beschreibung)
    if beschreibung != beschreibung_new:
      print '*',
      edu.beschreibung = beschreibung_new
      try:
        edu.save()
      except:
        print
        print 'edu_org', edu.id

def do_correct_edu_fach_sachgebiete():
  edu_fach_seachgebiete = DmsEduFachSachgebiet.objects.all()
  for edu in edu_fach_seachgebiete:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_fach_sachgebiet', edu.id

def do_correct_edu_lernrestypen():
  edu_lernrestypen = DmsEduLernResTyp.objects.all()
  for edu in edu_lernrestypen:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_lernrestyp', edu.id

def do_correct_edu_medienformate():
  edu_medienformate = DmsEduMedienformat.objects.all()
  for edu in edu_medienformate:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_medienformat', edu.id

def do_correct_edu_objekte():
  edu_objekte = DmsEduObjekt.objects.all()
  for edu in edu_objekte:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_medienformat', edu.id

def do_correct_edu_schlagworte():
  edu_schlagworte = DmsEduSchlagwort.objects.all()
  for edu in edu_schlagworte:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_schlagwort', edu.id

def do_correct_edu_schlagwortestem():
  edu_schlagwortestem = DmsEduSchlagwortStem.objects.all()
  for edu in edu_schlagwortestem:
    name = edu.name
    name_new = decode_html(name)
    stem = edu.stem
    stem_new = decode_html(stem)
    if name != name_new or stem != stem_new:
      print '*',
      edu.name = name_new
      edu.stem = stem_new
      try:
        edu.save()
      except:
        print
        print 'edu_schlagwortestem', edu.id

def do_correct_edu_schularten():
  edu_schularten = DmsEduSchulart.objects.all()
  for edu in edu_schularten:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_schulart', edu.id

def do_correct_edu_schulstufen():
  edu_schulstufen = DmsEduSchulstufe.objects.all()
  for edu in edu_schulstufen:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_schulstufe', edu.id

def do_correct_edu_sprachen():
  edu_sprachen = DmsEduSprache.objects.all()
  for edu in edu_sprachen:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_sprache', edu.id

def do_correct_edu_zielgruppen():
  edu_zielgruppen = DmsEduZielgruppe.objects.all()
  for edu in edu_zielgruppen:
    name = edu.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      edu.name = name_new
      try:
        edu.save()
      except:
        print
        print 'edu_sprache', edu.id

def do_correct_elixier_bildungsebenen():
  elixier_bildungsebenen = DmsElixierBildungsebene.objects.all()
  for elixier in elixier_bildungsebenen:
    name = elixier.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      elixier.name = name_new
      try:
        elixier.save()
      except:
        print
        print 'elixier_bildungsebenen', elixier.id

def do_correct_elixier_faecher():
  elixier_faecher = DmsElixierFach.objects.all()
  for elixier in elixier_faecher:
    name = elixier.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      elixier.name = name_new
      try:
        elixier.save()
      except:
        print
        print 'elixier_fach', elixier.id

def do_correct_elixier_medienformate():
  elixier_formate = DmsElixierMedienformat.objects.all()
  for elixier in elixier_formate:
    name = elixier.name
    name_new = decode_html(name)
    if name != name_new:
      print '*',
      elixier.name = name_new
      try:
        elixier.save()
      except:
        print
        print 'elixier_format', elixier.id

def do_correct_elixier_schlagworte():
  elixier_schlagworte = DmsElixierSchlagwort.objects.all()
  for elixier in elixier_schlagworte:
    schlagwort = elixier.schlagwort
    schlagwort_new = decode_html(schlagwort)
    if schlagwort != schlagwort_new:
      print '*',
      elixier.schlagwort = schlagwort_new
      try:
        elixier.save()
      except:
        print
        print 'elixier_schlagwort', elixier.id

def do_correct_elixier_orgs():
  elixier_orgs = DmsElixierOrg.objects.all()
  for elixier in elixier_orgs:
    anbieter_herkunft = elixier.anbieter_herkunft
    anbieter_herkunft_new = decode_html(anbieter_herkunft)
    autor = elixier.autor
    autor_new = decode_html(autor)
    beschreibung = elixier.beschreibung
    beschreibung_new = decode_html(beschreibung)
    beschreibung_lang = elixier.beschreibung_lang
    beschreibung_lang_new = decode_html(beschreibung_lang)
    bildungsebene = elixier.bildungsebene
    bildungsebene_new = decode_html(bildungsebene)
    einsteller = elixier.einsteller
    einsteller_new = decode_html(einsteller)
    fach_sachgebiet = elixier.fach_sachgebiet
    fach_sachgebiet_new = decode_html(fach_sachgebiet)
    herausgeber = elixier.herausgeber
    herausgeber_new = decode_html(herausgeber)
    kmk_standards = elixier.kmk_standards
    kmk_standards_new = decode_html(kmk_standards)
    lehrplanbezug = elixier.lehrplanbezug
    lehrplanbezug_new = decode_html(lehrplanbezug)
    lernressourcentyp = elixier.lernressourcentyp
    lernressourcentyp_new = decode_html(lernressourcentyp)
    lernziel = elixier.lernziel
    lernziel_new = decode_html(lernziel)
    medienformat = elixier.medienformat
    medienformat_new = decode_html(medienformat)
    methodik = elixier.methodik
    methodik_new = decode_html(methodik)
    preis = elixier.preis
    preis_new = decode_html(preis)
    rechte = elixier.rechte
    rechte_new = decode_html(rechte)
    schlagwort = elixier.schlagwort
    schlagwort_new = decode_html(schlagwort)
    schulform = elixier.schulform
    schulform_new = decode_html(schulform)
    sprache = elixier.sprache
    sprache_new = decode_html(sprache)
    systematikpfad = elixier.systematikpfad
    systematikpfad_new = decode_html(systematikpfad)
    techn_voraussetzungen = elixier.techn_voraussetzungen
    techn_voraussetzungen_new = decode_html(techn_voraussetzungen)
    titel = elixier.titel
    titel_new = decode_html(titel)
    titel_lang = elixier.titel_lang
    titel_lang_new = decode_html(titel_lang)
    weitere_kompetenzen = elixier.weitere_kompetenzen
    weitere_kompetenzen_new = decode_html(weitere_kompetenzen)
    zertifizierung = elixier.zertifizierung
    zertifizierung_new = decode_html(zertifizierung)
    zielgruppe = elixier.zielgruppe
    zielgruppe_new = decode_html(zielgruppe)
    if autor != autor_new or herausgeber != herausgeber_new or anbieter_herkunft != anbieter_herkunft_new or \
       preis != preis_new or titel_lang != titel_lang_new or beschreibung_lang != beschreibung_lang_new or \
       beschreibung != beschreibung_new or bildungsebene != bildungsebene_new or einsteller != einsteller_new or \
       fach_sachgebiet != fach_sachgebiet_new or kmk_standards != kmk_standards_new or \
       lehrplanbezug != lehrplanbezug_new or lernressourcentyp != lernressourcentyp_new or \
       lernziel != lernziel_new or medienformat != medienformat_new or methodik != methodik_new or \
       rechte != rechte_new or schlagwort != schlagwort_new or schulform != schulform_new or \
       sprache != sprache_new or systematikpfad != systematikpfad_new or \
       techn_voraussetzungen != techn_voraussetzungen_new or titel != titel_new or \
       weitere_kompetenzen != weitere_kompetenzen_new or zertifizierung != zertifizierung_new or \
       zielgruppe != zielgruppe_new:
      print '*',
      elixier.anbieter_herkunft = anbieter_herkunft_new
      elixier.autor = autor_new
      elixier.beschreibung = beschreibung_new
      elixier.beschreibung_lang = beschreibung_lang_new
      elixier.bildungsebene = bildungsebene_new
      elixier.einsteller = einsteller_new
      elixier.fach_sachgebiet = fach_sachgebiet_new
      elixier.herausgeber = herausgeber_new
      elixier.kmk_standards = kmk_standards_new
      elixier.lehrplanbezug = lehrplanbezug_new
      elixier.lernressourcentyp = lernressourcentyp_new
      elixier.lernziel = lernziel_new
      elixier.medienformat = medienformat_new
      elixier.methodik = methodik_new
      elixier.preis = preis_new
      elixier.rechte = rechte_new
      elixier.schlagwort = schlagwort_new
      elixier.schulform = schulform_new
      elixier.sprache = sprache_new
      elixier.systematikpfad = systematikpfad_new
      elixier.techn_voraussetzungen = techn_voraussetzungen_new
      elixier.titel = titel_new
      elixier.titel_lang = titel_lang_new
      elixier.weitere_kompetenzen != weitere_kompetenzen_new
      elixier.zertifizierung != zertifizierung_new
      elixier.zielgruppe != zielgruppe_new
      try:
        elixier.save()
      except:
        print
        print 'elixier_org', elixier.id

do_correct_auth_org()
do_correct_auth_org()
do_correct_auth_user()

"""
do_correct_items()
do_correct_containers()
do_correct_item_containers()
do_correct_edu_items()
do_correct_edu_orgs()
do_correct_edu_fach_sachgebiete()
do_correct_edu_lernrestypen()
do_correct_edu_medienformate()
do_correct_edu_objekte()
do_correct_edu_schlagworte()
do_correct_edu_schlagwortestem()
do_correct_edu_schularten()
do_correct_edu_schulstufen()
do_correct_edu_sprachen()
do_correct_edu_zielgruppen()

do_correct_elixier_bildungsebenen()
do_correct_elixier_faecher()
do_correct_elixier_medienformate()
do_correct_elixier_schlagworte()
do_correct_elixier_orgs()
"""