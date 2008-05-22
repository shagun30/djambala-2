#-*-coding: utf-8 -*-
"""
/dms/agenda/models.py

.. beschreibt die Datenbankstrukturen fuer Terminplaner für Institutionen
            Django content Management System

Werner Fabian
werner.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.01.2008  Beginn der Arbeit
"""

from django.db import models

from django.utils.translation import ugettext as _
#from dms.models               import DmsOrg
from dms.auth.models          import User

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------


class DmsAgendaType(models.Model):
  """ Termins-Art (z.B. 'Ferien', 'Sportereignis', 'Konferenz', ,,,) """
  name                  = models.TextField()

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_agenda_type'


class DmsAgendaDescription(models.Model):
  """ Beschreibungsdaten eines Termins """
  title                 = models.CharField(max_length=100)
  user                  = models.ForeignKey(User)
  description           = models.TextField()
  url                   = models.URLField()
  type                  = models.ForeignKey(DmsAgendaType)
  entire_days           = models.BooleanField()
  who_reads             = models.IntegerField()

  def __unicode__(self):
    return self.org

  class Meta:
    db_table = 'dms_agenda_description'


class DmsAgendaAppointment(models.Model):
  """ ein bestimmter Termin """
  description           = models.ForeignKey(DmsAgendaDescription)
  datetime_start        = models.DateTimeField()
  datetime_end          = models.DateTimeField()
  
  def __unicode__(self):
    return self.datetime_start

  class Meta:
    db_table = 'dms_agenda_appointment'


class DmsAgendaDescriptionGroup(models.Model):
  """ Verbindung Beschreibung - Personengruppe """
  description           = models.ForeignKey(DmsAgendaDescription)
  #group                 = models.ForeignKey(<ID der Benutzergruppe>) # **********************
  approved              = models.BooleanField()
  
  #def __unicode__(self):
  #  return self.datetime_start

  class Meta:
    db_table = 'dms_agenda_descr_group'

# Noch klären:
#  1. Wie sind Benutzergruppen realisiert?
#  2. "Gruppe - Gruppe" ?