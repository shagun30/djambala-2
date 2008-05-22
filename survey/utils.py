# -*- coding: utf-8 -*-
"""
/dms/survey/utils.py

.. enthaelt Hilfefunktionen fuer das E-Mail-Formular
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.01.2008  Beginn der Arbeit
0.02  19.01.2008  get_admin_options
"""

import string
import xml.dom.minidom

from django.template.loader import get_template
from django.template    import Context

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

# -----------------------------------------------------
def get_admin_options(item_container, user_perms):
  """ Personen mit manager-Rechten koennen bestimmte Optionen auswaehlen """
  if not user_perms.perm_manage:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/survey/admin_options.html')
  if item_container.item.integer_2:
    reset_option = False
  else:
    reset_option = True
  cSection = Context ({ 'path': get_site_url(item_container, ''), 'reset_option': reset_option})
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_form_tab_row(item_container, user, user_org, inputs, texts):
  """ baut eine Eingabeelement zusammen """
  input = text = ''
  for i in inputs:
    if i.question_id == item_container.item.id:
      if item_container.item.string_1 == 'checkbox':
        if input != '':
          input += '\n'
        input += i.value
      else:
        input = i.value
        break
  for t in texts:
    if t.question_id == item_container.item.id:
      text = t.value

  if user.is_authenticated() and user_org != None:
    name = item_container.item.name[:-5]  # .html abschneiden
    if name=='sex':
      if user.sex == _(u'm'):
        default = _(u'Herr')
      elif user.sex == _(u'w'):
        default = _(u'Frau')
      else:
        default = ''
    elif name=='first_name':
      default = user.first_name
    elif name=='last_name':
      default = user.last_name
    elif name=='title':
      default = user.title
    elif name=='email':
      default = user.email
    elif name=='username':
      default = user.username
    elif name=='organisation':
      default = user_org.organisation
    elif name=='sub_organisation':
      default = user_org.sub_organisation
    elif name=='street':
      default = user_org.street
    elif name=='zip':
      default = user_org.zip
    elif name=='town':
      default = user_org.town
    elif name=='phone':
      default = user_org.phone
    elif name=='fax':
      default = user_org.fax
    elif name=='homepage':
      default = user_org.homepage
    elif input != '':
      default = input
    elif text != '':
      default = text
    else:
      default = item_container.item.text_more
  else:
    default = item_container.item.text_more
  if item_container.item.string_1 == 'input':
    t_form = get_template('app/survey/input.html')
    context = Context ( { 'header': item_container.item.title,
                            'info': item_container.item.sub_title,
                            'maxlength': item_container.item.integer_2,
                            'size': item_container.item.integer_3,
                            'default': default,
                            'required': item_container.item.integer_1,
                            'name': item_container.item.id } )
  elif item_container.item.string_1 == 'text':
    t_form = get_template('app/survey/text.html')
    context = Context ( { 'header': item_container.item.title, 
                          'info': item_container.item.sub_title,
                          'default': default,
                          'cols': item_container.item.integer_4,
                          'rows': item_container.item.integer_5,
                          'required': item_container.item.integer_1,
                          'name': item_container.item.id } )
  elif item_container.item.string_1 in ['radio', 'checkbox']:
    if item_container.item.string_1 == 'radio':
      t_form = get_template('app/survey/radio.html')
    else:
      t_form = get_template('app/survey/checkbox.html')
    keys = string.splitfields(item_container.item.text.strip().replace('<p>','').replace('</p>',''), '\n')
    options = []
    defaults = string.splitfields(default, '\n')
    for key in keys:
      key = key.strip()
      if key != '':
        if key in defaults:
          options.append( {'name': key, 'checked': True, } )
        else:
          options.append( {'name': key, } )
    context = Context ( { 'header': item_container.item.title,
                          'info': item_container.item.sub_title,
                          'options': options,
                          'required': item_container.item.integer_1,
                          'name': item_container.item.id } )
  return t_form.render(context)

