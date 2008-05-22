# -*- coding: utf-8 -*-
"""
/dms/wikiitem/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Wiki-Seite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.03.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import save_item

from dms.roles          import require_permission
from dms.models         import DmsItem
from dms.utils          import get_tabbed_form
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_edit

from dms.wiki.queries   import save_version
from dms.wiki.queries   import delete_page_links

from dms.wikiitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def wikiitem_edit(request, item_container):
  """ Eigenschaften der Wiki-Seite aendern """

  wiki_page = item_container.item.name[:item_container.item.name.rfind('.html')]
  @transaction.commit_manually
  def save_values(request, item_container, old, new):
    save_version(request, item_container)
    save_item(item_container, old, new, True, new_user=request.user)
    delete_page_links(item_container)
    transaction.commit()

  class DmsItemForm(forms.Form):
    name       = forms.CharField(required=False,
                       widget=forms.HiddenInput(attrs={'value': wiki_page}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    sub_title  = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(widget=forms.Textarea(
                                 attrs={'rows':12, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    image_url           = forms.CharField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    image_url_url       = forms.URLField(required=False, max_length=200,
                                widget=forms.TextInput(attrs={'size':60}) )
    is_browseable       = forms.BooleanField(required=False)
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    license             = forms.ChoiceField(choices=get_license_choices(item_container),
                                            widget=forms.RadioSelect() )

  data_init = {
                'title'          : item_container.item.title,
                'sub_title'      : item_container.item.sub_title,
                'text'           : remove_link_icons(item_container.item.text),
                'is_browseable'  : item_container.is_browseable,
                'image_url'      : item_container.item.image_url,
                'image_url_url'  : item_container.item.image_url_url,
                'image_extern'   : item_container.item.image_extern,
                'visible_start'  : item_container.visible_start,
                'visible_end'    : item_container.visible_end,
                'license'         : item_container.item.license.id
              }

  app_name = 'wikiitem'
  my_title = _(u'Wiki-Seite ändern')
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , [ 'name', 'title', 'sub_title', 'text' ] ),
           ( 'tab_image'     , [ 'image_url', 'image_url_url', ] ),
           ( 'tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end' ] ),
           ( 'tab_license'   , [ 'license', ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(request, item_container, data_init, f.data)
    parent = item_container.get_parent()
    url = '%s?wiki_page=%s' % (item_container.get_parent().get_absolute_url(),
                                item_container.item.name[:item_container.item.name.rfind('.html')])
    return HttpResponseRedirect(url)
  else:
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
