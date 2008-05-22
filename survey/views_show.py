# -*- coding: utf-8 -*-
"""
/dms/survey/views_show.py

.. zeigt das Fragebogenformular an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.01.2008  Beginn der Arbeitfrom django.utils.encoding  import smart_unicode
0.02  15.01.2008  Weiterarbeit
0.03  16.01.2008  Kontrolle der Vollstaendigkeit der Angaben
0.04  17.01.2008  Vorbelegung mit Community-Daten
0.05  18.01.2008  Anonyme User koennen antworten (E-Mail)
0.06  19.01.2008  admin_options
0.07  09.02.2008  Daten werden wieder angezeigt
"""

import string
import types
import datetime

from django.utils.safestring  import mark_safe
from django.utils.encoding  import smart_unicode
from django.template.loader import get_template
from django.template    import Context
from django.core.mail   import send_mail
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.template.loader import get_template
from django.template    import Context

from django.utils.translation import ugettext as _

from dms.settings       import CONTROL_EMAIL
from dms.roles          import UserEditPerms

from dms.queries        import get_item_by_id
from dms.queries        import get_org_by_username

from dms.utils          import get_tabbed_form
from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.text_icons     import SEPERATOR_ICON

from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_folderish_vars_show
from dms.folder.utils   import get_folder_content

from dms.survey.models  import *
from dms.survey.queries import has_user_answered
from dms.survey.queries import create_survey
from dms.survey.queries import get_survey_by_user_id
from dms.survey.queries import save_input
from dms.survey.queries import save_text
from dms.survey.queries import delete_data
from dms.survey.queries import get_min_user
from dms.survey.queries import has_email_answered
from dms.survey.queries import get_survey_by_email
from dms.survey.queries import get_count
from dms.survey.queries import get_inputs_by_person
from dms.survey.queries import get_texts_by_person

from dms.survey.utils   import get_form_tab_row
from dms.survey.utils   import get_admin_options

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def survey_show(request,item_container):
  """ zeigt den Inhalt eines Email-Formulars """

  def save_survey(item_container, item_containers, post, user, user_org):
    """ speichert die Antworten """
    if user_org != None:  # User existiert und ist eingeloggt
      if has_user_answered(item_container, user.id):
        question_container = get_survey_by_user_id(item_container, user.id)
      else:
        question_container = create_survey(item_container, user.id)
    else:
      question_container = None
      # gibt es ein E-Mail-Feld
      for ic in item_containers:
        if ic.item.name == 'email.html' and ic.item.integer_1:
          email = post[str(ic.item.id)]
          if has_email_answered(ic, email):
            question_container = get_survey_by_email(item_container, ic, email)
            break
      # falls nein: Negativzahl erzeugen
      if question_container == None:
        question_container = create_survey(item_container, get_min_user(item_container)-1)
    pers_id = question_container.pers_id
    delete_data(item_container, pers_id)
    for ic in item_containers:
      id_str = str(ic.item.id)
      this_type = ic.item.string_1
      # --- Anzeige der Daten
      if id_str in post:
        this_data = post[id_str]
        if type(this_data) == types.ListType:
          for d in this_data:
            save_input(item_container, ic, pers_id, smart_unicode(d.strip()))
        elif this_type == 'text':
          save_text(item_container, ic, pers_id, smart_unicode(this_data.strip()))
        else:
          save_input(item_container, ic, pers_id, smart_unicode(this_data.strip()))

  def clean_data(data):
    """ Mehrfacheingaben werden in Listen umgewandelt """
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
    return render_to_response('app/survey/incomplete.html', vars)

  def get_input_data(item_container, item_containers, post):
    """ liefert die Eingabedaten """
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
    return data

  def send_survey(item_container, item_containers, post, user, user_org):
    """ sendet die Eingaben an den Eingeber """
    from django.core.mail import EmailMultiAlternatives
    subject = _(u'Ihre Eingaben: ') + item_container.item.title
    from_addr = CONTROL_EMAIL
    to_addr = ''
    if user_org != None:  # User existiert und ist eingeloggt
      to_addr = user.email
    else:
      # gibt es ein E-Mail-Feld
      for ic in item_containers:
        if ic.item.name == 'email.html' and ic.item.integer_1:
          to_addr = post[str(ic.item.id)]
          break
    if to_addr != '':
      vars = {}
      vars['text'] = mark_safe(item_container.item.text)
      vars['text_more'] = mark_safe(item_container.item.text_more)
      vars['data'] = get_input_data(item_container, item_containers, post)
      t_text = get_template('app/emailform/email_body_text.html')
      t_html = get_template('app/emailform/email_body.html')
      email_body = t_html.render(Context(vars))
      email_body_text = t_text.render(Context(vars))
      msg = EmailMultiAlternatives(subject, email_body_text, from_addr, [to_addr])
      msg.attach_alternative(email_body, 'text/html')
      msg.send()

  def show_success(item_container, item_containers, post):
    """ zeigt positive Rueckmeldung """
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text'] = ''
    vars['data'] = get_input_data(item_container, item_containers, post)
    return render_to_response('app/survey/success.html', vars)

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
    t_form = get_template('app/survey/base_form.html')
    if request.user.is_authenticated():
      inputs = get_inputs_by_person(item_container.item, request.user.id)
      texts  = get_texts_by_person(item_container.item, request.user.id)
    else:
      inputs = texts = {}
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
      form_objs.append(get_form_tab_row(ic, user, user_org, inputs, texts))
    if this_section != {}:
      this_section['forms'] = form_objs
      objs.append(this_section)
    form_context = Context (  { 'form_is_active': item_container.item.integer_2,
                                'objs': objs,
                                'submit': item_container.item.string_1,
                                'survey_id': item_container.item.id,
                                'separator': SEPERATOR_ICON,
                                'count': get_count(item_container),
                                'now': datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

                              } )
    return t_form.render(form_context)

  app_name = 'survey'
  user = request.user
  if user.username != 'anonymous':
    user_org = get_org_by_username(user.username)
  else:
    user_org = None
  post = []
  error_ids = []
  ics, sections, d_sections = get_folder_content(item_container, False, ['dmsSurveyItem'])
  if request.POST.has_key('survey_id') and int(request.POST['survey_id']) == item_container.item.id:
    post = request.POST.copy()
    error_ids = has_complete_data(item_container, ics, post)
    if error_ids == []:
      post = clean_data(post)
      save_survey(item_container, ics, post, user, user_org)
      send_survey(item_container, ics, post, user, user_org)
      return show_success(item_container, ics, post)
    else:
      return show_incomplete_data(error_ids)
  else:
    user_perms = UserEditPerms(user.username, request.path)
    vars = get_folderish_vars_show(request, item_container, app_name, '',
                                   get_admin_options(item_container, user_perms))
    vars['text_bottom'] = get_form(item_container, ics, sections, d_sections, post)
    vars['user_support_header'] = _('Steuerung')
    return render_to_response('base.html', vars)

