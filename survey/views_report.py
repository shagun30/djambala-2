# -*- coding: utf-8 -*-
"""
/dms/survey/views_report.py

.. enthaelt den View zur Auswertung der Ergebnisse des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.01.2008  Beginn der Arbeit
"""

import csv
import datetime
import types
import string

from django.http import HttpResponse
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _

from dms.roles            import require_permission
from dms.roles            import UserEditPerms

from dms.utils_form       import get_folderish_vars_show

from dms.survey.queries   import get_count
from dms.survey.queries   import count_inputs_by_name
from dms.survey.queries   import get_survey_id

from dms.survey.utils     import get_admin_options
from dms.folder.utils     import get_folder_content
from dms.csv_unicode      import UnicodeWriter
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def survey_report(request, item_container):
  """ Ergebnisse des Fragebogens auswerten """

  def get_report(item_container, ics, sections, d_sections):
    """ erzeugt die Auswertungsseite """
    t_header = get_template('app/survey/report_header.html')
    t_question = get_template('app/survey/report_question.html')
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
        if form_type in ['radio', 'checkbox']:
          options_str = ic.item.text.replace('<p>', '').replace('</p>', '')
          options = string.splitfields(options_str, '\n')
          data = []
          for option in options:
            option = option.strip()
            if option != '':
              item_count = count_inputs_by_name(item_container, ic, option)
              p = 100.0*item_count/count
              p0 = int(p/3)
              p1 = int((100.0 - p)/3)
              visual = '*'*p0 + ' '*p1
              data.append({'option': option, 'count': item_count, 'percent': '%5.1f' % p, 'visual': visual} )
      content += t_question.render(Context({
                                             'id': ic.item.id,
                                             'header': ic.item.title,
                                             'question': ic.item.sub_title,
                                             'is_input': form_type == 'input',
                                             'is_text': form_type == 'text',
                                             'data': data,
                                           }))
    return content

  app_name = 'survey'
  ics, sections, d_sections = get_folder_content(item_container, False, ['dmsSurveyItem'])
  user_perms = UserEditPerms(request.user.username, request.path)
  vars = get_folderish_vars_show(request, item_container, app_name, '',
                                  get_admin_options(item_container, user_perms))
  vars['text_bottom'] = get_report(item_container, ics, sections, d_sections)
  vars['user_support_header'] = _('Steuerung')
  return render_to_response('app/survey/report.html', vars)

