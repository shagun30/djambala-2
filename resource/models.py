#-*-coding: utf-8 -*-
"""
/dms/resource/models.py

.. beschreibt die Datenbankstrukturen fuer Ressourcenverwaltungen
            Django content Management System

Werner Fabian
werner.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.01.2008  Beginn der Arbeit
"""

from django.db import models

from django.utils.translation import ugettext as _
from dms.models               import DmsOrg
from dms.auth.models          import User

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsResourceSettings(models.Model):
  """ Zeitanzeige als Zeitpunkt ('09:35-10:20') oder verbale Beschreibung ('dritte Stunde') """
  org                   = models.ForeignKey(DmsOrg)
  #time_start            = models.DateTimeField(db_index=True)
  #time_end              = models.DateTimeField(db_index=True)
  time_start            = models.TimeField(db_index=True)
  time_end              = models.TimeField(db_index=True)
  name                  = models.TextField()
  is_period             = models.BooleanField()

  def __unicode__(self):
    return self.org

  class Meta:
    db_table = 'dms_res_settings'

class DmsResourceType(models.Model):
  """ Ressourcen-Typ (z.B. 'Laptop')"""
  org                   = models.ForeignKey(DmsOrg)
  description           = models.CharField(max_length=100)

  def __unicode__(self):
    return self.org

  class Meta:
    db_table = 'dms_res_type'

class DmsResourceResource(models.Model):
  """ Beschreibung einer einzelnen Ressource (z.B. 'Medienraum Nr. 217 ...') """
  res_type              = models.ForeignKey(DmsResourceType)
  description           = models.CharField(max_length=100)
  description_more      = models.TextField()
  url                   = models.URLField()

  def __unicode__(self):
    return self.type

  class Meta:
    db_table = 'dms_res_resource'

class DmsResourceEvent(models.Model):
  """ Reservierungsdaten einer Ressource """
  resource              = models.ForeignKey(DmsResourceResource)
  datetime_start        = models.DateTimeField()
  datetime_end          = models.DateTimeField()
  user                  = models.ForeignKey(User)

  def __unicode__(self):
    return self.resource

  class Meta:
    db_table = 'dms_res_event'

class DmsResourceComplaint(models.Model): # momentan nicht benutzt
  """ Maengelbeschreibung """
  resource              = models.ForeignKey(DmsResourceResource)
  datetime              = models.DateTimeField()
  complaint             = models.TextField()
  user                  = models.ForeignKey(User)
  reply                 = models.TextField()
  during_use            = models.BooleanField()

  def __unicode__(self):
    return self.resource

  class Meta:
    db_table = 'dms_res_complaint'

class DmsResourceBlocked(models.Model): # momentan nicht benutzt
  """ regelmaessig blockierte Termine (z.B. 'jeden Mittwoch von 10:00-11:00') """
  resource              = models.ForeignKey(DmsResourceResource)
  weekday               = models.IntegerField()
  time_start            = models.TimeField(db_index=True)
  time_end              = models.TimeField(db_index=True)
  purpose               = models.TextField()

  def __unicode__(self):
    return self.resource

  class Meta:
    db_table = 'dms_res_blocked'
