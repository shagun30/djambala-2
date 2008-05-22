#-*-coding: utf-8 -*-
"""
/dms/elixier/models.py

.. beschreibt die Datenbankstrukturen fuer den Elixieraustausch
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.07.2007  Beginn der Arbeit"""

from django.db              import models

from django.utils.translation import ugettext as _

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsElixierOrg(models.Model):
  """ Beschreibung der Originaldaten des Elixier-Datenaustausches ... """
  anbieter_herkunft = models.CharField(max_length=120)
  autor = models.CharField(max_length=80)
  autor_email = models.URLField()
  beschreibung = models.TextField()
  beschreibung_lang = models.TextField()
  bild_url = models.URLField()
  bildungsebene = models.TextField()
  einsteller = models.CharField(max_length=80, db_index=True)
  einsteller_email = models.URLField()
  fach_sachgebiet = models.TextField(db_index=True)
  herausgeber = models.CharField(max_length=120)
  id_local = models.CharField(max_length=64, unique=True)
  isbn = models.CharField(max_length=30)
  kmk_standards = models.TextField()
  lehrplanbezug = models.TextField()
  lernressourcentyp = models.TextField()
  lernzeit = models.CharField(max_length=60)
  lernziel = models.TextField()
  letzte_aenderung = models.DateTimeField(null=True)
  medienformat = models.TextField()
  methodik = models.TextField()
  preis = models.CharField(max_length=60)
  publikationsdatum = models.DateField(null=True)
  quelle_homepage_url = models.URLField()
  quelle_id = models.CharField(max_length=16, db_index=True)
  quelle_logo_url = models.URLField()
  quelle_pfad = models.CharField(max_length=60)
  rechte = models.TextField()
  schlagwort = models.TextField()
  schulform = models.TextField()
  sprache = models.TextField()
  systematikpfad = models.TextField()
  techn_voraussetzungen = models.TextField()
  titel = models.CharField(max_length=240)
  titel_lang = models.TextField()
  url_datensatz = models.URLField()
  url_ressource = models.URLField()
  verfallsdatum = models.DateField(null=True)
  weitere_kompetenzen = models.TextField()
  zertifizierung = models.TextField()
  zielgruppe = models.TextField()
  zeitstempel = models.DateTimeField()

  def __unicode__(self):
    return self.titel

  class Meta:
    db_table = 'dms_elixier_org'


class DmsElixierBildungsebene(models.Model):
  """ liefert die Fach/Sachgebiete gibt der aktuellen Datenbank? """
  name           = models.CharField(max_length=64, unique=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_elixier_bildungsebene'

class DmsElixierFach(models.Model):
  """ liefert die Fach/Sachgebiete der aktuellen Datenbank? """
  name  = models.CharField(max_length=64, unique=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_elixier_fach'

class DmsElixierMedienformat(models.Model):
  """ liefert die Medienformate der aktuellen Datenbank? """
  name          = models.CharField(max_length=64, unique=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_elixier_medienformat'

class DmsElixierQuelle(models.Model):
  """ liefert die Medienformate der aktuellen Datenbank? """
  name  = models.CharField(max_length=16, unique=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_elixier_quelle'

class DmsElixierSchlagwort(models.Model):
  """ liefert die Schlagworte der aktuellen Datenbank? """
  schlagwort  = models.CharField(max_length=64, unique=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_elixier_schlagwort'

class DmsElixierItem(models.Model):
  """ 
  Beschreibung, ob einzelne Elemente der Elixier-Datenbank verwendet werden ... 
  Status:  1 = uebernommen
  Status:  0 = indifferent
  Status: -1 = abgelehnt
  """
  id_local = models.CharField(max_length=64, unique=True)
  #item_id  = models.IntegerField()
  status   = models.IntegerField()
  fach_sachgebiet = models.IntegerField(default=-1)

  def __unicode__(self):
    return unicode(str(self.id_local))

  class Meta:
    db_table = 'dms_elixier_item'

