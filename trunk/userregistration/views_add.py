# -*- coding: utf-8 -*-
"""
/dms/userregistration/views_add.py

.. enthaelt den View zur Registrierung der User
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.06.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.encode_decode  import decode_html
from dms.queries        import exist_item
from dms.queries        import save_item_values
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_form     import get_item_vars_add
from dms.views_error    import show_error_object_exist

from dms.roles          import require_permission

from dms.userregistration.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def userregistration_add(request, item_container):
  """ Registrierung der Community-Mitglieder """

  def save_values(name, new, item_container):
    """ legt das User-Data-Objekt an """
    save_item_values(request.user, 'dmsUserRegistration', name,
                     new, item_container, True, False)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name       = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':30}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    sub_title  = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                       attrs={'size':4, 'style':'width:40%'} ) )

  app_name = 'userregistration'
  my_title = _(u'Registrierung von Community-Mitgliedern')

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'name': 'user_registration',
            'title': decode_html(_(u'Registrierung der Community-Mitglieder'))}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base', [ 'name', 'title', 'section', ]) ]
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
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response('app/base_edit.html', vars)
