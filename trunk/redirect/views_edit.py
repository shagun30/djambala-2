# -*- coding: utf-8 -*-
"""
/dms/redirect/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Weiterleitung
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

from dms.utils          import get_tabbed_form
from dms.utils          import get_parent_section_choices
from dms.roles          import require_permission
from dms.utils          import remove_link_icons
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html

from dms.redirect.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def redirect_edit(request, item_container):
  """ Eigenschaften des Ordners aendern """

  def save_values(item_container, old, new):
    save_item(item_container, old, new)

  class DmsItemForm ( forms.Form ) :
    title           = forms.CharField(max_length=240,
                            widget=forms.TextInput(attrs={'size':60}) )
    url_more        = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={'size':60}) )
    url_more_extern = forms.BooleanField(required=False)
    text            = forms.CharField(required=False,
                            widget=forms.Textarea(
                                   attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
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
                'text'            : remove_link_icons(item_container.item.text),
                'url_more'        : item_container.item.url_more,
                'url_more_extern' : item_container.item.url_more_extern,
                'section'         : item_container.section,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
              }
  app_name = 'redirect'
  my_title = _(u'Weiterleitung ändern')
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , ['title', 'url_more', 'url_more_extern', 'text', 'section', ] ),
           ( 'tab_visibility', ['is_browseable', 'visible_start', 'visible_end', ] ),
          ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values ( item_container, data_init, f.data )
    return HttpResponseRedirect(get_site_url(item_container, 'index.html/manage/'))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response('app/base_edit.html', vars)
