# -*- coding: utf-8 -*-
"""
/dms/discussitem/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften eines Diskussionsbeintrags
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.07.2007  Beginn der Arbeit
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
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html

from dms.discussitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def discussitem_edit(request, item_container):
  """ Eigenschaften des Diskussionsbeintrags aendern """

  def save_values(item_container, old, new):
    save_item(item_container, old, new)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    string_1   = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':60}) )
    string_2   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(widget=forms.Textarea(
                                              attrs={'rows':15, 'cols':60, 'id':'ta', 
                                                    'style':'width:100%;'}) )
    is_browseable       = forms.BooleanField(required=False)
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    #anti_spam  = forms.CharField(required=False, max_length=20,
    #                   widget=forms.TextInput(attrs={'size':20}) )

  data_init = {
                'title'        : decode_html(item_container.item.title),
                'text'         : remove_link_icons(item_container.item.text),
                'string_1'     : item_container.item.string_1,
                'string_2'     : item_container.item.string_2,
                'is_browseable': item_container.is_browseable,
                'visible_start': item_container.visible_start,
                'visible_end'  : item_container.visible_end,
              }

  app_name = u'discussitem'
  my_title = _(U'Diskussionsbeitrag ändern')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm ( data )
  tabs = [
           ( 'tab_base'      , [ 'string_1', 'string_2', 'title', 'text', ] ),
           ( 'tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end' ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
