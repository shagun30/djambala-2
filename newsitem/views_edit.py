# -*- coding: utf-8 -*-
"""
/dms/newsitem/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Nachricht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.03.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import save_item

from dms.roles          import require_permission
from dms.models         import DmsItem
from dms.utils          import get_tabbed_form
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html

from dms.newsitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def newsitem_edit(request, item_container):
  """ Eigenschaften des Gaestebucheintrags aendern """

  def save_values(item_container, old, new):
    save_item(item_container, old, new, True)

  class DmsItemForm(forms.Form):
    string_1   = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':60}) )
    string_2   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    sub_title  = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(widget=forms.Textarea(
                                 attrs={'rows':12, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    text_more  = forms.CharField(required=False, widget=forms.Textarea(
                                 attrs={'rows':24, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    url_more   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    url_more_extern     = forms.BooleanField(required=False)
    image_url           = forms.CharField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_url_url       = forms.URLField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_extern        = forms.BooleanField(required=False)
    is_browseable       = forms.BooleanField(required=False)
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    license             = forms.ChoiceField(choices=get_license_choices(item_container),
                                            widget=forms.RadioSelect() )

  data_init = {
                'title'          : decode_html(item_container.item.title),
                'sub_title'      : decode_html(item_container.item.sub_title),
                'text'           : remove_link_icons(item_container.item.text),
                'text_more'      : remove_link_icons(item_container.item.text_more),
                'string_1'       : item_container.item.string_1,
                'string_2'       : item_container.item.string_2,
                'is_browseable'  : item_container.is_browseable,
                'image_url'      : item_container.item.image_url,
                'image_url_url'  : item_container.item.image_url_url,
                'image_extern'   : item_container.item.image_extern,
                'url_more'       : item_container.item.url_more,
                'url_more_extern': item_container.item.url_more_extern,
                'visible_start'  : item_container.visible_start,
                'visible_end'    : item_container.visible_end,
                'license'         : item_container.item.license.id
              }

  app_name = 'newsitem'
  my_title = _(u'Nachricht ändern')
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , [ 'string_1', 'string_2', 'title', 'sub_title', 'text', 'text_more', \
                                 'url_more', 'url_more_extern', ] ),
           ( 'tab_image'     , [ 'image_url', 'image_url_url', 'image_extern' ] ),
           ( 'tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end' ] ),
           ( 'tab_license'   , [ 'license', ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
