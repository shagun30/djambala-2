# -*- coding: utf-8 -*-
"""
/dms/exercise/views_add.py

.. enthaelt den View zum Ergaenzen einer Aufgabe
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.05.2008  Beginn der Arbeit
0.02  07.05.2008  Aufgabe: 1..
0.03  09.05.2008  Punktzahl
0.04  15.05.2008  Uebernahme aus Lernarchiven
"""

import datetime

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import save_container_values
from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import count_item_container_children_by_app
from dms.queries        import get_app
from dms.queries        import save_item_values
from dms.queries        import get_item_container_by_url

from dms.roles          import *
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.utils_base         import convert_str_to_date
from dms.utils_form     import get_folderish_vars_add

from dms.file.utils     import save_file
from dms.mail           import send_control_email
from dms.edufolder.utils  import do_copy

from dms.exercise.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def exercise_add(request, item_container):
  """ neue Aufgabe anlegen """

  def save_values(request, name, new, files, item_container):
    """ Daten sichern """
    try:
      fname = check_name(files['fname']['filename'], True)
    except:
      fname = ''
    new['nav_title'] = new['title']
    new['sections'] = _(u'Aufgabe\nLösungen\nMusterlösung\n')
    community_id = 0
    schulverbund_id = 0
    new['is_exchangeable'] = item_container.item.is_exchangeable
    new['is_browseable'] = True
    new['has_usersupport'] = True
    edu_ic = None
    if new.has_key('string_2') and new['string_2'].strip() != '':
      url = new['string_2'].strip()
      edu_ic = get_item_container_by_url(url)
      if edu_ic != None:
        if edu_ic.item.app.name != 'dmsEduExerciseItem':
          return
        item_container_new = do_copy(request, edu_ic, item_container)
        item_container_new.item.app = get_app('dmsExercise') # !!!!!
        item_container_new.item.save()
        if new.has_key('title') and new['title'].strip() == '':
          item_container_new.title = new['title'].strip()
        if new.has_key('nav_title') and new['nav_title'].strip() == '':
          item_container_new.nav_title = new['nav_title'].strip()
        item_container_new.visible_start = convert_str_to_date(new['visible_start'])
        item_container_new.visible_end = convert_str_to_date(new['visible_end'])
        item_container_new.save()
    # --- muss explizit gesetzt werden
    if edu_ic == None:
      item_container_new = save_container_values(request.user, 'dmsExercise', name, new, item_container)
      if fname != '':
        save_file(fname, files, item_container_new)
        new['string_1'] = new['text'] = u''
        new['section'] = _(u'Aufgabe')
        new['integer_1'] = -1
        save_item_values(request.user, 'dmsFile', fname, new, item_container_new, True)
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    string_2   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    title     = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text      = forms.CharField(required=False,
                     widget=forms.Textarea(attrs={'rows':12, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    fname     = forms.CharField(required=False, max_length=200,
                      widget=forms.FileInput(attrs={'size':40}) )
    integer_1 = forms.IntegerField(min_value=-1, max_value=100,
                            widget=forms.TextInput(attrs={'size':5}) )
    string_1  = forms.CharField(required=False,
                     widget=forms.Textarea(attrs={'rows':5, 'cols':10,}) )
    section   = forms.CharField(required=False,
                      widget=forms.Select(choices=get_section_choices(item_container.container.sections),
                                          attrs={'size':4, 'style':'width:40%'} ) )
    visible_start = forms.DateField(input_formats=['%d.%m.%Y'],
                          widget=forms.TextInput(attrs={'size':10}))
    visible_end   = forms.DateField(input_formats=['%d.%m.%Y'],
                          widget=forms.TextInput(attrs={'size':10}))
    license       = forms.ChoiceField(choices=get_license_choices(item_container),
                          widget=forms.RadioSelect() )

  app_name = 'exercise'
  my_title = _(u'Aufgabe anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else:
    n_exercises = 1 + count_item_container_children_by_app(item_container, get_app('dmsExercise'))
    data = { 'title': '%s %i' % (_('Aufgabe'), n_exercises),
             'integer_1': 0,
             'string_1': '1:\n2:\n3:\n4:\n5:\n',
             'visible_start': datetime.datetime.now().strftime('%d.%m.%Y'),
             'visible_end': (datetime.datetime.now() + datetime.timedelta(2)).strftime('%d.%m.%Y'),
             'license': 1,
           }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base_2', [ 'string_2', 'section']),
           ('tab_base'  , ['title', 'text', 'fname', 'integer_1', 'string_1', 
                           'visible_start', 'visible_end',]),
           ('tab_license',[ 'license', ] ),
          ]
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = f.data['title'].strip().lower()
    name = check_name(name, True)
    if not exist_item(item_container, name):
      save_values(request, name, f.data, request.FILES, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else:
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response ( 'app/file/manage_edit.html', vars )
