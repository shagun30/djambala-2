# -*- coding: utf-8 -*-
"""
/dms/userregistration/views_show.py

.. zeigt den Inhalt der User-Rgistrierung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.06.2007  Beginn der Arbeit
0.02  26.06.2007  Vorlaeufiger Abschluss: ohne Versand der PDF-Dateien
"""

import datetime, os

from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.newforms.util import ValidationError
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.settings import TMP_PATH

from dms.auth.models    import User
from dms.models         import DmsUserOrg

from dms.queries        import get_site_url
from dms.queries        import get_org_by_org_id
from dms.queries        import get_user_by_email

from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_item_vars_add

from dms.userfolder.utils           import is_pupil

from dms.userregistration.utils     import get_school_section
from dms.userregistration.utils     import get_institutions_section
from dms.userregistration.utils     import get_edu_institutions_section
from dms.userregistration.utils     import get_items
from dms.userregistration.utils     import get_sex_choices
from dms.userregistration.utils     import get_username

from dms.userregistration.help_form   import help_form
from dms.userregistration.pdf_confirm import pdfConfirm
from dms.userregistration.pdf_saved_infos import pdfSavedInfos
from dms.userregistration.pdf_send    import pdfSend

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def userregistration_show(request, item_container):
  """ zeigt die moeglichen Optionen zur Community-Verwaltung """
  from django.template.loader import get_template
  from django.template import Context

  @transaction.commit_manually
  def save_values(org_id, new, item_container):
    """ """
    user = User()
    username = get_username('', new['first_name'].strip(), new['last_name'].strip())
    user.username = username
    user.sex = new['sex']
    user.first_name = new['first_name']
    user.last_name = new['last_name']
    user.email = new['email']
    user.title = new['title_name']
    user.is_staff = False
    user.is_active = False
    user.is_superuser = False
    user.date_joined = datetime.datetime.now()
    user.set_password(new['password1'])
    user.save()
    user_org = DmsUserOrg()
    user_org.user = user
    user_org.org_id = org_id
    user_org.save()
    transaction.commit()
    # --- E-Mails versenden: Backup-E-Mail sowie E-Mail mit zwei PDF-Dateien
    if not is_pupil('h.rauch'):
      params = {}
      params['user'] = 'h.rauch'
      params['vorname'] = new['first_name'].strip()
      params['nachname'] = new['first_name'].strip()
      params['titel'] = new['title_name'].strip()
      params['email'] = new['email'].strip()
      params['geschlecht'] = new['sex'].strip()
      params['kennwort'] = new['password1'].strip()
      org = get_org_by_org_id(this_org_id)
      params['d_org'] = org.organisation
      params['d_strasse'] = org.street
      params['d_plz'] = org.zip
      params['d_ort'] = org.town
      params['d_telefon'] = org.phone
      params['d_fax'] = org.fax
      params['org_id'] = org_id
      # --- PDF-Dateien erzeugen
      p = pdfConfirm()
      p.doIt(params)
      p = pdfSavedInfos()
      p.doIt(params)
      # --- und versenden
      p = pdfSend()
      p.doIt(params, True)
      # --- aufraeumen
      tmp_path = TMP_PATH + params['user']
      os.unlink ( tmp_path + "-bestaetigung.pdf" )
      os.unlink ( tmp_path + "-infos.pdf" )
  
    return username

  get_data = request.GET.copy()
  post_data = request.POST.copy()
  if get_data.has_key('org_id') or post_data.has_key('org_id'):
    this_org_id = int(get_data['org_id'])
    org = get_org_by_org_id(this_org_id)
    this_org_info = u'%s<br />%s<br />%s %s<br />%s: %s / %s: %s' % \
                   (org.organisation, org.street, org.zip, org.town, 
                    _(u'Telefon'), org.phone, _(u'Fax'), org.fax)
    class DmsItemForm(forms.Form):
      """ Elemente des Eingabeformulars """
      sex        = forms.ChoiceField(choices=get_sex_choices(),
                            widget=forms.RadioSelect() )
      first_name = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':30}) )
      last_name  = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':30}) )
      title_name = forms.CharField(required=False, max_length=10,
                        widget=forms.TextInput(attrs={'size':10}) )
      email      = forms.CharField(max_length=200,
                        widget=forms.TextInput(attrs={'size':50}) )
      password1  = forms.CharField(
                        widget=forms.PasswordInput(attrs={'size':30}) )
      password2  = forms.CharField(
                        widget=forms.PasswordInput(attrs={'size':30}) )
      org_info   = forms.CharField(required=False, widget=forms.HiddenInput(
                        attrs={'value':this_org_info}))
      def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
          raise ValidationError(_(u'Die beiden eingegebenen Kennwörter stimmen nicht überein!'))
        elif self.cleaned_data['password1'] != '' and len(self.cleaned_data['password2']) < 6:
          raise ValidationError(_(u'Das Kennwort muss mindestens sechs Zeichen lang sein!'))
        else:
          return self.cleaned_data['password2']
      def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_by_email(email) != None:
          raise ValidationError(_(u'Ihre angegebene E-Mail-Adresse wird bereits verwendet!'))
        else:
          return email
  else:
    this_org_id = 0


  app_name = 'userregistration'
  my_title = _(u'Registrierung als Community-Mitglied')

  vars = get_item_vars_show(request, item_container, app_name)
  if get_data.has_key('org_id') or post_data.has_key('org_id'):
    vars = get_item_vars_show(request, item_container, app_name)
    # --- Anmeldeformular
    # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
    show_errors = request.method == 'POST'
    if show_errors:
      data = request.POST.copy()
    else :
      data = {'sex': 'w', 'first_name': '', 'last_name': '', 'title_name': '',
              'email': '', 'password1': '', 'password2': '',}
    # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
    f = DmsItemForm(data)

    if not f.errors:
      # --- Daten speichern
      username = save_values(this_org_id, f.data, item_container)
      # --- Rueckmeldung geben
      tList = get_template('app/userregistration/results.html')
      cSection = Context ( { 'female': f.data['title_name']=='w',
                             'username': username, 
                             'title_name': f.data['title_name'],
                             'first_name': f.data['first_name'],
                             'last_name': f.data['last_name'],
                             'email': f.data['email'],
                             'next': get_site_url(item_container, 'index.html') } )
      c = tList.render(cSection)
      vars = get_item_vars_show(request, item_container, app_name)
      vars['title'] = _(u'Ihre Community-Zugangsdaten')
      vars['text'] = tList.render(cSection)
      vars['text_more'] = ''
      return render_to_response ( 'base-full-width.html', vars )
    tabs = [ ('tab_add_user', [ 'org_info',
                                'sex', 'first_name', 'last_name', 'title_name', 'email', 
                                'password1', 'password2', ]) ]
    content = get_tabbed_form(tabs, help_form, app_name, f, show_errors=show_errors)
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = item_container.get_absolute_url() + '?show_add_form=1&org_id=%i' % this_org_id
    return render_to_response ( 'app/base_edit.html', vars )
  elif get_data.has_key('inst_contains') or request.method == 'POST':
    # --- Zwischenauswahl
    items, search_title = get_items(get_data, post_data)
    tList = get_template('app/userregistration/section_table.html')
    cSection = Context ( { 'title': search_title, 'items': items } )
    c = tList.render(cSection)
    vars['content'] = tList.render(cSection)
    vars['title'] = _(u'1. Schritt der Registrierung')
    vars['sub_title'] = ''
    vars['text'] = ''
    vars['text_more'] = ''
    return render_to_response ( 'app/base_folderish.html', vars )
  else:
    # --- normale Startseite
    sections = ''
    sections += get_school_section()
    sections += get_edu_institutions_section()
    sections += get_institutions_section()
    vars['content'] = sections
    return render_to_response ( 'app/base_folderish.html', vars )
