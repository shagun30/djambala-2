# -*- coding: utf-8 -*-
"""
/dms/exercisefolder/views_add.py

.. enthaelt den View zum Ergaenzen einer Aufgabendatenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
0.02  03.05.2008  get_step_choices
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import save_container_values
from dms.queries        import exist_item
from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_form     import get_folderish_vars_add

from dms.exercisefolder.utils       import get_step_choices
from dms.exercisefolder.utils       import get_template_choices
from dms.exercisefolder.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def exercisefolder_add(request, item_container):
  """ neue Aufgabendatenbank anlegen """

  def save_values(name, new, item_container):
    """ Daten sichern """
    save_container_values(request.user, 'dmsExerciseFolder', name, new, item_container)
    # Korrektur der Breadcrumb-Leiste
    if new['integer_1'] == 0:
      item_container.container.is_top_folder = True
      item_container.conatiner.save()

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    name      = forms.CharField(max_length=60,
          widget=forms.TextInput(attrs={'size':20}) )
    title     = forms.CharField(max_length=240,
          widget=forms.TextInput(attrs={'size':60}) )
    nav_title = forms.CharField(required=False, max_length=60,
          widget=forms.TextInput(attrs={'size':30}) )
    integer_1 = forms.CharField(widget=forms.Select(choices=get_template_choices(),
                      attrs={'size':2, 'style':'width:60%'} ) )
    if item_container.item.app.name == 'dmsExerciseFolder':
      integer_2 = forms.CharField(widget=forms.Select(choices=get_step_choices(item_container.item.integer_2),
                      attrs={'size':4, 'style':'width:60%'} ) )
    else:
      integer_2 = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'value':0}) )
      section   = forms.CharField(required=False, 
                        widget=forms.Select(choices=get_section_choices(
                                     item_container.container.sections), attrs={'size':4, 'style':'width:40%'} ) )

  app_name = 'exercisefolder'
  my_title = _(u'Aufgabensammlung anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else :
    # --- Bild vom Eltern-Lernarchiv uebernehmen
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  if item_container.item.app.name == 'dmsExerciseFolder':
    tabs = [('tab_base',['name', 'title', 'nav_title', 'integer_1', 'integer_2' ]), ]
  else:
    tabs = [('tab_base',['name', 'title', 'nav_title', 'integer_1', 'integer_2', 'section' ]), ]
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else:
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
