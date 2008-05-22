# -*- coding: utf-8 -*-
"""
/dms/exercisefile/views_add.py

.. enthaelt den View zum Ergaenzen einer Aufgabendatei
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.05.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.settings       import HOME_PATH

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices, check_name
from dms.utils          import check_name
from dms.utils_form     import get_item_vars_add

from dms.queries        import save_item_values
from dms.queries        import exist_item

from dms.file.utils     import save_file
from dms.exercisefile.help_form import help_form

from dms.views_error    import show_error_object_exist

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def exercisefile_add(request, item_container):
  """ neue Aufgabendatei anlegen """

  def save_values(name, new, files, item_container):
    """ Daten sichern """
    new['section'] = _(u'Lösungen')
    new['integer_1'] = 0
    save_file(name, files, item_container)
    save_item_values(request.user, 'dmsExerciseFile', name, new, item_container, True)

  class DmsItemForm ( forms.Form ) :
    """ Elemente des Eingabeformulars """
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    text       = forms.CharField(required=False,
                       widget=forms.Textarea(
                                  attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )

  if item_container.container.path.find(HOME_PATH) == 0:
    from dms.queries  import get_quota
    quota = get_quota(request.user)
    quota_exceeded = quota.value > quota.max
  else:
    quota_exceeded = False
  app_name = 'exercisefile'
  my_title = _(u'Meine Lösung einstellen')
  # --- Sind Daten vorhanden oder muessen Sie initialisiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  f = DmsItemForm(data)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  tabs = [ ('tab_base', [ 'fname', 'text' ]),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    name = check_name(request.user.get_full_name() + '_' + request.FILES['fname']['filename'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, request.FILES, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_item_vars_add(request, item_container, app_name, my_title,
                             content, show_errors)
    vars['text_intro'] = help_form['one_file']['help']
    vars['quota_exceeded'] = quota_exceeded
    return render_to_response ( 'app/file/manage_edit.html', vars )
