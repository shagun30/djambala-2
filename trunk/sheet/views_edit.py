# -*- coding: utf-8 -*-
"""
/dms/sheet/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.01.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.queries        import get_site_url
from dms.queries        import save_item

from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import get_item_actions
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices

from dms.roles          import *

from dms.encode_decode  import decode_html

from dms.sheet.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def sheet_edit(request, item_container):
  """ Eigenschaften des Ordners aendern """

  def save_values(item_container, old, new):
    save_item(item_container, old, new)

  class DmsItemForm(forms.Form):
    title               = forms.CharField(max_length=240,
                                widget=forms.TextInput(attrs={'size':60}) )
    sub_title           = forms.CharField(required=False, max_length=240,
                                widget=forms.TextInput(attrs={'size':60}) )
    text                = forms.CharField(required=False,
                                widget=forms.Textarea(
                                        attrs={'rows':20, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    image_url           = forms.CharField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_url_url       = forms.URLField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_extern        = forms.BooleanField(required=False)
    info_slot_right     = forms.CharField(required=False,
                                widget=forms.Textarea(
                                        attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    section             = forms.CharField(required=False,
                                widget=forms.Select(choices=get_parent_section_choices(item_container),
                                       attrs={'size':4, 'style':'width:40%'} ) )
    is_browseable       = forms.BooleanField(required=False)
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    license             = forms.ChoiceField(choices=get_license_choices(item_container),
                                            widget=forms.RadioSelect() )

  data_init = {
                'title'           : decode_html(item_container.item.title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : remove_link_icons(item_container.item.text),
                'image_url'       : item_container.item.image_url,
                'image_url_url'   : item_container.item.image_url_url,
                'image_extern'    : item_container.item.image_extern,
                'info_slot_right' : info_slot_to_header ( item_container.item.info_slot_right ),
                'section'         : decode_html(item_container.section),
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'license'         : item_container.item.license.id
              }

  app_name = 'sheet'
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , [ 'title', 'sub_title', 'text', 'section' ] ),
           ( 'tab_image'     , [ 'image_url', 'image_url_url', 'image_extern' ] ),
           ( 'tab_frame'     , [ 'info_slot_right', ] ),
           ( 'tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end', ] ),
           ( 'tab_license'   , [ 'license', ] ),
         ]
  content = get_tabbed_form(tabs, help_form, 'document', f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    user_perms = UserEditPerms(request.user.username,request.path)
    my_title = _(u'Folie ändern')
    vars = { 'content_div_style': 'frame-main-manage',
             'site'             : item_container.container.site,
             'my_name'          : item_container.item.name,
             'action'           : get_item_actions(request, user_perms, item_container, app_name,
                                                   item_container.item.has_comments),
             'breadcrumb'       : get_breadcrumb(item_container),
             'content'          : content,
             'title'            : my_title,
             'sub_title'        : item_container.item.title,
             'footer_email'     : get_footer_email(item_container),
             'last_modified'    : item_container.get_last_modified(),
             'submit'           : my_title,
             'errors'           : f.errors,
             'show_errors'      : True,
            }
    return render_to_response ( 'app/base_edit.html', vars )
