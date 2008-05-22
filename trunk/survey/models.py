#-*-coding: utf-8 -*-
"""
/dms/survey/models.py

.. beschreibt die Datenbankstrukturen fuer Frageboegen
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.01.2008  Beginn der Arbeit
"""

from django.db import models

from django.utils.translation import ugettext as _
from dms.models  import DmsItem

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsSurvey(models.Model):
  """ Basisklasse fuer die Antworten """
  survey        = models.ForeignKey(DmsItem)  # Fragebogen
  pers_id       = models.IntegerField(db_index=True)  # user_id oder negative Zahl
  last_modified = models.DateTimeField()

  def __unicode__(self):
    return self.survey.title

  class Meta:
    db_table = 'dms_survey'

class DmsSurveyInput(models.Model):
  """ Klasse fuer input-Eingabefelder """
  survey        = models.ForeignKey(DmsItem)  # Fragebogen
  pers_id       = models.IntegerField(db_index=True)  # user_id oder negative Zahl
  question_id   = models.IntegerField(db_index=True)  # id der Frage
  value         = models.CharField(max_length=200)

  class Meta:
    db_table = 'dms_survey_input'

class DmsSurveyText(models.Model):
  """ Klasse fuer textarea-Eingabefelder """
  survey        = models.ForeignKey(DmsItem)  # Fragebogen
  pers_id       = models.IntegerField(db_index=True)  # user_id oder negative Zahl
  question_id   = models.IntegerField(db_index=True)  # id der Frage
  value         = models.TextField(null=True)

  class Meta:
    db_table = 'dms_survey_text'

