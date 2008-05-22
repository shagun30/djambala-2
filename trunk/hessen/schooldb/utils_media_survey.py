# -*- coding: utf-8 -*-
"""
/dms/hessen/schooldb/utils_media_survey.py

.. wertet den Medienfragebogen hessischer Schulen aus
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.04.2008  Beginn der Arbeit
0.02  28.04.2008  Einsatz-Optionen
"""

import csv
import datetime
import types
import string
from dms.csv_unicode      import UnicodeWriter

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from dms.roles          import require_permission

from dms.queries        import get_mediasurvey_gruppe_form_count
from dms.queries        import get_mediasurvey_gruppe_form

from dms.mediasurvey.utils    import  get_data_by_org_id
from dms.mediasurvey.models   import  DmsMediaSurvey
from dms.mediasurvey.models   import  DmsMediaSurvey_gruppe
from dms.mediasurvey.models   import  DmsMediaSurvey_option
from dms.mediasurvey.models   import  DmsMediaSurvey_gruppe_form
from dms.mediasurvey.models   import  DmsMediaSurvey_items

from dms.encode_decode    import decode_html
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def show_media_survey_csv(request, item_container, schools):
  """ zeigt Suchformular für Schul-Datenbank """

  n_faecher = get_mediasurvey_gruppe_form_count('fach')
  n_berufsfelder = get_mediasurvey_gruppe_form_count('berufsfeld')
  n_landeslizenzen = get_mediasurvey_gruppe_form_count('landeslizenz')

  # -----------------------------------------------------
  def get_gruppe_form_list(gruppe):
    """ """
    items = get_mediasurvey_gruppe_form(gruppe)
    ret = []
    for item in items:
      ret.append( (item.form, item.title) )
    return ret

  # -----------------------------------------------------
  def get_option_list(gruppe):
    """ """
    items = get_mediasurvey_option(gruppe)
    ret = []
    for item in items:
      ret.append( (item.option, item.title) )
    return ret

  # -----------------------------------------------------
  def get_gruppe_items(gruppe):
    """ """
    return get_mediasurvey_gruppe_form(gruppe)

  # -----------------------------------------------------
  def get_ja_nein_choices(id=1):
    """ """
    ret = []
    ret.append( (1, 'ja') )
    ret.append( (0, 'nein') )
    return ret
  # -----------------------------------------------------
  def get_nutzung_choices():
    ret = []
    for i in xrange(5):
      ret.append( (i*25, smart_unicode(i*25)+ '%' ) )
    return ret

  # -----------------------------------------------------
  def get_var_list(var_name, n_count):
    """ baut eine Liste mit Variablennamen zusammen """
    var_list = []
    for n in xrange(n_count):
      var_list.append(var_name + '_%02i' % n)
    return var_list

  # -----------------------------------------------------
  def get_var_list_items(var_name, items):
    """ baut eine Liste mit Variablennamen zusammen """
    var_list = []
    for n in xrange(len(items)):
      var_list.append((var_name + '_%02i' % n, items[n].title))
    return var_list

  # -----------------------------------------------------
  def get_var_checkbox_list(var_name, n_count, opts):
    """ baut eine Liste mit Variablennamen zusammen """
    var_list = []
    for n in xrange(n_count):
      var_list.append(var_name + '_%02i' % n)
    return var_list

  def get_header(name, cols, description='', length=20):
    if description != '':
      return { 'name': name, 'cols': cols, 'description': description[:length] }
    else:
      return { 'name': name, 'cols': cols }

  faecher = get_gruppe_items('fach')
  berufsfelder = get_gruppe_items('berufsfeld')
  landeslizenzen = get_gruppe_items('landeslizenz')
  schwerpunkt_opts = []
  for n in xrange(6):
    opt = 'opt_schwerpunkt_%02i' % n
    schwerpunkt_opts.append(opt)

  def get_headers():
    """ Uberschriften zusammenbauen """
    headers = []
    headers.append(get_header('eigene_com', 1))
    # 1.1
    headers.append(get_header('raeume_gesamt', 1))
    headers.append(get_header('mit_com_pcraum', 1))
    headers.append(get_header('ohne_com_pcraum', 1))
    headers.append(get_header('anz_com_pcraum', 1))
    headers.append(get_header('mit_com_fachraum', 1))
    headers.append(get_header('ohne_com_fachraum', 1))
    headers.append(get_header('anz_com_fachraum', 1))
    headers.append(get_header('nutzung_sch_com', 1))
    gruppe = get_gruppe_form_list('nutzung_raum_com')
    headers.append((get_header('nutzung_raum_com', len(gruppe)), gruppe))
    # 1.2
    headers.append(get_header('typ_1', 1))
    headers.append(get_header('typ_1_mobil', 1))
    headers.append(get_header('typ_2', 1))
    headers.append(get_header('typ_2_mobil', 1))
    headers.append(get_header('notebook', 1))
    headers.append(get_header('notebook_klasse', 1))
    # 1.3
    gruppe = get_gruppe_form_list('peripherie')
    headers.append((get_header('peripherie', len(gruppe)), gruppe))
    # 1.4
    gruppe = get_gruppe_form_list('software')
    headers.append((get_header('software', len(gruppe)), gruppe))
    # 1.5
    gruppe = get_gruppe_form_list('lernplattform')
    headers.append((get_header('lernplattform', len(gruppe)), gruppe))
    headers.append(get_header('eigene_plattform', 1))
    # 2
    headers.append(get_header('netz', 1))
    gruppe = get_gruppe_form_list('netz_bs')
    headers.append((get_header('netz_bs', len(gruppe)), gruppe))
    headers.append(get_header('netz_com', 1))
    headers.append(get_header('netz_wlan', 1))
    headers.append(get_header('netz_raum', 1))
    # 3
    headers.append(get_header('internet', 1))
    gruppe = get_gruppe_form_list('internet_art')
    headers.append((get_header('internet_art', len(gruppe)), gruppe))
    headers.append(get_header('internet_anz', 1))
    # 4.1
    gruppe = get_var_list_items('com_einsatz', faecher) # com_einsatz
    headers.append((get_header('com_einsatz', len(gruppe)), gruppe))
    gruppe = get_var_list_items('com_einsatz_bf', berufsfelder) # com_einsatz_bf
    headers.append((get_header('com_einsatz_bf', len(gruppe)), gruppe))
    # 4.2
    headers.append(get_header('com_beruf', 1))
    headers.append(get_header('com_foerder', 1))
    # 4.3
    gruppe = get_var_list_items('int_einsatz', faecher) # int_einsatz
    headers.append((get_header('int_einsatz', len(gruppe)), gruppe))
    gruppe = get_var_list_items('int_einsatz_bf', berufsfelder) # int_einsatz_bf
    headers.append((get_header('int_einsatz_bf', len(gruppe)), gruppe))
    # 4.4
    headers.append(get_header('int_website', 1))
    gruppe = get_gruppe_form_list('interaktion')
    headers.append((get_header('interaktion', len(gruppe)), gruppe))
    # 4.5
    group = DmsMediaSurvey_gruppe.objects.get(gruppe='opt_schwerpunkt')
    n = 0
    for fach in faecher:
      name = '%s_%02i' % ('einsatz', n)
      for j in xrange(4):
        option = DmsMediaSurvey_option.objects.filter(gruppe=group).get(option='opt_schwerpunkt_0%i' %j)
        headers.append(get_header(name, 1, '%s:\n%s' % (fach.title, option.title[:20]), 40))
      n += 1
    n = 0
    for berufsfeld in berufsfelder:
      name = '%s_%02i' % ('einsatz_bf', n)
      for j in xrange(4):
        option = DmsMediaSurvey_option.objects.filter(gruppe=group).get(option='opt_schwerpunkt_0%i' %j)
        headers.append(get_header(name, 1, '%s:\n%s' % (berufsfeld.title, option.title[:20]), 40))
      n += 1
    #4.6
    gruppe = get_var_list_items('landeslizenz', landeslizenzen) # landeslizenz
    headers.append((get_header('landeslizenz', len(gruppe)), gruppe))
    # 4.7
    gruppe = get_gruppe_form_list('unterstuetzung')
    headers.append((get_header('unterstuetzung', len(gruppe)), gruppe))
    # 4.8
    gruppe = get_gruppe_form_list('fortbildung')
    headers.append((get_header('fortbildung', len(gruppe)), gruppe))
    gruppe = get_gruppe_form_list('fortbildung_k')
    headers.append((get_header('fortbildung_k', len(gruppe)), gruppe))
    # 4.9
    headers.append(get_header('nutzung', 1))
    return headers

  def get_titles(headers):
    """ """
    titles = []
    for header in headers:
      if type(header) == types.DictType:
        if header.has_key('description'):
          titles.append(header['description'])
        else:
          titles.append(header['name'])
      else:
        name = header[0]['name']
        #titles.append(name)
        for item in header[1]:
          titles.append('%s:\n%s' % ( name, decode_html(item[1])[:20]) )
    return titles

  def get_data(school, headers):
    """ """
    str_values = []
    for header in headers:
      if type(header) == types.DictType:
        key = header['name']
        value = school[key]
        if type(value) == types.ListType:
          if value != []:
            arr = string.splitfields(header['description'], '\n')
            this_option = arr[1]
            for v in value:
              option = DmsMediaSurvey_option.objects.get(option=v)
              is_set = False
              if option.title == this_option:
                is_set = True
                break
            if is_set:
              values.append(u'1')
            else:
              values.append(u'-')
          else:
            values.append(u'-')
        else:
          values.append(unicode(value))
      else:
        main_key = header[0]['name']
        if school.has_key(main_key):
          this_values = school[main_key]
        else:
          this_values = []
        if this_values == [] and school.has_key(main_key+'_00'):
          for item in header[1]:
            if school.has_key(item[0]):
              value = school[item[0]]
              option = DmsMediaSurvey_option.objects.get(option=value)
              values.append(unicode(decode_html(option.title)[:20]))
            else:
              values.append('-')
        else:
          for item in header[1]:
            if item[0] in this_values:
              value = '1'
              values.append(unicode(value))
            else:
              values.append('0')
    return str_values

  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=%s.csv' % item_container.item.name
  writer = UnicodeWriter(response, quoting=csv.QUOTE_ALL, delimiter=';')

  writer.writerow([_('Ergebnisse des Medienfragebogens'), 
                   datetime.datetime.now().strftime('%d.%m.%Y %H:%M')])
  writer.writerow([])
  headers = get_headers()
  titles = get_titles(headers)
  writer.writerow([ header for header in [_('Schulname'), _('Schulort'), _('Schul-Nr')] + titles ])
  for school in schools:
    org_id = school[0].Schul_Nr
    data = get_data_by_org_id(request, item_container, org_id)
    values = []
    values.append(school[0].NameSchule)
    values.append(school[1].Ort)
    values.append(unicode(org_id))
    if data['hat_daten']:
      values += get_data(data, headers)
    writer.writerow([ value for value in values ])
  return response
