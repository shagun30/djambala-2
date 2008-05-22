# -*- coding: utf-8 -*-
"""
/dms/wikibookitem/views_add.py

.. enthaelt den View zum Ergaenzen einer Wiki-Seite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.03.2008  Beginn der Arbeit
"""

import string
import time
import datetime

from django.utils.encoding  import smart_unicode
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.queries        import save_item_values
from dms.queries        import get_random_question_answer
from dms.queries        import check_answer
from dms.queries        import get_user
from dms.queries        import get_site_url

#from dms.roles          import *
from dms.utils          import get_tabbed_form
from dms.utils          import get_license_choices
from dms.utils          import check_name
from dms.mail           import send_control_email
from dms.utils_form     import get_item_vars_add

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html_dir

from dms.views_error    import show_error_spam

from dms.wikiitem.help_form       import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def wikiitem_add(request, item_container):
  """ neue Nachricht anlegen """
  if request.GET.has_key('wiki_page'):
    wiki_page = check_name(request.GET['wiki_page'].lower(), True)
  else:
    wiki_page = 'start'

  def save_values(name, new, my_folder):
    """ Wiki-Seite sichern """
    new['section'] = ''
    save_item_values(request.user, 'dmsWikiItem', name, new, my_folder,
                     not my_folder.item.is_moderated, True,)
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    name       = forms.CharField(required=False,
             widget=forms.HiddenInput(attrs={'value': wiki_page}) )
    title      = forms.CharField(max_length=240,
             widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(widget=forms.Textarea(
             attrs={'rows':24, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    #license         = forms.ChoiceField(choices=get_license_choices(item_container),
    #         widget=forms.RadioSelect() )

  app_name = 'wikiitem'
  my_title = _(u'Wiki-Seite anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'license': 1, }
  f = DmsItemForm ( data )

  if request.method == 'POST' and not f.errors:
    #new = encode_html_dir(f.data)
    new = f.data
    name = new['name'] + '.html'
    save_values(name, f.data, item_container)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    # --- Reihenfolge, Ueberschriften, Hilfetexte
    tabs = [ ('tab_base', [ 'name', 'title', 'text', ]),
             #( 'tab_license',    [ 'license', ] ),
            ]
    content = get_tabbed_form(tabs, help_form, app_name, f)
    if item_container.item.is_moderated:
      moderated_text = help_form['moderated_text']['info']
    else:
      moderated_text = ''
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['moderated_text'] = moderated_text
    return render_to_response ( 'app/base_edit.html', vars )
