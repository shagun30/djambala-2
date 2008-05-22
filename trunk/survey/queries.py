#-*-coding: utf-8 -*-
"""
/dms/survey/queries.py

.. beschreibt die Datenbankabfragen fuer Frageboegen
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.01.2008  Beginn der Arbeit
"""

from django.db import transaction
from django.db import models

from django.utils.translation import ugettext as _

from dms.models  import DmsItem
from dms.models  import get_last_modified

from dms.survey.models  import DmsSurvey
from dms.survey.models  import DmsSurveyInput
from dms.survey.models  import DmsSurveyText

# -----------------------------------------------------
def has_user_answered(survey_container, user_id):
  """ liefert True, falls Daten schon existieren, sonst False """
  items = DmsSurvey.objects.filter(survey=survey_container.item).filter(pers_id=user_id)
  if len(items) >= 1:
    return True
  else:
    return False

# -----------------------------------------------------
def create_survey(survey_container, pers_id):
  """ legt einen neuen Antwortkomplex an """
  self = DmsSurvey()
  self.survey = survey_container.item
  self.pers_id = pers_id
  self.last_modified = get_last_modified()
  self.save()
  return self

# -----------------------------------------------------
def get_survey_by_user_id(survey_container, user_id):
  """ liefert das Hauptelement der Antworten """
  return DmsSurvey.objects.filter(survey=survey_container.item).filter(pers_id=user_id)[0].value

# -----------------------------------------------------
def get_survey_answer(survey_container, pers_id, question_id):
  """ liefert die Antwort von pers_id zu question_id """
  items = DmsSurveyInput.objects.filter(survey=survey_container.item).filter(question_id=question_id).\
            filter(pers_id=pers_id)
  if len(items) > 0:
    return items[0]
  else:
    return None

# -----------------------------------------------------
def get_survey_answers(survey_container, question_id, value):
  """ liefert die Antwort Typ value zu question_id """
  return DmsSurveyInput.objects.filter(survey=survey_container.item).filter(question_id=question_id).\
            filter(value=value).order_by('pers_id')

# -----------------------------------------------------
def save_input(survey_container, question_container, pers_id, value):
  """ speichert value fuer den Fragebogen zur entsprechenden Frage """
  this_item = DmsSurveyInput()
  this_item.survey = survey_container.item
  this_item.question_id = question_container.item.id
  this_item.pers_id = pers_id
  this_item.value = value
  this_item.save()
  return this_item

# -----------------------------------------------------
def save_text(survey_container, question_container, pers_id, value):
  """ speichert value als Text fuer den Fragebogen zur entsprechenden Frage """
  this_item = DmsSurveyText()
  this_item.survey = survey_container.item
  this_item.question_id = question_container.item.id
  this_item.pers_id = pers_id
  this_item.value = value
  this_item.save()
  return this_item

# -----------------------------------------------------
def delete_data(survey_container, user_id):
  """ loescht die entsprechenden Antworten (von Checkboxen) """
  DmsSurveyInput.objects.filter(survey=survey_container.item).filter(pers_id=user_id).delete()
  DmsSurveyText.objects.filter(survey=survey_container.item).filter(pers_id=user_id).delete()

# -----------------------------------------------------
def get_min_user(survey_container):
  """ neue "freie" User-ID anfordern """
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute('SELECT MIN(pers_id) FROM dms_survey WHERE survey_id=' + str(survey_container.item.id))
  row = cursor.fetchone()
  id = row[0]
  if id == None or id > 0:
    id = 0
  return id

# -----------------------------------------------------
def has_email_answered(survey_container, email):
  """ liefert True, falls Daten schon existieren, sonst False """
  items = DmsSurveyInput.objects.filter(survey=survey_container.item).filter(value=email)
  if len(items) >= 1:
    return True
  else:
    return False

# -----------------------------------------------------
def get_survey_by_email(survey_container, question_container, email):
  """ falls Daten von email existieren, wird der betreffende Fragebogen zurueckgegeben """
  items = DmsSurveyInput.objects.filter(survey=survey_container.item).\
                                 filter(question_id=question_container.item.id).\
                                 filter(value=email)
  items = DmsSurvey.objects.filter(id=items[0].survey.id)
  if len(items) > 0:
    return items[0]
  else:
    return None

# -----------------------------------------------------
def get_count(survey_container):
  """ liefert die Anzahl der Frageboegen """
  return DmsSurvey.objects.filter(survey=survey_container.item).count()

# -----------------------------------------------------
def get_all_surveys(survey_container):
  """ liefert alle teilnehmenden Personen des Fragebogens """
  return DmsSurvey.objects.filter(survey=survey_container.item).order_by('-last_modified')

# -----------------------------------------------------
def get_inputs_by_person(survey, pers_id):
  """ liefert alle Input-Felder des Fragebogens """
  return DmsSurveyInput.objects.filter(survey=survey).filter(pers_id=pers_id)

# -----------------------------------------------------
def get_input_by_person_question(survey_container, pers_id, question):
  """ liefert das entsprechende Input-Felder des Fragebogens der betreffenden Person """
  items = DmsSurveyInput.objects.filter(survey=survey_container.item).filter(pers_id=pers_id).\
               filter(question_id=question.item.id)
  if len(items) >= 1:
    return items[0].value
  else:
    return ''

# -----------------------------------------------------
def get_texts_by_person(survey, pers_id):
  """ liefert alle Input-Felder des Fragebogens """
  return DmsSurveyText.objects.filter(survey=survey).filter(pers_id=pers_id)

def get_text_by_person_question(survey_container, pers_id, question_id):
  """ liefert Text-Feld des Fragebogens """
  items = DmsSurveyText.objects.filter(survey=survey_container.item).filter(pers_id=pers_id).\
               filter(question_id=question_id)
  if len(items) >= 1:
    return items[0].value
  else:
    return ''

# -----------------------------------------------------
@transaction.commit_manually
def delete_complete(survey_container):
  """ loescht alle Eingabedaten """
  survey_items = DmsSurvey.objects.filter(survey=survey_container.item)
  for survey_item in survey_items:
    DmsSurveyInput.objects.filter(survey=survey_container).delete()
    DmsSurveyText.objects.filter(survey=survey_container).delete()
  survey_items.delete()
  transaction.commit()

# -----------------------------------------------------
def get_survey_id(survey_container):
  """ liefert die ID des Fragebogens """
  return DmsSurvey.objects.get(item=survey_container.item).id

# -----------------------------------------------------
def count_inputs_by_name(survey_container, question_container, value):
  """ liefert alle Input-Felder des Fragebogens """
  return DmsSurveyInput.objects.filter(survey=survey_container.item).\
                                filter(question_id=question_container.item.id).\
                                filter(value=value).count()

def count_inputs_by_name_pers_id(survey_container, question_container, value, pers_id):
  """ liefert die Input-Felder des Fragebogens einer einzelnen Person """
  return DmsSurveyInput.objects.filter(survey=survey_container.item).\
                                filter(question_id=question_container.item.id).\
                                filter(pers_id=pers_id).\
                                filter(value=value).count()

