# -*- coding: utf-8 -*-
"""
/dms/newsbookitem/views_add.py

.. enthaelt den View zum Ergaenzen einer Nachricht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.03.2007  Beginn der Arbeit
0.02  21.05.2008  show_error_community_members_only
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
from dms.mail           import send_control_email
from dms.utils_form     import get_item_vars_add

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html_dir

from dms.views_error    import show_error_spam
from dms.views_error    import show_error_community_members_only

from dms.newsitem.help_form       import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def newsitem_add(request, item_container):
  """ neue Nachricht anlegen """
  question, answer = get_random_question_answer()
  my_user = get_user(request.user.username)
  if my_user != None:
    my_name = my_user.get_full_name()
    my_email = my_user.email
  else:
    my_name = ''
    my_email = ''

  def save_values(name, new, my_folder):
    """ Daten sichern """
    new['section'] = ''
    new['visible_start'] = datetime.date.today().strftime('%d.%m.%Y')
    save_item_values(request.user, 'dmsNewsItem', name, new, my_folder,
                     not my_folder.item.is_moderated, True,
                     visible_start=new['visible_start'],
                     visible_end=new['visible_end'])
    send_control_email(item_container)

  class DmsItemForm ( forms.Form ) :
    if my_user == None:
      string_1   = forms.CharField(max_length=60,
             widget=forms.TextInput(attrs={'size':60}) )
      string_2   = forms.CharField(required=False, max_length=200,
             widget=forms.TextInput(attrs={'size':60}) )
      anti_spam_question = forms.CharField(required=False,
             widget=forms.HiddenInput(attrs={'value':question}) )
      anti_spam_answer   = forms.CharField(max_length=20,
             widget=forms.TextInput(attrs={'size':20}) )
    else:
      # --- eigentlich koennte required=False entfallen
      string_1   = forms.CharField(required=False,
             widget=forms.HiddenInput(attrs={'value':my_name}) )
      string_2   = forms.CharField(required=False,
             widget=forms.HiddenInput(attrs={'value':my_email}) )
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
    visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
             widget=forms.TextInput(attrs={'size':10}))
    #license         = forms.ChoiceField(choices=get_license_choices(item_container),
    #         widget=forms.RadioSelect() )

  app_name = 'newsitem'
  my_title = _(u'Nachricht anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'visible_end': (datetime.datetime.now() + datetime.timedelta(30)).strftime('%d.%m.%Y'),
             'license': 1, }
  f = DmsItemForm ( data )

  if request.method == 'POST' and not f.errors:
    #new = encode_html_dir(f.data)
    new = f.data
    if request.user.username == '':
      if new.has_key('anti_spam_question'):
        is_ok = check_answer(new['anti_spam_question'], new['anti_spam_answer'])
    else:
      is_ok = True
    if is_ok:
      now = smart_unicode(time.time())
      name = 'news_item_' + now[:string.find(now, '.')] + '.html'
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else:
      return show_error_spam(request, item_container)
  else :
    # --- Reihenfolge, Ueberschriften, Hilfetexte
    if my_user == None:
      if item_container.item.integer_4 == 1:
        return show_error_community_members_only(request, item_container)
      tabs = [ ('tab_base', [ 'string_1', 'string_2', 'title', 'sub_title', 'text',
                              'text_more', 'url_more', 'visible_end',
                              'anti_spam_question', 'anti_spam_answer' ]),
               #( 'tab_license',    [ 'license', ] ),
             ]
    else:
      tabs = [ ('tab_base', [ 'string_1', 'string_2', 'title', 'sub_title', 'text',
                              'text_more', 'url_more', 'visible_end', ]),
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
