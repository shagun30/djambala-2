# -*- coding: utf-8 -*-
"""
/dms/export_dms/views_add.py

.. enthaelt den View zum Export von DMS-Objekten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.11.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_edit

from dms.export_dms.utils     import convert_sql_to_xml

from dms.export_dms.help_form import help_form

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def export_add(request, item_container):
  """ neue Datei anlegen """

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    content_type = forms.CharField(widget=forms.HiddenInput)

  app_name = 'export'
  data = { 'content_type': 'text/xml', }
  f = DmsItemForm(data)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  tabs = [ ('tab_base', [ 'content_type', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST':
    vars = { 'xml_data': convert_sql_to_xml(item_container), }
    return render_to_response('app/export/export.html', vars, mimetype='text/xml')
  else :
    # --- Formular (erneut) anzeigen
    my_title = _(u'Daten als XML exportieren')
    commands = { 'unknown': True, }
    vars = get_item_vars_edit(request, item_container, app_name, my_title,
                              content, f, commands)
    return render_to_response('app/file/manage_edit.html', vars)
