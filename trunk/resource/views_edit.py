# -*- coding: utf-8 -*-
"""
/dms/resource/views_edit.py

.. enthaelt den View zurm Aendern der Eigenschaften der Ressourcenverwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2008  Uebernahme von Folder
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import get_user_roles
from dms.roles          import require_permission
from dms.queries        import get_site_url
from dms.queries        import get_role_by_user_path
from dms.queries        import get_role_by_name
from dms.queries        import save_min_role_id
from dms.queries        import get_org_by_username

from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html
from dms.projectgroup.utils       import get_role_choices

from dms.resource.queries   import exist_settings_org_id
from dms.resource.queries   import clear_org_settings
from dms.resource.queries   import create_org_settings

from dms.resource.utils   import show_org_settings
from dms.resource.utils   import get_periods_list

from dms.resource.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def resource_edit(request, item_container):
  """ Eigenschaften der Ressourcenverwaltung aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')
  user_role = get_role_by_user_path(request.user, item_container.container.path)

  def get_choices():
    """ """
    ret = []
    ret.append( (0, _(u'Zeitspannen wie oben')) )
    ret.append( (1, _(u'Vorbelegung Schulstunden')) ) # Schulen
    ret.append( (2, _(u'Vorbelegung Zeitstunden')) )  # Institutionen
    return ret

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
    org = get_org_by_username(request.user.username)
    if int(new['my_periods'])==0:
      periods_list = get_periods_list(org.org_id, new['periods_as_text'])
      create_org_settings(org.org_id, periods_list)
    elif int(new['my_periods'])==1:
      #clear_org_settings(org.org_id)
      create_org_settings(org.org_id, get_periods_list(1, ''))   # Schulen
    else:
      create_org_settings(org.org_id, get_periods_list(-1, ''))  # Institutionen
    #new['my_periods'] = -1
    item_container.container.save_values(old, new)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()


  org = get_org_by_username(request.user.username)
  """
  if not exist_settings_org_id(org.org_id):
    preset_periods = 0
  else:
    preset_periods = 1
  """
  
  class dms_itemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    title          = forms.CharField(max_length=240,
                           widget=forms.TextInput(attrs={'size':60}) )
    nav_title      = forms.CharField(max_length=60,
                           widget=forms.TextInput(attrs={'size':30}) )
    sub_title      = forms.CharField(required=False, max_length=240,
                           widget=forms.TextInput(attrs={'size':60}) )
    text           = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':5, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    text_more      = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':10, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    image_url      = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    image_url_url  = forms.URLField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    image_extern   = forms.BooleanField(required=False)
    is_wide        = forms.BooleanField(required=False)
    is_important   = forms.BooleanField(required=False)
    if profi_mode:
      info_slot_right= forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'style':'width:100%;'}) )
    else:
      info_slot_right= forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    if item_container.parent_item_id >= 0 :
      section        = forms.CharField(required=False,
                            widget=forms.Select(choices=
                                    get_parent_section_choices(item_container),
                                    attrs={'size':4, 'style':'width:40%'} ) )
    #sections       = forms.CharField(required=False, widget=forms.Textarea(
    #                       attrs={'rows':5, 'cols':40, 'style':'width:50%;'}) )
    is_browseable  = forms.BooleanField(required=False)
    visible_start  = forms.DateField(input_formats=['%d.%m.%Y'],
                           widget=forms.TextInput(attrs={'size':15}))
    visible_end    = forms.DateField(input_formats=['%d.%m.%Y'],
                           widget=forms.TextInput(attrs={'size':15}))
    #show_next      = forms.BooleanField(required=False)
    #string_1       = forms.CharField(required=False, max_length=200,
    #                       widget=forms.TextInput(attrs={'size':60}) )
    #min_role_id    = forms.CharField(required=True,
    #                    widget=forms.Select(choices=get_role_choices(user_role),
    #                                        attrs={'size':10, 'style':'width:100%'} ) )
    my_periods      = forms.ChoiceField(choices=get_choices(), widget=forms.RadioSelect() )
    periods_as_text = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
  
  org = get_org_by_username(request.user.username)
  my_periods_as_text = show_org_settings(org.org_id)
  
  app_name = 'resource'
  my_title = _(u'Ressourcenverwaltung ändern')
  my_item = item_container.item
  data_init = {
                'title'          : decode_html(my_item.title),
                'nav_title'      : decode_html(item_container.container.nav_title),
                'sub_title'      : decode_html(my_item.sub_title),
                'text'           : remove_link_icons(my_item.text),
                'text_more'      : remove_link_icons(my_item.text_more),
                'image_url'      : my_item.image_url,
                'image_url_url'  : my_item.image_url_url,
                'image_extern'   : my_item.image_extern,
                'is_wide'        : my_item.is_wide,
                'is_important'   : my_item.is_important,
                'info_slot_right': info_slot_to_header(my_item.info_slot_right),
                #'sections'       : decode_html(item_container.container.sections),
                'is_browseable'  : item_container.is_browseable,
                'visible_start'  : item_container.visible_start,
                'visible_end'    : item_container.visible_end,
                #'show_next'      : item_container.container.show_next,
                #'string_1'       : my_item.string_1,
                #'min_role_id'    : item_container.container.min_role_id,
                #'my_periods'     : preset_periods,
                'my_periods'     : 0,
                'periods_as_text': my_periods_as_text,
              }
  if item_container.parent_item_id >= 0 :
    data_init['section'] = decode_html(item_container.section)
  
  # --- Sind Daten vorhanden oder muessen sie initialisiert werden?
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm(data)
  """
  if user_role <= get_role_by_name('the_manager'):
    #tab_more = ['show_next', 'string_1', 'min_role_id' ]
    tab_more = ['my_periods' ]
  else:
    #tab_more = ['show_next', 'string_1']
    tab_more = ['my_periods']
  """
  tab_more = ['periods_as_text', 'my_periods']
  if item_container.parent_item_id >= 0 :
    tabs = [
             ('tab_base'      , ['title', 'sub_title', 'nav_title', 'section',]),
             ('tab_intro'     , ['text', 'text_more', 'image_url', 'image_url_url', 'image_extern',
                                 'is_wide', 'is_important']),
             ('tab_frame'     , ['info_slot_right',]),
             ('tab_visibility', ['is_browseable', 'visible_start', 'visible_end', ]),
             ('tab_more'      , tab_more),
           ]
  else :
    tabs = [
             ('tab_base'      , ['title', 'sub_title', 'nav_title',]),
             ('tab_intro'     , ['text','text_more','image_url','image_url_url',
                                'is_wide','is_important','image_extern',]),
             ('tab_frame'     , ['info_slot_right',]),
             ('tab_visibility', ['visible_start','visible_end', ]),
             ('tab_more'      , tab_more),
           ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
