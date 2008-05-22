# -*- coding: utf-8 -*-
"""
/dms/home/views_edit.py

.. enthaelt den View zurm Aendern der Eigenschaften von Home-Verzeichnissen
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

from dms.roles          import require_permission

from dms.queries        import get_site_url
from dms.queries        import get_role_by_user_path
from dms.queries        import get_item_container_by_parent_item_id
from dms.queries        import save_min_role_id
from dms.queries        import get_min_max_menu_left
from dms.queries        import get_item_container_children

from dms.roles          import *
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_folderish_vars_edit
from dms.utils_navigation         import save_menus_left

from dms.encode_decode  import decode_html

from dms.home.utils       import get_role_choices
from dms.home.utils       import get_menu_left_from_sections
from dms.home.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def home_edit(request, item_container):
  """ Eigenschaften des Home-Verzeichnisses aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')
  my_role = get_role_by_user_path(request.user, item_container.container.path)

  #@transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
    ic = get_item_container_by_parent_item_id(item_container.item.id)
    folders = []
    for i in ic:
      if i.item.app.is_folderish and not i.item.app.is_userfolder:
        folders.append(i.item.name)
    text = get_menu_left_from_sections(item_container, '', new['sections'], folders)
    if my_role <= 10 and new.has_key('new_menu') and new['new_menu']:
      n_min, n_max = get_min_max_menu_left()
      menu_left_id = 1 + max(abs(n_min), n_max)
      save_menus_left(menu_left_id, text)
      item_container.container.menu_left_id = menu_left_id
      item_container.container.nav_name_left = 'start|'
      item_container.container.save()
      # heuristischer Versuch, die Menupunkte zu bestimmen
      ics = get_item_container_children(item_container, True)
      for ic in ics:
        ic.container.menu_left_id = menu_left_id
        if ic.item.name in new['sections']:
          ic.container.nav_name_left = 'start|' + ic.item.name.lower()
        else:
          ic.container.nav_name_left = 'start|'
        ic.container.save()
    else:
      save_menus_left(item_container.container.menu_left_id, text)
    item_container.container.save_values(old, new)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    save_min_role_id(item_container, old, new)
    #transaction.commit()

  class dms_itemForm ( forms.Form ) :
    """ Elemente des Eingabeformulars """
    text              = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows':5, 'cols':60, 'id':'ta',
                                      'style':'width:100%;'}) )
    text_more         = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows':10, 'cols':60, 'id':'ta1',
                                      'style':'width:100%;'}) )
    image_url         = forms.CharField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
    image_url_url     = forms.URLField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
    image_extern      = forms.BooleanField(required=False)
    is_wide           = forms.BooleanField(required=False)
    is_important      = forms.BooleanField(required=False)
    if profi_mode:
      info_slot_right = forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'style':'width:100%;'}) )
    else:
      info_slot_right = forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    sections          = forms.CharField(required=False, widget=forms.Textarea(
                              attrs={'rows':5, 'cols':40, 'style':'width:60%;'}) )
    visible_start     = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':15}))
    visible_end       = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':15}))
    show_next         = forms.BooleanField(required=False)
    min_role_id       = forms.CharField(required=True,
                        widget=forms.Select(choices=get_role_choices(my_role),
                                      attrs={'size':6, 'style':'width:100%'} ) )
    string_2          = forms.CharField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
    new_menu          = forms.BooleanField(required=False)

  my_item = item_container.item
  app_name = 'home'
  my_title = _(u'Home-Verzeichnis ändern')
  data_init = {
                'text'            : remove_link_icons(my_item.text),
                'text_more'       : remove_link_icons(my_item.text_more),
                'image_url'       : my_item.image_url,
                'image_url_url'   : my_item.image_url_url,
                'image_extern'    : my_item.image_extern,
                'is_wide'         : my_item.is_wide,
                'is_important'    : my_item.is_important,
                'info_slot_right' : info_slot_to_header(my_item.info_slot_right),
                'sections'        : decode_html(item_container.container.sections),
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'show_next'       : item_container.container.show_next,
                'min_role_id'     : item_container.container.min_role_id,
                'string_2'        : my_item.string_2,
                'new_menu'        : False
              }
  s = item_container.visible_start
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST':
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm ( data )
  visibility = ['visible_start', 'visible_end', 'string_2']
  if my_role <= 10:   # the_manager
    visibility.append('new_menu')
  tabs = [
          ('tab_base'        , ['sections', ]),
          ('tab_intro'       , ['text', 'text_more', 'image_url', 'image_url_url', 'image_extern',
                                'is_wide', 'is_important']),
          ('tab_frame'       , ['info_slot_right',]),
          ('tab_visibility'  , visibility),
          ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    dont = { 'navigation_left_mode': False, 'navigation_mode': False}
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f, dont)
    return render_to_response ( 'app/base_edit.html', vars )
