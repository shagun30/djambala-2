#-*-coding: utf-8 -*-
"""
/dms/folder/views_navigation_top.py

.. enthaelt den View zum Aendern des linken Navigationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.05.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_menuitems_by_id_navmenu_top
from dms.queries        import get_site_url

from dms.utils_form     import get_folderish_vars_edit
from dms.utils          import get_tabbed_form

#from dms.encode_decode  import decode_html
#from dms.encode_decode  import encode_html

from dms.utils_navigation import save_menus_top
from dms.folder.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def folder_navigation_top(request, item_container):
  """ Eigenschaften des Ordners aendern """

  class dms_itemForm ( forms.Form ) :
    name        = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':60}) )
    navigation  = forms.CharField(required=False,
                        widget=forms.Textarea( attrs={'rows':24, 'cols':80, 'wrap':'off',
                                               'style':'width:100%;' }) )
  app_name = u'folder'
  my_title = _(u'Oberen Navigationsbereich ändern')
  nav_menu = get_menuitems_by_id_navmenu_top(item_container.container.menu_top_id)[0]
  data_init = { 'name': nav_menu.name,
                'navigation': nav_menu.navigation,}
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = dms_itemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_navigation_top', ['name', 'navigation',]),]
  content=get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    nav_menu.save_menu(data_init, f.data)
    if data_init['navigation'] != f.data['navigation']:
      if request.GET.has_key('profi'):
        save_menus_top(item_container.container.menu_left_id, f.data['navigation'], True)
      else:
        save_menus_top(item_container.container.menu_left_id, f.data['navigation'])
    return HttpResponseRedirect(get_site_url(item_container, 'index.html/manage/'))
  else:
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
