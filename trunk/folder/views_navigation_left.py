#-*-coding: utf-8 -*-
"""
/dms/folder/views_navigation_left.py

.. enthaelt den View zum Aendern des linken 
igationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.03.2007  Beginn der Arbeit
"""

from django.http          import HttpResponse, HttpResponseRedirect
from django.shortcuts     import render_to_response
from django               import newforms as forms
from django.db            import transaction

from django.utils.translation import ugettext as _

from dms.roles            import require_permission
from dms.queries          import get_site_url
from dms.queries          import get_all_menus_left
from dms.queries          import get_menu_by_name_left
from dms.queries          import get_min_max_menu_left

from dms.utils_form       import get_folderish_vars_edit
from dms.utils_navigation import save_menus_left
from dms.utils_navigation import save_menu_left_new
from dms.utils            import get_tabbed_form

#from dms.encode_decode  import decode_html
#from dms.encode_decode  import encode_html

from dms.folder.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def folder_navigation_left(request, item_container):
  """ Eigenschaften des Ordners aendern """

  @transaction.commit_manually
  def save_it(data):
    n_min, n_max = get_min_max_menu_left()
    menu_id = 1 + max(abs(n_min), n_max)
    save_menu_left_new(-1*menu_id, data['new_name'], data['new_description'], '999', True)
    transaction.commit()

  class dms_itemForm(forms.Form):
    # --- Komponenten fuer neues Menue
    if not request.GET.has_key('name'):
      new_name   = forms.CharField(max_length=60,
                          widget=forms.TextInput(attrs={'size':60}) )
      new_description = forms.CharField(max_length=80,
                          widget=forms.TextInput(attrs={'size':60}) )
    else:
      # --- vorhandenes Menue aendern
      name        = forms.CharField(max_length=60,
                          widget=forms.HiddenInput(attrs={'size':60}) )
      navigation  = forms.CharField(required=False,
                          widget=forms.Textarea( attrs={'rows':24, 'cols':80, 'wrap':'off',
                                                'style':'width:100%;' }) )
  name = ''
  app_name = u'folder'
  if not request.method == 'POST' :
    data = request.GET.copy()
    if not data.has_key('name'):
      my_title = _(u'Linken Navigationsbereich ändern/ergänzen')
      nav_menus = get_all_menus_left(mode=1)
      data = { 'new_name': '', 'new_description': ''}
      f = dms_itemForm(data)
      tabs = [('tab_navigation_left_new', ['new_name', 'new_description',]),]
      content = get_tabbed_form(tabs, help_form, app_name, f, has_tabs=False)
      vars = get_folderish_vars_edit(request, item_container, app_name, my_title,
                                     content, None)
      vars['menus_left'] = nav_menus
      return render_to_response ( 'app/folder/menus_left.html', vars )

  if request.method == 'POST':
    data = request.POST.copy()
    if data.has_key('new_name'):
      f = dms_itemForm(data)
      if not f.errors:
        save_it(data)
        # --- anschliessend wird das Edit-Formular aufgerufen
      my_title = _(u'Linken Navigationsbereich ergänzen')
      nav_menus = get_all_menus_left(mode=1)
      f = dms_itemForm(data)
      tabs = [('tab_navigation_left_new', ['new_name', 'new_description',]),]
      content = get_tabbed_form(tabs, help_form, app_name, f)
      vars = get_folderish_vars_edit(request, item_container, app_name, my_title,
                                     content, None)
      vars['menus_left'] = nav_menus
      return render_to_response ( 'app/folder/menus_left.html', vars )

  my_title = _(u'Linken Navigationsbereich ändern')
  if request.method == 'POST':
    data = request.POST.copy()
    nav_menu = get_menu_by_name_left(data['name'])
  else:
    name = request.GET.copy()['name']
    nav_menu = get_menu_by_name_left(name)
    data_init = { 'name': nav_menu.name,
                  'navigation': nav_menu.navigation }
    data = data_init
  f = dms_itemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_navigation_left', ['name', 'navigation',]),]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors:
    nav_menu.save_menu(f.data, True)
    save_menus_left(abs(nav_menu.menu_id), f.data['navigation'], True)
    u = get_site_url(item_container, 'index.html/manage')
    return HttpResponseRedirect(get_site_url(item_container, 'index.html/manage/'))
  else:
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response('app/base_edit.html', vars)