# -*- coding: utf-8 -*-
"""
/dms/text/views_show.py

.. enthaelt den View zum Ergaenzen einer Textseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.05.2007  Beginn der Arbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import save_item_values
from dms.queries        import exist_item
from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_add

from dms.views_error    import show_error_object_exist

from dms.text.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def text_add(request, item_container):
  """ neue Infoseite anlegen """

  def save_values(name, new, my_folder):
    """ Daten sichern """
    save_item_values(request.user, 'dmsText', name, new, my_folder, False, False)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name       = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':20, 'cols':60, 'style':'width:100%;'}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                       attrs={'size':4, 'style':'width:40%'} ) )
    is_browseable = forms.BooleanField(required=False)
    license         = forms.ChoiceField(choices=get_license_choices(item_container),
                                        widget=forms.RadioSelect() )

  app_name = 'text'
  my_title = _(u'Textseite anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'text': '', 'license': 1,}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base', [ 'name', 'title', 'text', 'section', 'is_browseable' ]),
           ( 'tab_license',    [ 'license', ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not name.endswith('.txt'):
      name += '.txt'
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response('app/base_edit.html', vars)
