# -*- coding: utf-8 -*-
"""
/dms/edufileitem/views_add.py

.. enthaelt den View zum Ergaenzen einer Datei in den Lernarchiven
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

Belegung der Joker-Felder in DmsItem:
  string_1  = quelle_id
  string_2  = lokal_id
  integer_1 = community_id
  integer_2 = schulverbund_id
  integer_3 = lern_res_typ_id
  integer_4 = medienformat_id
  integer_5 = zertifikat_id

0.01  07.09.2007  Beginn der Arbeit
0.02  28.11.2007  eigenes Logo setzen
"""

import datetime
import time

from django.utils.translation import ugettext as _

from dms.auth.decorators    import login_required
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from dms.settings       import EDUFOLDER_SOURCE
from dms.settings       import EDUFOLDER_LANGUAGE

from dms.queries        import get_site_url
from dms.edufolder.utils    import get_alter_choices

from dms.models         import DmsItem
from dms.edufolder.models   import DmsEduItem
from dms.edufolder.utils    import get_org_image_url
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices, check_name
from dms.utils          import get_license_choices
from dms.mail           import send_control_email
from dms.utils_form     import get_item_vars_add

from dms.queries        import save_item_values
from dms.queries        import set_extra_data
from dms.queries        import get_edu_sprache_id

from dms.encode_decode  import encode_html

from dms.edulinkitem.utils       import get_lernrestyp_choices
from dms.edulinkitem.utils       import get_medienformat_choices
from dms.edulinkitem.utils       import get_schlagworte_by_path
from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_sprachen_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import get_faecher_by_schlagworte
from dms.edulinkitem.utils       import get_schulart_by_schlagworte
from dms.edulinkitem.utils       import save_schlagworte

from dms.edufileitem.help_form   import help_form

from dms.file.utils     import save_file

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@login_required
def edufileitem_add(request, item_container):
  """ neue Datei fuer Lernarchiv anlegen """

  def save_values(name, new, files, item_container):
    """ Daten sichern """
    save_file(name, files, item_container)
    community_id = 0
    schulverbund_id = 0
    new['is_exchangeable'] = item_container.item.is_exchangeable
    new['string_1']  = EDUFOLDER_SOURCE
    new['string_2']  = ''
    new['integer_1'] = community_id
    new['integer_2'] = schulverbund_id
    new['integer_3'] = new['lernrestyp']
    new['integer_4'] = new['medienformat']
    new['integer_5'] = 1  # zertifikat_id
    new['extra']     = set_extra_data(schlagwort_org=encode_html(new['schlagwort']))
    # eigenes Logo setzen
    image_url, image_url_url, image_extern = get_org_image_url(new['url_more'], True)
    new['image_url'] = image_url
    new['image_url_url'] = image_url_url
    new['image_extern'] = image_extern
    item_container_new = save_item_values(request.user, 'dmsEduFileItem', name, new,
                                          item_container,
                                          not item_container.item.is_moderated, False)
    edu_item = DmsEduItem.save_values(DmsEduItem(), item_container_new, new, True)
    for i in new['fach_sachgebiet']:
      edu_item.fach_sachgebiet.add(i)
    for i in new['schulart']:
      edu_item.schulart.add(i)
    for i in new['schulstufe']:
      edu_item.schulstufe.add(i)
    for i in new['sprache']:
      edu_item.sprache.add(i)
    for i in new['zielgruppe']:
      edu_item.zielgruppe.add(i)
    save_schlagworte(edu_item, new)
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    fname       = forms.CharField(required=False, max_length=200,
         widget=forms.FileInput(attrs={'size':40}) )
    title      = forms.CharField(max_length=240,
         widget=forms.TextInput(attrs={'size':60}) )
    url_more   = forms.CharField(required=False, max_length=200,
         widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta',
                                      'style':'width:100%;'}) )
    lernrestyp = forms.CharField(
         widget=forms.Select(choices=get_lernrestyp_choices(),
                             attrs={'style':'width:60%'} ) )
    medienformat = forms.CharField(
         widget=forms.Select(choices=get_medienformat_choices(),
                             attrs={'style':'width:60%'} ) )
    titel_lang = forms.CharField(required=False, max_length=240,
         widget=forms.TextInput(attrs={'size':60}) )
    beschreibung_lang = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':12, 'cols':60, 'id':'ta1',
                                      'style':'width:100%;'}) )
    schlagwort = forms.CharField(required=False,
         widget=forms.Textarea( attrs={'rows':4, 'cols':40, 'style':'width:60%;'}) )
    sprache    = forms.MultipleChoiceField(required=False, choices=get_sprachen_list(),
         widget=forms.CheckboxSelectMultiple() )
    lernziel   = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta2',
                                      'style':'width:100%;'}) )
    lernzeit   = forms.CharField(required=False, max_length=20,
         widget=forms.TextInput(attrs={'size':20}) )
    methodik   = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta3',
                                      'style':'width:100%;'}) )
    lehrplan   = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta4',
                                      'style':'width:100%;'}) )
    standards_kmk = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta5',
                                      'style':'width:100%;'}) )
    standards_weitere = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta6',
                                      'style':'width:100%;'}) )
    fach_sachgebiet   = forms.MultipleChoiceField(required=False,
         choices=get_fach_list(),
         widget=forms.CheckboxSelectMultiple() )
    zielgruppe = forms.MultipleChoiceField(required=False,
         choices=get_zielgruppen_list(),
         widget=forms.CheckboxSelectMultiple() )
    schulstufe = forms.MultipleChoiceField(required=False,
         choices=get_schulstufen_list(),
         widget=forms.CheckboxSelectMultiple() )
    schulart   = forms.MultipleChoiceField(required=False,
         choices=get_schularten_list(),
         widget=forms.CheckboxSelectMultiple() )
    autor      = forms.CharField(required=False, max_length=120,
         widget=forms.TextInput(attrs={'size':60}) )
    herausgeber = forms.CharField(required=False, max_length=240,
         widget=forms.TextInput(attrs={'size':60}) )
    publikations_datum = forms.CharField(required=False, max_length=30,
         widget=forms.TextInput(attrs={'size':20}) )
    isbn       = forms.CharField(required=False, max_length=20,
         widget=forms.TextInput(attrs={'size':20}) )
    rechte     = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':6, 'cols':60, 'id':'ta7',
                                      'style':'width:100%;'}) )
    anbieter_herkunft = forms.CharField(required=False, max_length=240,
         widget=forms.TextInput(attrs={'size':60}) )
    preis      = forms.CharField(required=False, max_length=20,
         widget=forms.TextInput(attrs={'size':20}) )
    techn_voraus = forms.CharField(required=False,
         widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta8',
                                      'style':'width:100%;'}) )
    image_url  = forms.CharField(required=False, max_length=200,
         widget=forms.TextInput(attrs={'size':60}) )
    image_url_url = forms.URLField(required=False, max_length=200,
         widget=forms.TextInput(attrs={'size':60}) )
    image_extern = forms.BooleanField(required=False)
    section    = forms.CharField(required=False,
         widget=forms.Select(choices=
                 get_section_choices(item_container.container.sections),
                 attrs={'size':4, 'style':'width:60%'} ) )
    is_browseable   = forms.BooleanField(required=False)
    visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
         widget=forms.TextInput(attrs={'size':10}))
    visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
         widget=forms.TextInput(attrs={'size':10}))
    alter_min  = forms.ChoiceField(choices=get_alter_choices(),
                       widget=forms.RadioSelect() )
    alter_max  = forms.ChoiceField(choices=get_alter_choices(),
                       widget=forms.RadioSelect() )
    license         = forms.ChoiceField(choices=get_license_choices(item_container),
         widget=forms.RadioSelect() )

  app_name = 'edufileitem'
  my_title = _(u'Datei im Lernarchiv anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialisiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    schlagworte_str, schlagworte = get_schlagworte_by_path(item_container)
    faecher = get_faecher_by_schlagworte(schlagworte)
    zielgruppen = [3, 4, 5]
    schulart, schulstufe = get_schulart_by_schlagworte(schlagworte)
    #schulart = [1, 2, 3]
    #schulstufe = [3,4]
    sprache = [get_edu_sprache_id(EDUFOLDER_LANGUAGE)]
    this_year = int(datetime.datetime.now().strftime ( '%Y' ))
    rights = _(u'Diese Ressource kann für unterrichtliche Zwecke genutzt werden.'),
    data = { 'license': 1,
             'lernrestyp': 4,
             'medienformat': 5,
             'schlagwort': schlagworte_str,
             'sprache': sprache,
             'fach_sachgebiet': faecher, 
             'schulart': schulart, 
             'schulstufe': schulstufe, 
             'zielgruppe': zielgruppen, 
             'rechte': rights,
             'is_browseable': True,
             'visible_start': datetime.date.today(), 
             'visible_end': datetime.date(int(this_year)+10,12,31),
             'alter_min': -1,
             'alter_max': -1
           }
  f = DmsItemForm(data)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  if item_container.container.sections.strip() != '':
    base = ('tab_base', [ 'lernrestyp', 'title', 'fname', 'text',
                          'section', 'schlagwort', ])
  else:
    base = ('tab_base', [ 'lernrestyp', 'title', 'text', 'fname', 'schlagwort', ])
  tabs = [ base,
           ('tab_course',      [ 'fach_sachgebiet',]),
           ('tab_pupil',       [ 'titel_lang', 'beschreibung_lang', 'alter_min', 'alter_max' ]),
           ('tab_details',     [ 'zielgruppe', 'schulstufe', 'schulart']),
           ('tab_paed',        [ 'lernzeit', 'lernziel', 'methodik', 'lehrplan', 
                                 'standards_kmk', 'standards_weitere', ]),
           ('tab_description', [ 'url_more', 'medienformat', 'sprache', ]),
           ('tab_formal',      [ 'autor', 'herausgeber', 'publikations_datum', 'isbn',
                                 'anbieter_herkunft', 'preis', 'rechte', 'techn_voraus'
                               ]),
           ('tab_image',       [ 'image_url', 'image_url_url', 'image_extern', ] ),
           ('tab_license',     [ 'license', ] ),
           ('tab_visibility',  [ 'is_browseable', 'visible_start', 'visible_end', ] ),
          ]

  content = get_tabbed_form(tabs, help_form, app_name, f)
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    new = f.cleaned_data
    name = check_name(request.FILES['fname']['filename'], True)
    save_values(name, new, request.FILES, item_container)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else:
    commands = { 'show_mode': True, 'image_mode': True, }
    vars = get_item_vars_add(request, item_container, app_name, my_title, 
                             content, show_errors, commands)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response('app/file/manage_edit.html', vars)
