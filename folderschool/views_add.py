# -*- coding: utf-8 -*-
"""
/dms/folderschool/views_add.py

.. enthaelt den View zum Anlegen eines Basisordners fuer Schulen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import save_container_values
from dms.queries        import save_item_values
from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import get_role_by_user_path
from dms.queries        import get_min_max_menu_left
from dms.queries        import do_protect_folder
from dms.queries        import get_item_container_by_parent_item_id

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_base     import ACL_USERS
from dms.utils_form     import get_folderish_vars_add

from dms.folderschool.utils       import create_school
from dms.folderschool.utils       import get_role_choices
from dms.folderschool.utils       import get_menu_left_from_sections
from dms.folderschool.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def folderschool_add(request, item_container):
  """ neue Arbeitsgruppe anlegen """

  def save_values(name, new, item_container):
    """ Daten sichern """
    create_school(name, new, item_container)

  my_role = get_role_by_user_path(request.user, item_container.container.path)

  class DmsItemForm(forms.Form):
    integer_1   = forms.IntegerField(min_value=1000, max_value=9999,
                        widget=forms.TextInput(attrs={'size':10}) )

  app_name = 'folderschool'
  my_title = _(u'Basisordner für Schule anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'title': '',}
  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_base',['integer_1', ]),]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = 'schule_%s' % f.data['integer_1']
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name,
                                  my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
