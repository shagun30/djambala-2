# -*- coding: utf-8 -*-
"""
/dms/file/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.02.2007  Beginn der Arbeit
0.02  05.03.2007  has_comments
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import *
from dms.models         import DmsItem
from dms.queries        import get_site_url

from dms.settings       import DOWNLOAD_PATH
from dms.utils          import get_tabbed_form
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html

from dms.file.utils     import save_file
from dms.file.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def file_edit(request, item_container):
  """ Eigenschaften der Datei aendern """

  @transaction.commit_manually
  def save_values(item_container, old, new, files):
    """ """
    if files != {}:
      filename = files['fname']['filename']
      # --- Dateien gleichen Namens werden ersetzt
      if filename == item_container.item.name:
        save_file(filename, files, item_container)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

  class DmsItemForm(forms.Form):
    if item_container.is_data_object:
      fname               = forms.CharField(required=False, max_length=200,
                                  widget=forms.FileInput(attrs={'size':40}) )
      license             = forms.ChoiceField(choices=get_license_choices(item_container),
                                              widget=forms.RadioSelect() )
    title               = forms.CharField(max_length=240,
                                widget=forms.TextInput(attrs={'size':60}) )
    sub_title           = forms.CharField(required=False, max_length=240,
                                widget=forms.TextInput(attrs={'size':60}) )
    text                = forms.CharField(required=False, widget=forms.Textarea(
                                 attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    text_more           = forms.CharField(required=False, widget=forms.Textarea(
                                 attrs={'rows':24, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    url_more_extern     = forms.BooleanField(required=False)
    image_url           = forms.CharField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_url_url       = forms.URLField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_extern        = forms.BooleanField(required=False)
    section             = forms.CharField(required=False,
                                widget=forms.Select(choices=get_parent_section_choices(item_container),
                                       attrs={'size':4, 'style':'width:40%'} ) )
    is_browseable       = forms.BooleanField(required=False)
    has_comments        = forms.BooleanField(required=False)
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))

  data_init = {
                'title'           : decode_html(item_container.item.title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : remove_link_icons(item_container.item.text),
                'text_more'       : remove_link_icons(item_container.item.text_more),
                'url_more_extern' : item_container.item.url_more_extern,
                'image_url'       : item_container.item.image_url,
                'image_url_url'   : item_container.item.image_url_url,
                'image_extern'    : item_container.item.image_extern,
                'section'         : item_container.section,
                'has_comments'    : item_container.item.has_comments,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'license'         : item_container.item.license.id
              }
  app_name = 'file'
  my_title = _(u'Datei ändern')
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , [ 'title', 'sub_title', 'text', 'section', 'url_more_extern', 'has_comments' ] ),
           ( 'tab_more'      , [ 'text_more', ] ),
           ( 'tab_image'     , [ 'image_url', 'image_url_url', 'image_extern' ] ),
           ( 'tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end' ] ),
         ]
  if item_container.is_data_object:
    tabs.append ( ('tab_update', [ 'fname', ] ) )
    tabs.append ( ( 'tab_license'   , [ 'license', ] ) )
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data, request.FILES)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/file/manage_edit.html', vars )
