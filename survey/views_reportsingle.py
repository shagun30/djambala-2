# -*- coding: utf-8 -*-
"""
/dms/survey/views_reportsingle.py

.. enthaelt den View zur Auswertung von Einzelergebnissen des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  25.02.2008  Beginn der Arbeit
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

from dms.utils_form       import get_folderish_vars_show

from dms.survey.queries   import get_count
from dms.survey.queries   import count_inputs_by_name
from dms.survey.queries   import count_inputs_by_name_pers_id
from dms.survey.queries   import get_survey_id
from dms.survey.queries   import get_all_surveys
from dms.survey.queries   import get_texts_by_person
from dms.survey.queries   import get_text_by_person_question
from dms.survey.queries   import get_input_by_person_question

from dms.survey.utils     import get_admin_options
from dms.folder.utils     import get_folder_content
from dms.csv_unicode      import UnicodeWriter
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def survey_reportsingle(request, item_container):
  """ Einzelergebnisse des Fragebogens auswerten """

  def get_report(item_container, ics, sections, d_sections, pers_id):
    """ erzeugt die Auswertungsseite """
    t_header = get_template('app/survey/report_header.html')
    t_question = get_template('app/survey/reportsingle_question.html')
    content = ''
    section = ''
    data = {}
    count = get_count(item_container)
    for ic in ics:
      if section != ic.section:
        section = ic.section
        content += t_header.render(Context({'header': ic.item.title,}))
      results = ''
      form_type = ic.item.string_1
      if count > 0:
        this_input = this_text = ''
        if form_type in ['radio', 'checkbox']:
          options_str = ic.item.text.replace('<p>', '').replace('</p>', '')
          options = string.splitfields(options_str, '\n')
          data = []
          for option in options:
            option = option.strip()
            if option != '':
              item_count = count_inputs_by_name_pers_id(item_container, ic, option, pers_id)
              p = 100.0*item_count/count
              p0 = int(p/3)
              p1 = int((100.0 - p)/3)
              visual = '*'*p0 + ' '*p1
              data.append({'option': option, 'count': item_count, 
                           'percent': '%5.1f' % p, 'visual': visual} )
        elif form_type == 'text':
          this_text = get_text_by_person_question(item_container, pers_id, ic.item.id).\
                          replace('\n', '<br />\n')
          if this_text == '':
            this_text = _(u'Ohne Antwort')
        elif form_type == 'input':
          this_input = get_input_by_person_question(item_container, pers_id, ic)
          if this_text == '':
            this_text = _(u'Ohne Antwort')
      content += t_question.render(Context({
                                             'id': ic.item.id,
                                             'header': ic.item.title,
                                             'question': ic.item.sub_title,
                                             'this_input': mark_safe(this_text),
                                             'this_text': mark_safe(this_text),
                                             'data': data,
                                           }))
    return content

  def get_users(item_container):
    """ liefert die Personen, die den Fragebogen ausgefuellt haben """
    survey_users = get_all_surveys(item_container)
    users = []
    for user in survey_users:
      if user.pers_id < 0:
        users.append({'pers_name': user.pers_id, 'pers_id': user.pers_id})
      else:
        users.append({'pers_name': get_user_by_id(user.pers_id).get_full_name(), 
                      'pers_id': user.pers_id})
    return users

  app_name = 'survey'
  user_perms = UserEditPerms(request.user.username, request.path)
  vars = get_folderish_vars_show(request, item_container, app_name, '',
                                  get_admin_options(item_container, user_perms))
  vars['user_support_header'] = _('Steuerung')
  if request.GET.has_key('show_user_survey'):
    pers_id = int(request.GET['show_user_survey'])
    ics, sections, d_sections = get_folder_content(item_container, False, ['dmsSurveyItem'])
    vars['text_bottom'] = get_report(item_container, ics, sections, d_sections, pers_id)
    return render_to_response('app/survey/reportsingle.html', vars)
  else:
    vars['text'] = ''
    vars['text_more'] = ''
    vars['survey_users'] = get_users(item_container)
    return render_to_response('app/survey/reportsingle.html', vars)

