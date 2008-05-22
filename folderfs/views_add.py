# -*- coding: utf-8 -*-
"""
/dms/folderfs/views_add.py

.. enthaelt den View zum Ergaenzen eines FS-Ordners
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.01.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_form     import get_folderish_vars_add

from dms.queries        import save_container_values
from dms.queries            import exist_item

from dms.folderfs.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def folderfs_add(request, item_container):
  """ neuen FS-Ordner anlegen """

  def save_values(name, new, my_folder):
    """ Daten sichern """
    new['sections'] = ''
    new['has_user_support'] = True
    new['is_moderated'] = True
    save_container_values(request.user, 'dmsFolderFS', name, new, my_folder)

  class DmsItemForm(forms.Form):
    name     =forms.CharField(max_length=60,
                    widget=forms.TextInput(attrs={'size':20}) )
    title    =forms.CharField(max_length=240,
                    widget=forms.TextInput(attrs={'size':60}) )
    nav_title=forms.CharField(required=False, max_length=60,
                    widget=forms.TextInput(attrs={'size':30}) )
    section  =forms.CharField(required=False,
                    widget=forms.Select(choices=get_section_choices(item_container.container.sections),
                                        attrs={'size':4, 'style':'width:40%'} ) )

  app_name = 'folderfs'
  my_title = _(u'Ordner für Dateisystem anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'name': _(u'dateien'), 'title': _(u'Dateien') }
  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_base',['name','title','nav_title','section',]),]
  # --- Formular zusammenbauen
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
  else :
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
