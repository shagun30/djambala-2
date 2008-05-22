# -*- coding: utf-8 -*-
"""
/dms/home/views_add.py

.. enthaelt den View zum Anlegen eines Home-Verzeichnisses
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.04.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import get_role_by_user_path
from dms.queries        import get_item_container_by_parent_item_id

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_form     import get_folderish_vars_add

from dms.home.utils       import create_home
from dms.home.utils       import get_role_choices
from dms.home.utils       import get_menu_left_from_sections
from dms.home.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def home_add(request, item_container):
  """ neues Home-Verzeichnis anlegen """

  class DmsItemForm(forms.Form):
    name        = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':20}) )

  app_name = 'home'
  my_title = _(u'Home-Verzeichnis anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'name': _(u'Username'), }
  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_base', ['name', ]),]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    username = check_name(f.data['name'], True)
    if not exist_item(item_container, username):
      create_home(username, item_container) # Ausnahme: user wird Besitzer des Home-Verzeichnisses!!!
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, username)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name,
                                  my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
