# -*- coding: utf-8 -*-
"""
/dms/survey/views_export.py

.. enthaelt den View zum Exportieren der Ergebnisse des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.01.2008  Beginn der Arbeit
"""

import csv
import datetime
import types

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from dms.roles            import *

from dms.survey.queries   import get_all_surveys
from dms.survey.queries   import get_inputs_by_person
from dms.survey.queries   import get_texts_by_person

from dms.folder.utils     import get_folder_content
from dms.csv_unicode      import UnicodeWriter
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def survey_export_csv(request, item_container):
  """ Ergebnisse des Fragebogens im CSV-Format exportieren, Rezept 144 aus Django-Snippets """

  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=%s.csv' % item_container.item.name
  writer = UnicodeWriter(response, quoting=csv.QUOTE_ALL, delimiter=';')

  ics, sections, d_sections = get_folder_content(item_container, False, ['dmsSurveyItem'])
  writer.writerow([item_container.item.title, datetime.datetime.now().strftime('%d.%m.%Y %H:%M')])
  writer.writerow([])
  headers = []
  for ic in ics:
    if ic.item.string_1 in ['input', 'text', 'radio']:
      headers.append(ic.item.title[:30])
    else:
      headers.append(ic.item.title)
      keys = string.splitfields(ic.item.text.strip().replace('<p>','').replace('</p>',''), '\n')
      for key in keys:
        key = key.strip()
        if key != '':
          headers.append('.. ' + key[:30])
  # Write the header of the CSV file
  writer.writerow([ header for header in headers ])

  # Write all rows of the CSV file
  surveys = get_all_surveys(item_container)
  for survey in surveys:
    inputs = get_inputs_by_person(survey.survey, survey.pers_id)
    texts = get_texts_by_person(survey.survey, survey.pers_id)
    data = {}
    for input in inputs:
      id = input.question_id
      if data.has_key(id):
        if type(data[id]) == types.ListType:
          data[id] = data[id].append(input.value)
        else:
          data[id] = [data[id], input.value]
      else:
        data[id] = input.value
    for text in texts:
      data[text.question_id] = text.value
    values = []
    for ic in ics:
      if ic.item.string_1 in ['input', 'text', 'radio']:
        if data.has_key(ic.item.id):
          values.append(data[ic.item.id])
        else:
          values.append('')
      else:
        values.append('')
        id = ic.item.id
        if data.has_key(ic.item.id) and type(data[ic.item.id]) != types.ListType:
          data[id] = [data[id]]
        keys = string.splitfields(ic.item.text.strip().replace('<p>','').replace('</p>',''), '\n')
        for key in keys:
          key = key.strip()
          if key != '':
            if data.has_key(id) and key in data[id]:
              values.append('1')
            else:
              values.append('0')
        #assert False
    # Datenzeile schreiben
    writer.writerow([ value for value in values ])
  return response

