# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/views_show.py

.. zeigt die Inhalte der Fortbildungsdatenbank an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.02.2008  Beginn der Arbeit
0.02  20.02.2008  gueltig
0.03  21.02.2008  Anzeige der Details
0.04  22.02.2008  Anmeldeformular
"""

from django.template.loader import get_template
from django.template    import Context
from django             import newforms as forms
from django.shortcuts   import render_to_response
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.utils          import get_tabbed_form
from dms.utils          import encode_email

from dms.queries        import get_org_by_username

from dms.hessen.trainingdb.queries    import get_veranstaltung_count
from dms.hessen.trainingdb.queries    import get_veranstaltung_by_iq_id
from dms.hessen.trainingdb.queries    import get_faecher_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_zielgruppen_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_schularten_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_fach_by_name

from dms.hessen.trainingdb.utils      import has_search_items
from dms.hessen.trainingdb.utils      import get_form_list
from dms.hessen.trainingdb.utils      import get_fach_choices
from dms.hessen.trainingdb.utils      import get_gueltig_choices
from dms.hessen.trainingdb.utils      import get_schulart_choices
from dms.hessen.trainingdb.utils      import get_zielgruppe_choices
from dms.hessen.trainingdb.utils      import get_anbieter_choices
from dms.hessen.trainingdb.utils      import get_datum
from dms.hessen.trainingdb.utils      import get_schularten_str
from dms.hessen.trainingdb.utils      import get_zielgruppen_str
from dms.hessen.trainingdb.utils      import get_faecher_str
from dms.hessen.trainingdb.utils      import get_veranstaltungen_by_filter

from dms.hessen.trainingdb.schools    import views_schulen
from dms.hessen.trainingdb.views_flyer  import trainingdb_show_flyer
from dms.hessen.trainingdb.views_email  import trainingdb_show_email

from dms.hessen.trainingdb.help_form  import help_form

from dms.views_error      import show_error
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def trainingdb_show_training(request, item_container, veranst_iq_id):
  """ zeigt Einzelveranstaltung der Fortbildungsdatenbank """

  item = get_veranstaltung_by_iq_id(veranst_iq_id)
  if item == None:
    return show_error(request, item_container, _('Falsche Veranstaltungsnummer'),
                          _(u'<p>Zu dieser Veranstaltungsnummer gibt es keine Veranstaltung (mehr)!</p>'))
  if item[0].veranst_status in ['', 'freigegeben']:
    veranst_status = ''
  else:
    veranst_status = item[0].veranst_status
  anbieter = '%s<br />%s<br />%s %s' % (item[1].anbieter_name,
                                        item[1].anbieter_strasse,
                                        item[1].anbieter_plz,
                                        item[1].anbieter_ort)

  class DmsItemForm(forms.Form):
    """ Elemente des Anmeldeformulars """
    vorname = forms.CharField(
         widget=forms.TextInput(attrs={'size':40, 'max_length':60}) )
    nachname = forms.CharField(
         widget=forms.TextInput(attrs={'size':40, 'max_length':60}) )
    personalnummer = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':20, 'max_length':10}) )
    strasse = forms.CharField(
         widget=forms.TextInput(attrs={'size':40, 'max_length':60}) )
    plz = forms.CharField(
         widget=forms.TextInput(attrs={'size':10, 'max_length':10}) )
    ort = forms.CharField(
         widget=forms.TextInput(attrs={'size':50, 'max_length':80}) )
    telefon = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':20, 'max_length':20}) )
    email = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':50, 'max_length':120}) )
    school_name = forms.CharField(
         widget=forms.TextInput(attrs={'size':50, 'max_length':80}) )
    school_ort = forms.CharField(
         widget=forms.TextInput(attrs={'size':50, 'max_length':80}) )
    school_telefon = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':20, 'max_length':20}) )
    school_no = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':10, 'max_length':4}) )
    zusatz = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':5, 'cols':40, 'style':'width:100%;'}) )
    uebernachtung = forms.BooleanField()
    v_thema = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_thema}))
    v_intern_id = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_intern_id}))
    v_iq_id = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_iq_id}))
    v_anbieter = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':anbieter}))
    v_datum = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':get_datum(item)}))
    v_punkte = forms.CharField(required=False,
         widget=forms.HiddenInput(attrs={'value':item[0].veranst_punkte}))

  app_name = u'trainingdb'
  user = request.user
  if user.is_authenticated():
    org = get_org_by_username(user.username)
    if org.org_id > 0:
      org_id = org.org_id
    else:
      org_id = ''
    data_init = {
              'vorname': user.first_name,
              'nachname': user.last_name,
              'email': user.email,
              'school_name': org.organisation,
              'school_ort': org.town,
              'school_telefon': org.phone,
              'school_no': org_id,
              'uebernachtung': False,
            }
  else:
    data_init = { 'uebernachtung': False, 
                }
  # --- Sind Daten im Anmeldeformular vorhanden?
  show_errors = (request.method=='POST')
  if show_errors:
    data = request.POST.copy()
  else:
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  # --- Formulardaten per E-Mail versenden
  if not f.errors:
    return trainingdb_show_email(request, item_container, data, item)
  if veranst_status != '':
    formular_daten = ''
  else:
    tabs = [ ('tab_school_person', [ 'school_no', 'school_name', 'school_ort', 'school_telefon',
                              'vorname', 'nachname', 'personalnummer',
                              'strasse', 'plz', 'ort',
                              'telefon', 'email' ] ),
            ('tab_zusatz', [ 'zusatz', 'uebernachtung', ] ),
            ('tab_veranstaltung', [ 'v_anbieter', 'v_thema', 'v_datum', 'v_punkte',
                              'v_iq_id', 'v_intern_id'] ),
          ]
    formular_daten = get_tabbed_form(tabs, help_form, app_name, f)

  t_details = get_template('app/hessen/trainingdb/show_details.html')
  t_anmeldung = get_template('app/hessen/trainingdb/show_anmeldung.html')
  # --- Zeitraum zusammenbauen
  if item[0].veranst_anmeldung != None:
    anmeldung = item[0].veranst_anmeldung.strftime('%d.%m.%Y')
  else:
    anmeldung = ''
  vars_details = {
                   'thema': item[0].veranst_thema,
                   'beschreibung': mark_safe(item[0].veranst_beschreibung.replace('\n', '<br />\n')),
                   'zeitraum': get_datum(item),
                   'anmeldung': anmeldung,
                   'faecher': get_faecher_str(get_faecher_by_veranst_iq_id(veranst_iq_id)),
                   'zielgruppen': get_zielgruppen_str(get_zielgruppen_by_veranst_iq_id(veranst_iq_id)),
                   'schularten': get_schularten_str(get_schularten_by_veranst_iq_id(veranst_iq_id)),
                   'veranst_ort': item[0].veranst_ort,
                   'veranst_punkte': item[0].veranst_punkte,
                   'veranst_kosten': item[0].veranst_kosten,
                   'veranst_intern_id': item[0].veranst_intern_id,
                   'veranst_iq_id': item[0].veranst_iq_id,
                   'veranst_hinweise': mark_safe(item[0].veranst_hinweise.replace('\n', '<br />\n')),
                   'veranst_zusatz': mark_safe(item[0].veranst_zusatz.replace('\n', '<br />\n')),
                   'veranst_url': item[0].veranst_url,
                   'veranst_url_text': item[0].veranst_url_text,
                   'veranst_leitung': item[0].veranst_leitung,
                   'veranst_dozenten': item[0].veranst_dozenten,
                   'veranst_fest_teilnehmer': item[0].veranst_feste_teilnehmer,
                   'veranst_status': veranst_status,
                   'veranst_v_art': item[2].v_art_name,
                   'anbieter_url': item[1].anbieter_url,
                   'anbieter_name': item[1].anbieter_name,
                   'anbieter_person': item[1].anbieter_person,
                   'anbieter_strasse': item[1].anbieter_strasse,
                   'anbieter_plz': item[1].anbieter_plz,
                   'anbieter_ort': item[1].anbieter_ort,
                   'anbieter_telefon': item[1].anbieter_telefon,
                   'anbieter_fax': item[1].anbieter_fax,
                   'anbieter_email': item[1].anbieter_email,
                 }
  vars = get_item_vars_show(request, item_container, app_name)
  vars['thema'] = item[0].veranst_thema
  vars['details'] = t_details.render(Context(vars_details))
  vars_anmeldung = { 'formular_daten': formular_daten,
                     'veranst_status': veranst_status,
                     'submit': _(u'Online anmelden'),
                   }
  vars['anmeldeformular'] = t_anmeldung.render(Context(vars_anmeldung))
  vars['veranst_iq_id'] = veranst_iq_id
  vars['errors'] = show_errors and f.errors != {}
  #assert False
  return render_to_response ( 'app/hessen/trainingdb/show_training.html', vars )

# -----------------------------------------------------
def trainingdb_show(request, item_container):
  """ zeigt Suchformular für Fortbildungsdatenbank """

  def get_tabs(request, item_container, simple_mode):
    """ """
    tabs = [ ('tab_faecher', [ 'training_text', 'training_fach', ] ), ]
    if item_container.item.integer_1 < 1:
      tabs.append(('tab_gueltig', [ 'training_gueltig', ] ))
    tabs.append(('tab_schularten', [ 'training_schulart', ] ))
    tabs.append(('tab_zielgruppen', [ 'training_zielgruppe', ] ))
    if not simple_mode and item_container.item.string_1 == '':
      tabs.append(('tab_anbieter', [ 'training_anbieter', ] ))
    tabs.append(('tab_weiteres', [ 'training_iq_nummer', 'training_intern_nummer' ] ))
    return tabs

  show_errors = (request.method=='POST')
  data = {}
  if show_errors:
    data = request.POST.copy()
  get = request.GET.copy()
  if get.has_key('school_op'):
    return views_schulen(request, item_container, get['school_op'])
  elif get.has_key('school_flyer'):
    return trainingdb_show_flyer(request, item_container, get['school_flyer'])
  simple_mode = (item_container.item.integer_1 < 1 and not get.has_key('ext_options'))
  # --- wurden Parameter direkt uebergeben?
  # --- Problem: ID der Namen in dms und in Fortbildungsdatenbank koennen unterschiedlich sein!!!
  # --- Deshalb: Namen anstelle der IDs
  if request.GET.has_key('fach'):
    data['training_fach'] = int(request.GET['fach'])
  if request.GET.has_key('schulart'):
    data['training_schulart'] = int(request.GET['schulart'])
  if request.GET.has_key('freie_suche'):
    data['training_text'] = request.GET['freie_suche']
  if request.GET.has_key('anbieter'):
    data['training_anbieter'] = request.GET['anbieter']
    simple_mode = False
  
  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    training_fach = forms.CharField(required=False,
         widget=forms.Select(choices=get_fach_choices(item_container),
                             attrs={'size':20, 'style':'width:100%'} ) )
    training_text = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':40, 'max_length':120}) )
    training_gueltig = forms.CharField(required=False,
         widget=forms.Select(choices=get_gueltig_choices(),
                             attrs={'size':20, 'style':'width:100%'} ) )
    training_schulart = forms.CharField(required=False,
         widget=forms.Select(choices=get_schulart_choices(item_container),
                             attrs={'size':20, 'style':'width:100%'} ) )
    training_zielgruppe = forms.CharField(required=False,
         widget=forms.Select(choices=get_zielgruppe_choices(item_container),
                             attrs={'size':20, 'style':'width:100%'} ) )
    training_iq_nummer = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':10, 'max_length':20}) )
    training_intern_nummer = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':10, 'max_length':20}) )
    if not simple_mode:
      training_anbieter = forms.CharField(required=False,
          widget=forms.Select(choices=get_anbieter_choices(item_container),
                              attrs={'size':20, 'style':'width:100%'} ) )

  app_name = u'trainingdb'
  # --- Sind Daten vorhanden?
  #if request.GET.has_key('region'):
  #  data = { 'training_gueltig': int(request.GET['region']), }
  vars = get_item_vars_show(request, item_container, app_name)
  # Daten einer Einzelveranstaltung anzeigen
  if request.GET.has_key('show_training'):
    return trainingdb_show_training(request, item_container, request.GET['show_training'])
  elif has_search_items(data) or item_container.item.integer_1 > 0 or item_container.item.string_1 > '':
    if item_container.item.integer_1 > 0:
      data['training_gueltig'] = item_container.item.integer_1
    if item_container.item.string_1 > '':
      data['training_anbieter'] = item_container.item.string_1
    items = get_veranstaltungen_by_filter(data)
    ret = []
    for item in items:
      if item.veranst_datum_von != None:
        datum = item.veranst_datum_von.strftime('%m/%d/%Y')
      else:
        datum = None
      ret.append({'iq_id': item.veranst_iq_id,
                  'thema': item.veranst_thema,
                  'anbieter': item.anbieter_name,
                  'kosten': item.veranst_kosten,
                  'datum': datum,
                  })
    vars['objs'] = ret
    vars['base_url'] = item_container.get_absolute_url()
    vars['count'] = len(ret)
    vars['title'] = _(u'Suchergebnisse in der hessischen Fortbildungsdatenbank')

    # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
    f = DmsItemForm(data)
    tabs = get_tabs(request, item_container, simple_mode)
    my_form = get_tabbed_form(tabs, help_form, app_name, f)
    content = my_form
    vars['submit'] = _(u'Suche starten')
    vars['content'] = content
    vars['show_frame_left'] = True
    vars['count_total'] = get_veranstaltung_count(item_container)
    # --- Formular anzeigen
    return render_to_response ( 'app/hessen/trainingdb/trainings.html', vars )
  else:
    # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
    f = DmsItemForm(data)
    tabs = get_tabs(request, item_container, simple_mode)
    my_form = get_tabbed_form(tabs, help_form, app_name, f)
    content = my_form
    vars['submit'] = _(u'Suche starten')
    vars['content'] = content
    vars['show_frame_left'] = True
    vars['count'] = get_veranstaltung_count(item_container)
    vars['slot_right_info'] = item_container.item.info_slot_right
    # --- Formular anzeigen
    return render_to_response ( 'app/hessen/trainingdb/base_edit.html', vars )

