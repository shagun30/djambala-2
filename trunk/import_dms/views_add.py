# -*- coding: utf-8 -*-
"""
/dms/import_dms/views_add.py

.. enthaelt den View zum Import von DMS-Objekten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  27.04.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.models         import DmsItem
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils          import check_name
from dms.utils          import check_name
from dms.utils_form     import get_item_vars_edit

from dms.import_dms.utils     import convert_xml_to_sql

from dms.import_dms.help_form import help_form

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def import_add(request, item_container):
  """ neue Datei anlegen """

  def save_values(user, name, files, my_folder):
    """ Daten sichern """
    #content = files['fname']['content'].encode('iso-8859-1')
    content = files['fname']['content']
    content_type = files['fname']['content-type']
    res = convert_xml_to_sql(user, content, my_folder)
    return res

  class DmsItemForm ( forms.Form ) :
    """ Elemente des Eingabeformulars """
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
  app_name = 'import'
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  f = DmsItemForm(data)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  tabs = [ ('tab_base', [ 'fname', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    name = check_name(request.FILES['fname']['filename'], True)
    save_values(request.user, name, request.FILES, item_container)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    # --- Formular (erneut) anzeigen
    my_title = _(u'XML-Daten importieren')
    commands = { 'unknown': True, }
    vars = get_item_vars_edit(request, item_container, app_name, my_title,
                              content, f, commands)
    return render_to_response('app/file/manage_edit.html', vars)
