#-*-coding: utf-8 -*-
"""
/mediasurvey/models.py

.. beschreibt die Datenbankstrukturen des Medien-Fragebogens
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.04.2007  Beginn der Arbeit
0.02  22.04.2007  Speichern der Werte
"""

import  datetime
import  string
import  re

from django.utils.encoding  import smart_unicode
from django.db              import models

from django.utils.translation import ugettext as _

from dms.auth.models        import User
#from dms.models             import get_last_modified

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsMediaSurvey(models.Model):
  """ Beschreibung den Web-Fragebogen ... """
  # 1
  org_id                  = models.IntegerField(unique=True)
  last_modified           = models.DateTimeField(default=datetime.datetime.now())
  eigene_com              = models.BooleanField(default=False)
  # 1.1
  raeume_gesamt           = models.IntegerField(default=0)
  mit_com_pcraum          = models.IntegerField(default=0)
  mit_com_fachraum        = models.IntegerField(default=0)
  ohne_com_pcraum         = models.IntegerField(default=0)
  ohne_com_fachraum       = models.IntegerField(default=0)
  anz_com_pcraum          = models.IntegerField(default=0)
  anz_com_fachraum        = models.IntegerField(default=0)
  nutzung_sch_com         = models.BooleanField(default=False)
  # --- Nutzungsmoeglichkeiten separat: nutzung_raum_com
  # 1.2
  typ_1                   = models.IntegerField(default=0)
  typ_1_mobil             = models.IntegerField(default=0)
  typ_2                   = models.IntegerField(default=0)
  typ_2_mobil             = models.IntegerField(default=0)
  notebook                = models.IntegerField(default=0)
  notebook_klasse         = models.IntegerField(default=0)
  # 1.3 Peripherie separat: peri
  # 1.4 Software separat: software
  # 1.5 Lernplattform separat: lernplattform
  eigene_plattform        = models.BooleanField(default=False)
  #2.
  netz                    = models.BooleanField(default=False)
  # --- Betriebssystem separat: netz_bs
  netz_com                = models.IntegerField(default=0)
  netz_wlan               = models.IntegerField(default=0)
  netz_raum               = models.IntegerField(default=0)
  #3.
  internet                = models.BooleanField(default=False)
  # --- Internetanschluss separat: internet
  internet_anz            = models.IntegerField(default=0)
  # 4.1 Computereinsatz separat: com_einsatz_x
  # 4.2 Interneteinsatz separat: int_einsatz_x
  com_beruf               = models.IntegerField(default=0)
  com_foerder             = models.IntegerField(default=0)
  # 4.3 Einsatzschwerpunkte separat: einsatz_x
  # 4.4 Landeslizenzen separat: landeslizenz_x
  # 4.5 Unterstuetzungssystem separat: unterstuetzung_x
  # 4.6 Fortbildung separat: fortbildung_x
  # 4.7
  nutzung                 = models.IntegerField(default=0)
  int_website             = models.CharField(max_length=120)

  def __unicode__(self):
    return smart_unicode(self.org_id)

  class Meta:
    db_table = 'dms_ms_dmsmediasurvey'

  def save_values(self, org_id, new_values):
    """ speichert die Werte in new_values """
    self.org_id = org_id
    # 1 eigene Computer
    self.eigene_com         = new_values['eigene_com']
    self.mit_com_pcraum     = new_values['mit_com_pcraum']
    self.mit_com_fachraum   = new_values['mit_com_fachraum']
    self.ohne_com_pcraum    = new_values['ohne_com_pcraum']
    self.ohne_com_fachraum  = new_values['ohne_com_fachraum']
    self.anz_com_pcraum     = new_values['anz_com_pcraum']
    self.anz_com_fachraum   = new_values['anz_com_fachraum']
    self.nutzung_sch_com    = new_values['nutzung_sch_com']
    # 1.1 Raeume insgesamt
    self.raeume_gesamt      = new_values['raeume_gesamt']
    # 1.2 Hardware
    self.typ_1              = new_values['typ_1']
    self.typ_1_mobil        = new_values['typ_1_mobil']
    self.typ_2              = new_values['typ_2']
    self.typ_2_mobil        = new_values['typ_2_mobil']
    self.notebook           = new_values['notebook']
    self.notebook_klasse    = new_values['notebook_klasse']
    # 1.5 Lernplattform
    self.eigene_plattform   = new_values['eigene_plattform']
    # 2 Netz
    self.netz               = new_values['netz']
    self.netz_com           = new_values['netz_com']
    self.netz_wlan          = new_values['netz_wlan']
    self.netz_raum          = new_values['netz_raum']
    # 3 Internet
    self.internet           = new_values['internet']
    self.internet_anz       = new_values['internet_anz']
    # 4.2
    self.com_beruf          = new_values['com_beruf']
    self.com_foerder        = new_values['com_foerder']
    # 4.4
    self.int_website        = new_values['int_website']
    # 4.7
    self.nutzung            = new_values['nutzung']
    #self.last_modified     = get_last_modified()
    self.last_modified      = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    self.save()

  class Admin:
    fields = (
        (None,  {'fields': ('org_id', 'last_modified', 'eigene_com')}),
        ('1.1 Unterrichtsräume', 
                {'fields': ('raeume_gesamt', 'mit_com_pcraum', 'mit_com_fachraum',
                            'ohne_com_pcraum', 'ohne_com_fachraum', 'anz_com_pcraum',
                            'anz_com_fachraum', 'nutzung_sch_com')}),
        ('1.2 Hardware', 
                {'fields': ('typ_1', 'typ_1_mobil', 'typ_2', 'typ_2_mobil',
                            'notebook', 'notebook_klasse')}),
        ('1.5 Lernplattformen', 
                {'fields': ('eigene_plattform',)}),
        ('2 Vernetzung',   
                {'fields': ('netz', 'netz_com', 'netz_wlan', 'netz_raum')}),
        ('3 Internet',   
                {'fields': ('internet', 'internet_anz')}),
        ('4 Nutzung',   
                {'fields': ('nutzung',)}),
    )
    list_filter = ( 'last_modified', )
    list_display = ( 'id', 'org_id', 'last_modified' )
    pass

class DmsMediaSurvey_gruppe(models.Model):
  """ Beschreibung der Auswahl-Items ... """
  gruppe = models.CharField(max_length=40, db_index=True)

  def __unicode__(self):
    return self.gruppe

  class Meta:
    db_table = 'dms_ms_dmsmediasurvey_gruppe'

  class Admin:
    ordering = [ 'id', ]
    list_display = ( 'id', 'gruppe' )
    pass

class DmsMediaSurvey_option(models.Model):
  """ Beschreibung der Auswahl-Items ... """
  gruppe = models.ForeignKey(DmsMediaSurvey_gruppe)
  option = models.CharField(max_length=40, db_index=True)
  title  = models.CharField(max_length=120)

  def __unicode__(self):
    return self.option

  class Meta:
    db_table = 'dms_ms_dmsmediasurvey_option'

  class Admin:
    list_filter = ( 'gruppe', )
    ordering = [ 'option' ]
    list_display = ( 'id', 'gruppe', 'option', 'title' )
    pass

class DmsMediaSurvey_gruppe_form(models.Model):
  """ Beschreibung der Auswahl-Items ... """
  gruppe = models.ForeignKey(DmsMediaSurvey_gruppe)
  form   = models.CharField(max_length=40, db_index=True)
  title  = models.CharField(max_length=120)

  def __unicode__(self):
    return self.form

  class Meta:
    db_table = 'dms_ms_dmsmediasurvey_gruppe_form'

  class Admin:
    list_filter = ( 'gruppe', )
    ordering = [ 'gruppe', 'form' ]
    list_display = ( 'id', 'gruppe', 'form', 'title' )
    pass

class DmsMediaSurvey_items(models.Model):
  """ Beschreibung der Auswahl-Items ... """
  gruppe_form   = models.ForeignKey(DmsMediaSurvey_gruppe_form)
  option = models.ForeignKey(DmsMediaSurvey_option)
  multi  = models.BooleanField(default=False)
  org_id = models.IntegerField(db_index=True)

  def __unicode__(self):
    return smart_unicode(self.org_id) + ' :: ' + smart_unicode(self.option)

  class Meta:
    db_table = 'dms_ms_dmsmediasurvey_items'

  class Admin:
    list_filter = ( 'org_id', )
    ordering = [ 'org_id', 'gruppe_form', ]
    list_display = ( 'id', 'org_id', 'gruppe_form', 'option' )
    pass

