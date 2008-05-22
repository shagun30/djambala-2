# -*- coding: utf-8 -*-
"""
/dms/emailform/views_show.py

.. zeigt den Inhalt eines Email-Formulars an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  06.11.2007  Beginn der Arbeit
0.02  19.01.2008  Umstellung auf Datenstrukturen des Fragebogens
0.03  18.03.2008  gegebenenfalls wird eine Bestaetigungsemail an die eigene Adresse gesendet
"""

import string
import types
import datetime

from django.utils.encoding  import smart_unicode
from django.template.loader import get_template
from django.template    import Context
from django.core.mail import EmailMultiAlternatives
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.settings       import CONTROL_EMAIL
from dms.roles          import UserEditPerms
from dms.queries        import get_item_by_id
from dms.queries        import get_org_by_username
from dms.utils_form     import get_folderish_vars_show

from dms.utils          import get_tabbed_form
from dms.text_icons     import SEPERATOR_ICON
from dms.utils_form     import get_item_vars_show

from dms.survey.models  import *
from dms.survey.queries import has_user_answered
from dms.survey.queries import create_survey
from dms.survey.queries import get_survey_by_user_id
from dms.survey.queries import save_input
from dms.survey.queries import save_text
from dms.survey.queries import get_min_user
from dms.survey.queries import has_email_answered
from dms.survey.queries import get_survey_by_email
from dms.survey.queries import get_count

from dms.folder.utils   import get_folder_content
from dms.survey.utils   import get_form_tab_row

from dms.emailform.utils  import get_form_items
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def emailform_show(request,item_container):
  """ zeigt den Inhalt eines Email-Formulars """

  def send_email(item_container, item_containers, post, user, user_org):
    """ sendet die Antworten """
    t_text = get_template('app/emailform/email_body_text.html')
    t_html = get_template('app/emailform/email_body.html')
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text'] = ''
    data = []
    my_email = ''
    for ic in item_containers:
      id_str = str(ic.item.id)
      # --- Anzeige der Daten
      if id_str in post and post[id_str]!='':
        this_data = post[id_str]
        if type(this_data) == types.ListType:
          value = ''
          for d in this_data:
            if value != '':
              value += ' | '
            value += d
        else:
          value = this_data
        data.append( { u'header': ic.item.title, u'value': value })
        if ic.item.name == 'email.html':
          my_email = value.strip()
    subject = item_container.item.string_1
    from_addr = CONTROL_EMAIL
    to_addr = [item_container.item.url_more]
    if my_email != '':
      to_addr.append(my_email)
    vars['data'] = data
    email_body = t_html.render(Context(vars))
    email_body_text = t_text.render(Context(vars))
    msg = EmailMultiAlternatives(subject, email_body_text, from_addr, to_addr)
    msg.attach_alternative(email_body, 'text/html')
    msg.send()

  def clean_data(data):
    """ """
    cleaned_data = {}
    keys = data.keys()
    for key in keys:
      this_item = data.getlist(key)
      if len(this_item) == 1:
        cleaned_data[key] = this_item[0]
      else:
        cleaned_data[key] = this_item
    return cleaned_data

  def show_incomplete_data(error_ids):
    """ zeigt eine entsprechende Fehlerseite an """
    vars = get_item_vars_show(request, item_container, app_name)
    error_list = []
    for error in error_ids:
      item = get_item_by_id(error)
      error_list.append(item.title)
    vars['text'] = ''
    vars['error_list'] = error_list
    return render_to_response('app/emailform/incomplete.html', vars)

  def show_success(item_container, item_containers, post):
    """ zeigt positive Rueckmeldung """
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text'] = ''
    data = []
    for ic in item_containers:
      id_str = str(ic.item.id)
      # --- Anzeige der Daten
      if id_str in post and post[id_str]!='':
        this_data = post[id_str]
        if type(this_data) == types.ListType:
          value = ''
          for d in this_data:
            if value != '':
              value += ' | '
            value += d
        else:
          value = this_data
        data.append( { 'header': ic.item.title, 'value': value })
    vars['data'] = data
    return render_to_response('app/emailform/success.html', vars)

  def has_complete_data(item_container, item_containers, post):
    """ sind alle Muss-Daten vorhanden? """
    error_ids = []
    for ic in item_containers:
      if ic.item.integer_1:  # required
        id_str = str(ic.item.id)
        if not post.has_key(id_str) or post[id_str]=='':
          error_ids.append( ic.item.id )
    return error_ids

  def get_form(item_container, ics, sections, d_sections, err_ids, post=[]):
    """ erzeugt das Eingabeformular """
    t_form = get_template('app/emailform/base_form.html')
    this_section = {}
    form_objs = []
    section = ''
    objs = []
    curr = 0
    for ic in ics:
      if section != ic.section:
        if this_section != {}:
          this_section['forms'] = form_objs
          objs.append(this_section)
          this_section = {}
          curr += 1
          form_objs = []
        section = ic.section
        this_section['name'] = section
        this_section['tab'] = curr
        if curr == 0:
          this_section['selected'] = True
      form_objs.append(get_form_tab_row(ic, user, user_org, {}, {}))
    if this_section != {}:
      this_section['forms'] = form_objs
      objs.append(this_section)
    form_context = Context (  { 'objs': objs,
                                'submit': item_container.item.string_1,
                                'email_id': item_container.item.id,
                              } )
    return t_form.render(form_context)

  app_name = 'emailform'
  user = request.user
  if user.username != 'anonymous':
    user_org = get_org_by_username(user.username)
  else:
    user_org = None
  post = []
  error_ids = []
  ics, sections, d_sections = get_folder_content(item_container, False, ['dmsEmailItem'])
  #assert False
  if request.POST.has_key('email_id') and int(request.POST['email_id']) == item_container.item.id:
    post = request.POST.copy()
    error_ids = has_complete_data(item_container, ics, post)
    if error_ids == []:
      post = clean_data(post)
      send_email(item_container, ics, post, user, user_org)
      return show_success(item_container, ics, post)
    else:
      return show_incomplete_data(error_ids)
  else:
    #vars = get_item_vars_show(request, item_container, app_name)
    user_perms = UserEditPerms(user.username, request.path)
    vars = get_folderish_vars_show(request, item_container, app_name, '', '')
    vars['text_bottom'] = get_form(item_container, ics, sections, d_sections, post)
    return render_to_response('base.html', vars)

