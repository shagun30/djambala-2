# -*- coding: utf-8 -*-
"""
/dms/userregistration/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften der User-Verwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.06.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_item_vars_edit

from dms.userregistration.help_form  import help_form

from dms.encode_decode  import decode_html

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def userregistration_edit(request, item_container):
  """ Eigenschaften der User-Verwaltung aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
    item_container.container.save_values(old, new)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

  class dms_itemForm ( forms.Form ) :
    title          = forms.CharField(max_length=240,
                           widget=forms.TextInput(attrs={'size':60}) )
    sub_title      = forms.CharField(required=False, max_length=240,
                           widget=forms.TextInput(attrs={'size':60}) )
    text           = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    text_more      = forms.CharField(required=False, widget=forms.Textarea(
                           attrs={'rows':10, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    image_url      = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    image_url_url  = forms.URLField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    image_extern   = forms.BooleanField(required=False)
    is_wide        = forms.BooleanField(required=False)
    is_important   = forms.BooleanField(required=False)
    section        = forms.CharField(required=False,
                           widget=forms.Select(choices=get_parent_section_choices(item_container),
                                  attrs={'size':4, 'style':'width:40%'} ) )
    is_browseable  = forms.BooleanField(required=False)
    visible_start  = forms.DateField(input_formats=['%d.%m.%Y'],
                           widget=forms.TextInput(attrs={'size':10}))
    visible_end    = forms.DateField(input_formats=['%d.%m.%Y'],
                           widget=forms.TextInput(attrs={'size':10}))

  app_name = 'userregistration'
  my_title = _(u'Registrierung der Community-Mitglieder ändern')
  my_item = item_container.item
  data_init = {
                'title'          : decode_html(my_item.title),
                'text'           : remove_link_icons(my_item.text),
                'text_more'      : remove_link_icons(my_item.text_more),
                'image_url'      : my_item.image_url,
                'image_url_url'  : my_item.image_url_url,
                'image_extern'   : my_item.image_extern,
                'is_wide'        : my_item.is_wide,
                'is_important'   : my_item.is_important,
                'section'        : item_container.section,
                'is_browseable'  : item_container.is_browseable,
                'visible_start'  : item_container.visible_start,
                'visible_end'    : item_container.visible_end,
              }

  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = dms_itemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte // Sonderfall: Startseite
  tabs = [
          ( 'tab_base'      , [ 'title', 'sub_title', 'text', 'text_more', 'is_wide', 'is_important'] ),
          ( 'tab_image'     , [ 'image_url', 'image_url_url', 'image_extern', ] ),
          ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ),
        ]
  content = get_tabbed_form(tabs, help_form, app_name,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    commands = { 'show_mode': True, 'image_mode': True,}
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f, commands)
    return render_to_response ( 'app/base_edit.html', vars )

