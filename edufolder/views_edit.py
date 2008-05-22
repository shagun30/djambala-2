# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_edit.py

.. enthaelt den View zurm Aendern der Eigenschaften des Lernarchivs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
0.03  24.09.2007  is_exchangeable
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import set_extra_data
from dms.queries        import get_extra_data
from dms.queries        import get_extra_var

from dms.roles          import *
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils          import get_fach_choices
from dms.utils          import get_schulart_choices

from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html

from dms.edufolder.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edufolder_edit(request, item_container):
  """ Eigenschaften des Lernarchivs aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """

    def check_values(old, new, *args):
      for key in args:
        if key != -1 and not new.has_key(key):
          new[key] = old[key]
      return new

    item_container.container.save_values(old, new)
    old['extra'] = item_container.item.extra
    new = check_values(old, new, 'fach', 'schulart', 'freie_suche') 
    f = fach = new['fach']
    #if f != '' and int(f) == -1:
    if f != '' and f == '---':
      f = ''
    s = new['schulart']
    #if s != '' and int(s) == -1:
    if s != '' and s == '---':
      s = ''
    if f == '' and s == '' and new['freie_suche'] == '':
      new['extra'] = set_extra_data()
    else:
      freie_suche = new['freie_suche']
      new['extra'] = set_extra_data(fach=f, schulart=s, freie_suche=freie_suche)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

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
      info_slot_right= forms.CharField(required=False, 
          widget=forms.Textarea(attrs={'rows':10, 'cols':60, 'id':'ta2',
                                       'style':'width:100%;'}) )
    if item_container.parent_item_id >= 0 :
      section        = forms.CharField(required=False,
                            widget=forms.Select(choices=
                                    get_parent_section_choices(item_container),
                                    attrs={'size':4, 'style':'width:40%'} ) )
    sections       = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':5, 'cols':40, 'style':'width:50%;'}) )
    has_user_support  = forms.BooleanField(required=False)
    has_comments      = forms.BooleanField(required=False)
    is_moderated      = forms.BooleanField(required=False)
    is_browseable     = forms.BooleanField(required=False)
    visible_start     = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':10}))
    visible_end       = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':10}))
    string_1       = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    string_2          = forms.CharField(required=False,max_length=240,
                             widget=forms.TextInput(attrs={'size':60}) )
    url_more          = forms.CharField(required=False,max_length=200,
                             widget=forms.TextInput(attrs={'size':60}) )
    fach              = forms.CharField(required=False,
                             widget=forms.Select(choices=get_fach_choices(),
                                    attrs={'size':10, 'style':'width:80%'} ) )
    schulart          = forms.CharField(required=False,
                             widget=forms.Select(choices=get_schulart_choices(),
                                    attrs={'size':10, 'style':'width:80%'} ) )
    freie_suche       = forms.CharField(required=False,max_length=120,
                             widget=forms.TextInput(attrs={'size':60}) )
    is_exchangeable = forms.BooleanField(required=False)

  app_name = u'edufolder'
  my_title = _(u'Online-Lernarchiv ändern')
  if item_container.item.string_2 == '':
    string2 = _(u'Wikipedia')
  else:
    string2 = item_container.item.string_2
  extra_data = get_extra_data(item_container)
  fach = get_extra_var(extra_data, 'fach', '')
  schulart = get_extra_var(extra_data, 'schulart', '')
  freie_suche = get_extra_var(extra_data, 'freie_suche', '')
  data_init = {
                'title'           : decode_html(item_container.item.title),
                'nav_title'       : decode_html(item_container.container.nav_title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : remove_link_icons(item_container.item.text),
                'text_more'       : remove_link_icons(item_container.item.text_more),
                'image_url'       : item_container.item.image_url,
                'image_url_url'   : item_container.item.image_url_url,
                'image_extern'    : item_container.item.image_extern,
                'is_wide'         : item_container.item.is_wide,
                'is_important'    : item_container.item.is_important,
                'info_slot_right' : info_slot_to_header(item_container.\
                                                        item.info_slot_right),
                'sections'        : decode_html(item_container.container.sections),
                'has_user_support': item_container.item.has_user_support,
                'has_comments'    : item_container.item.has_comments,
                'is_moderated'    : item_container.item.is_moderated,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'string_1'        : item_container.item.string_1,
                'string_2'        : string2,
                'url_more'        : item_container.item.url_more,
                'fach'            : fach,
                'schulart'        : schulart,
                'freie_suche'     : freie_suche,
                'is_exchangeable' : item_container.item.is_exchangeable
              }
  if item_container.parent_item_id >= 0:
    #data_init['section'] = decode_html(item_container.section)
    data_init['section'] = item_container.section

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm ( data )
  tabs = [
            ('tab_base'        , ['title', 'sub_title', 'nav_title',
                                  'section', 'sections',]),
            ('tab_intro'       , ['text', 'text_more',
                                  'image_url', 'image_url_url', 'image_extern',
                                  'is_wide', 'is_important']),
            ('tab_events'      , ['fach', 'schulart', 'freie_suche', ]),
            ('tab_wiki'        , ['url_more', 'string_2']),
            ('tab_user_support', ['has_user_support', 'is_moderated', 'has_comments']),
            ('tab_frame'       , ['info_slot_right',]),
            ('tab_visibility'  , ['is_browseable', 'visible_start', 'visible_end', 'string_1' ]),
            ('tab_formal'      , ['is_exchangeable', ]),
          ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
