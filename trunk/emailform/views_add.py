# -*- coding: utf-8 -*-
"""
/dms/emailform/views_add.py

.. enthaelt den View zum Ergaenzen eines Email-Formulars
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  06.11.2007  Beginn der Arbeit
0.02  07.11.2007  Ziel-E-Mail
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import save_container_values
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

from dms.emailform.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def emailform_add(request, item_container):
  """ neues Email-Formular anlegen """

  parent_app = get_parent_app(item_container)

  def save_values(name, new, item_container):
    """ Daten sichern """
    save_container_values(request.user, 'dmsEmailForm', name, new, item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name       = forms.CharField(max_length=60,
         widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(max_length=240,
         widget=forms.TextInput(attrs={'size':60}) )
    nav_title=forms.CharField(required=False, max_length=60,
                    widget=forms.TextInput(attrs={'size':30}) )
    string_1   = forms.CharField(max_length=120,
         widget=forms.TextInput(attrs={'size':60}) )
    url_more   = forms.CharField(max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
         get_section_choices(item_container.container.sections),
                       attrs={'size':4, 'style':'width:40%'} ) )
    sections =forms.CharField(required=False,
                    widget=forms.Textarea( attrs={'rows':5, 'cols':40, 'style':'width:50%;'}) )

  app_name = 'emailform'
  my_title = _(u'E-Mail-Formular anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialisiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'sections': _(u'Allgemeine Angaben'), }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base', [ 'name', 'title', 'nav_title', 'url_more', 'string_1', 'text',
                          'section', 'sections', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name, my_title,
                                  content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
