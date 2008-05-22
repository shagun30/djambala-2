# -*- coding: utf-8 -*-
"""
/dms/mediasurvey/views_add.py

.. enthaelt den View zum Ergaenzen eines Medien-Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.04.2007  Beginn der Arbeit
"""

import string, datetime

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_app
from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_item_add_actions
from dms.utils_form     import get_folderish_vars_add

from dms.queries        import exist_item
from dms.queries        import save_item_values

from dms.views_error    import show_error_object_exist

from dms.mediasurvey.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def mediasurvey_add(request, item_container):
  """ neuen Medienfragebogen anlegen """

  parent_app = get_parent_app(item_container)

  def save_values(name, new, my_folder):
    """ Daten sichern """
    save_item_values(request.user, 'dmsMediaSurvey', name, new, my_folder, True)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name       = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':12, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                       attrs={'size':4, 'style':'width:40%'} ) )
  app_name = 'mediasurvey'
  my_title = _(u'Medienfragebogen anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'name': 'medien_fragebogen',
             'title': 'Medien-Fragebogen',
           }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base', [ 'name', 'title', 'text', 'section', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], False)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response('app/base_edit.html', vars)
