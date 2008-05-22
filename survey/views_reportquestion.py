# -*- coding: utf-8 -*-
"""
/dms/survey/views_reportquestion.py

.. enthaelt den View zur Auswertung von Ergebnisse zu einzelnen Fragen des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  26.02.2008  Beginn der Arbeit
"""

import csv
import datetime
import types
import string

from django.http import HttpResponse
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring  import mark_safe
from django.utils.translation import ugettext as _

from dms.roles            import require_permission
from dms.roles            import UserEditPerms

from dms.queries          import get_user_by_id
from dms.queries          import get_item_by_id

from dms.utils_form       import get_folderish_vars_show

from dms.survey.queries   import get_count
from dms.survey.queries   import count_inputs_by_name
from dms.survey.queries   import count_inputs_by_name_pers_id
from dms.survey.queries   import get_survey_id
from dms.survey.queries   import get_all_surveys
from dms.survey.queries   import get_texts_by_person
from dms.survey.queries   import get_text_by_person_question
from dms.survey.queries   import get_input_by_person_question
from dms.survey.queries   import get_survey_answer
from dms.survey.queries   import get_survey_answers

from dms.survey.utils     import get_admin_options
from dms.folder.utils     import get_folder_content
from dms.csv_unicode      import UnicodeWriter
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def survey_reportquestion(request, item_container):
  """ Einzelergebnisse des Fragebogens auswerten """

  def get_report(item_container, question_id):
    """ erzeugt die Auswertungsseite """
    users = get_all_surveys(item_container)
    question = get_item_by_id(question_id)
    form_type = question.string_1
    if form_type in ['radio', 'checkbox']:
      t_question = get_template('app/survey/reportquestion_pers.html')
      options_str = question.text.replace('<p>', '').replace('</p>', '')
      options = string.splitfields(options_str, '\n')
      answers = []
      for option in options:
        items = get_survey_answers(item_container, question_id, option.strip())
        users = ''
        for item in items:
          if users != '':
            users += ', '
          p = item.pers_id
          try:
            users += get_user_by_id(item.pers_id).get_full_name()
          except:
            users += str(item.pers_id)
        answers.append({ 'value': option, 'names': mark_safe(users) })
      return t_question.render(Context({ 'header': question.title,
                                         'question': question.sub_title,
                                         'options': options,
                                         'answers': answers,
                                       }))
    elif form_type in ['text', 'input']:
      options = []
      answers = []
      t_question = get_template('app/survey/reportquestion_text_pers.html')
      users = get_all_surveys(item_container)
      for user in users:
        if form_type == 'text':
          text = get_text_by_person_question(item_container, user.pers_id, question_id).strip()
        else:
          text = get_input_by_person_question(item_container, user.pers_id, question_id).strip()
        if text != '':
          name = get_user_by_id(user.pers_id).get_full_name()
          answers.append({ 'value': mark_safe(text.replace('\n', '<br />')),
                           'name': mark_safe(name) })
      return t_question.render(Context({ 'header': question.title,
                                         'question': question.sub_title,
                                         'options': options,
                                         'answers': answers,
                                       }))

  def get_questions(ics):
    """ liefert die Fragen des Fragebogens """
    questions = []
    for ic in ics:
      questions. append( {'id': ic.item.id, 'header': ic.item.title, 'question': ic.item.sub_title} )
    return questions

  app_name = 'survey'
  user_perms = UserEditPerms(request.user.username, request.path)
  vars = get_folderish_vars_show(request, item_container, app_name, '',
                                  get_admin_options(item_container, user_perms))
  vars['user_support_header'] = _('Steuerung')
  vars['text'] = ''
  vars['text_more'] = ''
  if request.GET.has_key('show_question_survey'):
    question_id = int(request.GET['show_question_survey'])
    vars['answers'] = get_report(item_container, question_id)
    return render_to_response('app/survey/reportquestion.html', vars)
  else:
    ics, sections, d_sections = get_folder_content(item_container, False, ['dmsSurveyItem'])
    vars['survey_questions'] = get_questions(ics)
    return render_to_response('app/survey/reportquestion.html', vars)

