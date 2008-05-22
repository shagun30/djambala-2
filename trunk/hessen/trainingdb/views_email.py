# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/views_email.py

.. sendet Daten der Online-Anmeldung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.02.2008  Beginn der Arbeit
0.02  29.02.2008  Versenden der Online-Anmeldung
0.03  04.03.2008  bulkmail
"""

import tempfile, os
from dms.settings       import BULK_EMAIL_PATH

from django.template.loader   import get_template
from django.template          import Context
from django.core.mail         import EmailMultiAlternatives
from django                   import newforms as forms
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.settings       import CONTROL_EMAIL
from dms.mail           import createhtmlmail
from dms.utils_form     import get_item_vars_show
from dms.utils          import get_tabbed_form
from dms.hessen.trainingdb.queries    import get_anbieter_by_iq_id
from dms.hessen.trainingdb.utils      import get_datum

from dms.hessen.trainingdb.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def do_send_email(request, item_container, data, item):
  """ """
  tForm = get_template('app/hessen/trainingdb/send_data.html')
  tForm_text = get_template('app/hessen/trainingdb/send_data_text.html')
  anbieter_iq_id = item[0].veranst_anbieter_iq_id
  anbieter = get_anbieter_by_iq_id(anbieter_iq_id)
  data['uebernachtung'] = (data['uebernachtung'] == u'on')
  data['anmelde_email'] = anbieter.anbieter_email
  content = Context(data)
  subject = '[Anmeldung] Veranstaltung %s' % data['v_intern_id']
  from_addr = CONTROL_EMAIL
  to_addr = [anbieter.anbieter_email]
  #Test: to_addr = ['hans.rauch@gmx.net']
  if data['email'].find('@') > 0:
    to_addr.append(data['email'])
  email_body = tForm.render(content)
  email_body_text = tForm_text.render(content)
  msg = EmailMultiAlternatives(subject, email_body_text, from_addr, to_addr)
  msg.attach_alternative(email_body, 'text/html')
  msg.send()

  app_name = u'trainingdb'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['next'] = item_container.get_parent().get_absolute_url()
  return render_to_response('app/hessen/trainingdb/success.html', vars)

# -----------------------------------------------------
def trainingdb_show_email(request, item_container, data, item):
  """ zeigt die Daten der Online-Anmeldung """

  class DmsItemForm(forms.Form):
    """ Elemente des Anmeldeformulars """
    vorname = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['vorname']}) )
    nachname = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['nachname']}) )
    personalnummer = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['personalnummer']}) )
    strasse = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['strasse']}) )
    plz = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['plz']}) )
    ort = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['ort']}) )
    telefon = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['telefon']}) )
    email = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['email']}) )
    school_name = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['school_name']}) )
    school_ort = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['school_ort']}) )
    school_telefon = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['school_telefon']}) )
    school_no = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['school_no']}) )
    zusatz = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value': data['zusatz']}) )
    uebernachtung = forms.BooleanField(required=False,
         widget=forms.HiddenInput(attrs={'value': data.has_key('uebernachtung')}) )
    v_thema = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_thema}))
    v_intern_id = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_intern_id}))
    v_iq_id = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_iq_id}))
    v_anbieter = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':data['v_anbieter']}))
    v_datum = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':get_datum(item)}))
    v_punkte = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_punkte}))

  app_name = u'trainingdb'
  send_email_str = _(u'Online-Anmeldung tatsächlich versenden')
  if data.has_key('submit') and data['submit'] == send_email_str+' ...':
    return do_send_email(request, item_container, data, item)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  if not f.errors:
    tabs = [('tab_schule2', [ 'school_no', 'school_name', 'school_ort', 'school_telefon', ] ),
            ('tab_person2', [ 'vorname', 'nachname', 'personalnummer',
                              'strasse', 'plz', 'ort',
                              'telefon', 'email' ] ),
            ('tab_zusatz2', [ 'zusatz', 'uebernachtung', ] ),
            ('tab_veranstaltung', [ 'v_anbieter', 'v_thema', 'v_datum', 'v_punkte',
                              'v_iq_id', 'v_intern_id'] ),
          ]
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text'] = _(u'<p>Hier noch einmal Ihre Daten:</p>')
    vars['submit'] = send_email_str
    vars['content'] = get_tabbed_form(tabs, help_form, app_name, f)
    # --- Formular anzeigen
    return render_to_response ( 'app/base_edit.html', vars )
