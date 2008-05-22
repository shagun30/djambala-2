#-*-coding: utf-8 -*-
"""
/dms/document/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.01.2007  Beginn der Arbeit
0.02  07.04.2007  Straffung des Programmcodes
"""

from django.db              import transaction
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_app
from dms.queries        import get_site_url
from dms.queries        import save_item
from dms.queries        import save_item_container
from dms.queries        import get_data_item_container

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import get_license_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import  decode_html

from dms.document.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def document_edit(request, item_container):
  """ Eigenschaften der Informationsseite aendern """

  parent_app = get_parent_app(item_container)

  def save_values(item_container, old, new):
    if item_container.is_data_object:
      save_item(item_container, old, new)
    else:
      save_item_container(item_container, old, new)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    if item_container.is_data_object:
      title           = forms.CharField(max_length=240,
                              widget=forms.TextInput(attrs={'size':60}) )
      sub_title       = forms.CharField(required=False, max_length=240,
                              widget=forms.TextInput(attrs={'size':60}) )
      if parent_app == 'dmsPool':
        text       = forms.CharField(required=False, widget=forms.Textarea(
                          attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
        text_more  = forms.CharField(required=False, widget=forms.Textarea(
                          attrs={'rows':18, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
      else:
        text       = forms.CharField(required=False, widget=forms.Textarea(
                          attrs={'rows':20, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
      image_url       = forms.CharField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
      image_url_url   = forms.URLField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
      image_extern    = forms.BooleanField(required=False)
      info_slot_right = forms.CharField(required=False, widget=forms.Textarea(
                              attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
      section         = forms.CharField(required=False,
                              widget=forms.Select(choices=get_parent_section_choices(item_container),
                                    attrs={'size':4, 'style':'width:40%'} ) )
      is_browseable   = forms.BooleanField(required=False)
      has_comments    = forms.BooleanField(required=False)
      visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))
      visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))
      license         = forms.ChoiceField(choices=get_license_choices(item_container),
                                          widget=forms.RadioSelect() )
    else:
      section         = forms.CharField(required=False,
                              widget=forms.Select(choices=get_parent_section_choices(item_container),
                                    attrs={'size':4, 'style':'width:40%'} ) )
      is_browseable   = forms.BooleanField(required=False)
      visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))
      visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))

  data_init = {
                'title'           : decode_html(item_container.item.title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : remove_link_icons(item_container.item.text),
                'image_url'       : item_container.item.image_url,
                'image_url_url'   : item_container.item.image_url_url,
                'image_extern'    : item_container.item.image_extern,
                'info_slot_right' : info_slot_to_header(item_container.item.info_slot_right),
                'section'         : decode_html(item_container.section),
                'has_comments'    : item_container.item.has_comments,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'license'         : item_container.item.license.id
              }
  app_name = u'document'
  if parent_app == 'dmsPool':
    data_init['text_more'] = item_container.item.text_more
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)
  if item_container.is_data_object:
    my_title = _(u'Informationsseite ändern')
    if parent_app == 'dmsPool':
      tabs = [
              ( u'tab_base'      , [ u'title', u'sub_title', u'text', u'text_more', u'has_comments',] ),
              ( u'tab_image'     , [ u'image_url', u'image_url_url', u'image_extern', ] ),
              ( u'tab_frame'     , [ u'info_slot_right', ] ),
              ( u'tab_visibility', [ u'section', u'is_browseable', u'visible_start', u'visible_end', ] ),
              ( u'tab_license',    [ u'license', ] ),
            ]
    else:
      tabs = [
              ( u'tab_base'      , [ u'title', u'sub_title', u'text',  u'has_comments',] ),
              ( u'tab_image'     , [ u'image_url', u'image_url_url', u'image_extern', ] ),
              ( u'tab_frame'     , [ u'info_slot_right', ] ),
              ( u'tab_visibility', [ u'section', u'is_browseable', u'visible_start', u'visible_end', ] ),
              ( u'tab_license',    [ u'license', ] ),
            ]
  else:
    data_url = get_data_item_container(item_container).get_absolute_url()
    my_title = _(u'Einblendung einer Informationsseite ändern') + data_url
    tabs = [ ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else:
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/base_edit.html', vars )
