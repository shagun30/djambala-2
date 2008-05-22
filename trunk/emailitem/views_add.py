# -*- coding: utf-8 -*-
"""
/dms/emailitem/views_add.py

.. enthaelt den View zum Ergaenzen einer Frage
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.01.2007  Beginn der Arbeit
"""

import string
import time
import datetime

from django.utils.encoding  import smart_unicode
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import save_item_values
from dms.queries        import exist_item
from dms.queries        import get_parent_app
from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.utils_form     import get_folderish_vars_add

from dms.views_error    import show_error_object_exist

from dms.surveyitem.utils      import get_yes_no_choices
from dms.emailitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def emailitem_add(request, item_container):
  """ neue Frage anlegen """

  if request.GET.has_key('form_type'):
    form_type = request.GET['form_type']
  else:
    form_type = 'input'

  def save_values(name, new, my_folder):
    """ Daten sichern """
    if new.has_key('text'):
      new['text'] = new['text'].replace('<p>', '').replace('</p>', '')
    save_item_values(request.user, 'dmsEmailItem', name, new, my_folder, True, False)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name       = forms.CharField(required=False, max_length=60,  widget=forms.TextInput(attrs={'size':20}) )
    string_1   = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'value':form_type}) )
    title      = forms.CharField(max_length=240, widget=forms.TextInput(attrs={'size':60}) )
    sub_title  = forms.CharField(required=False, max_length=240, widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':4, 'cols':60, 'style':'width:100%;'}) )
    text_more  = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':4, 'cols':60, 'style':'width:100%;'}) )
    section    = forms.CharField(widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                           attrs={'size':4, 'style':'width:40%'} ) )
    integer_1 = forms.ChoiceField(choices=get_yes_no_choices(), widget=forms.RadioSelect() )
    integer_2 = forms.IntegerField(required=False, min_value=1, max_value=200, widget=forms.TextInput(attrs={'size':5}) )
    integer_3 = forms.IntegerField(required=False, min_value=1, max_value=80, widget=forms.TextInput(attrs={'size':5}) )
    integer_4 = forms.IntegerField(required=False, min_value=20, max_value=60, widget=forms.TextInput(attrs={'size':5}) )
    integer_5 = forms.IntegerField(required=False, min_value=3, max_value=20, widget=forms.TextInput(attrs={'size':5}) )

  app_name = u'emailitem'
  my_title = _(u'Frage anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else:
    if form_type == 'input':
      data = { 'integer_1': 1, 'integer_2': 60, 'integer_3': 40, }
    elif form_type == 'text':
      data = { 'integer_1': 0, 'integer_4': 50, 'integer_5': 5, }
    else:
      data = { 'integer_1': 1, }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  if form_type == 'input':
    tabs = [ ('tab_base', [ 'name', 'string_1', 'title', 'sub_title', 'text_more', 
                            'integer_1', 'integer_2', 'integer_3', 'section', ]), ]
  elif form_type == 'text':
    tabs = [ ('tab_base', [ 'name', 'string_1', 'title', 'sub_title', 'text_more', 
                            'integer_1', 'integer_4', 'integer_5', 'section', ]), ]
  else:
    tabs = [ ('tab_base', [ 'name', 'string_1', 'title', 'sub_title', 'text', 'text_more',
                            'integer_1', 'section', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    now = smart_unicode(time.time())
    if f.data['name'] != '':
      name = check_name(f.data['name'], False)
      if not exist_item(item_container, name):
        save_values(name, f.data, item_container)
      else:
        return show_error_object_exist(request, item_container, name)
    else:
      name = 'question_' + now[:string.find(now, '.')] + '.html'
      save_values(name, f.data, item_container)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_folderish_vars_add(request, item_container, app_name, my_title,
                                  content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
