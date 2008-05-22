# -*- coding: utf-8 -*-
"""
/dms/eduexerciseitem/views_add.py

.. enthaelt den View zum Ergaenzen einer Aufgabe
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.05.2008  Beginn der Arbeit
"""

import datetime

from django.utils.translation import ugettext as _

from dms.settings       import EDUFOLDER_SOURCE
from dms.settings       import EDUFOLDER_LANGUAGE

from django.db              import transaction
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from dms.settings       import EDUFOLDER_SOURCE
from dms.settings       import EDUFOLDER_LANGUAGE

from dms.edufolder.models   import DmsEduItem
from dms.edufolder.utils    import get_alter_choices

from dms.queries        import save_container_values
from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import get_edu_sprache_id
from dms.queries        import set_extra_data
from dms.queries        import get_medienformat_by_name
from dms.queries        import get_lernrestyp_by_name
from dms.queries        import save_item_values
from dms.mail           import send_control_email

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import check_name
from dms.utils          import get_section_choices
from dms.utils_form     import get_folderish_vars_add

from dms.edufolder.utils         import get_org_image_url
from dms.edulinkitem.utils       import get_schlagworte_by_path
from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_sprachen_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import get_faecher_by_schlagworte
from dms.edulinkitem.utils       import get_schulart_by_schlagworte
from dms.edulinkitem.utils       import save_schlagworte
from dms.edulinkitem.utils       import get_lernrestyp_choices

from dms.encode_decode  import encode_html
from dms.file.utils     import save_file

from dms.eduexerciseitem.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def eduexerciseitem_add(request, item_container):
  """ neue Aufgabe anlegen """

  #@transaction.commit_manually
  def save_values(name, new, files, item_container):
    """ Daten sichern """
    community_id = 0
    schulverbund_id = 0
    new['is_exchangeable'] = True
    new['nav_title'] = new['title']
    new['sections'] = _(u'Aufgabe\nLösungen\nMusterlösung\n')
    new['string_1']  = EDUFOLDER_SOURCE
    new['string_2']  = new['points']
    new['integer_1'] = community_id
    new['integer_2'] = schulverbund_id
    new['integer_3'] = get_lernrestyp_by_name(_(u'Aufgabe')).id
    new['integer_4'] = 6  # Internet
    new['integer_5'] = 1  # zertifikat_id
    new['integer_6'] = new['max_points']
    new['extra']     = set_extra_data(schlagwort_org=encode_html(new['schlagwort']))
    new['is_browseable'] = not item_container.item.is_moderated
    new['has_usersupport'] = item_container.item.has_user_support
    ## eigenes Logo setzen
    #image_url, image_url_url, image_extern = get_org_image_url('', True)
    #new['image_url'] = image_url
    #new['image_url_url'] = image_url_url
    #new['image_extern'] = image_extern
    item_container_new = save_container_values(request.user, 'dmsEduExerciseItem',
                                               name, new, item_container)
    edu_item = DmsEduItem.save_values(DmsEduItem(), item_container_new, new, True)
    if new.has_key('fach_sachgebiet'):
      for i in new['fach_sachgebiet']:
        edu_item.fach_sachgebiet.add(i)
    if new.has_key('schulart'):
      for i in new['schulart']:
        edu_item.schulart.add(i)
    if new.has_key('schulstufe'):
      for i in new['schulstufe']:
        edu_item.schulstufe.add(i)
    if new.has_key('sprache'):
      for i in new['sprache']:
        edu_item.sprache.add(i)
    if new.has_key('zielgruppe'):
      for i in new['zielgruppe']:
        edu_item.zielgruppe.add(i)
    save_schlagworte(edu_item, new)
    try:
      fname = check_name(files['fname']['filename'], True)
    except:
      fname = ''
    if fname != '':
      save_file(fname, files, item_container_new)
      new['string_1'] = new['text'] = u''
      new['section'] = _(u'Aufgabe')
      new['integer_1'] = new['integer_2'] = new['integer_3'] = new['integer_4'] = new['integer_5'] = -1
      new['integer_6'] = -1
      save_item_values(request.user, 'dmsFile', fname, new, item_container_new, True)
    #transaction.commit()
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    name       = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    titel_lang = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                         attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    beschreibung_lang = forms.CharField(required=False, widget=forms.Textarea(
                         attrs={'rows':8, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    schlagwort = forms.CharField(required=False, widget=forms.Textarea(
                         attrs={'rows':4, 'cols':40, 'style':'width:60%;'}) )
    sprache    = forms.MultipleChoiceField(required=False, choices=get_sprachen_list(),
                    widget=forms.CheckboxSelectMultiple() )
    lernziel   = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    lernzeit   = forms.CharField(required=False, max_length=20,
                       widget=forms.TextInput(attrs={'size':20}) )
    methodik   = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta3', 'style':'width:100%;'}) )
    lehrplan   = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta4', 'style':'width:100%;'}) )
    standards_kmk = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta5', 'style':'width:100%;'}) )
    standards_weitere = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta6', 'style':'width:100%;'}) )
    fach_sachgebiet   = forms.MultipleChoiceField(required=False,
         choices=get_fach_list(), widget=forms.CheckboxSelectMultiple() )
    zielgruppe = forms.MultipleChoiceField(required=False,
         choices=get_zielgruppen_list(), widget=forms.CheckboxSelectMultiple() )
    schulstufe = forms.MultipleChoiceField(required=False,
         choices=get_schulstufen_list(), widget=forms.CheckboxSelectMultiple() )
    schulart   = forms.MultipleChoiceField(required=False,
         choices=get_schularten_list(), widget=forms.CheckboxSelectMultiple() )
    autor      = forms.CharField(required=False, max_length=120,
                       widget=forms.TextInput(attrs={'size':60}) )
    herausgeber = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    publikations_datum = forms.CharField(required=False, max_length=30,
                       widget=forms.TextInput(attrs={'size':20}) )
    isbn       = forms.CharField(required=False, max_length=20,
                       widget=forms.TextInput(attrs={'size':20}) )
    rechte     = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':6, 'cols':60, 'id':'ta7', 'style':'width:100%;'}) )
    anbieter_herkunft = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    preis      = forms.CharField(required=False, max_length=20,
                       widget=forms.TextInput(attrs={'size':20}) )
    techn_voraus = forms.CharField(required=False, widget=forms.Textarea(
                       attrs={'rows':8, 'cols':60, 'id':'ta8', 'style':'width:100%;'}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                                           attrs={'size':4, 'style':'width:60%'} ) )
    is_browseable   = forms.BooleanField(required=False)
    visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
                            widget=forms.TextInput(attrs={'size':10}))
    visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
                            widget=forms.TextInput(attrs={'size':10}))
    max_points  = forms.IntegerField(min_value=-1, max_value=100,
                            widget=forms.TextInput(attrs={'size':5}) )
    points      = forms.CharField(required=False,
                     widget=forms.Textarea(attrs={'rows':5, 'cols':10,}) )
    alter_min  = forms.ChoiceField(choices=get_alter_choices(),
                       widget=forms.RadioSelect() )
    alter_max  = forms.ChoiceField(choices=get_alter_choices(),
                       widget=forms.RadioSelect() )

  app_name = 'eduexerciseitem'
  my_title = _(u'Aufgabe anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else :
    schlagworte_str, schlagworte = get_schlagworte_by_path(item_container)
    faecher = get_faecher_by_schlagworte(schlagworte)
    zielgruppen = [2, 3, 4, 5]
    schulart, schulstufe = get_schulart_by_schlagworte(schlagworte)
    sprache = [get_edu_sprache_id(EDUFOLDER_LANGUAGE)]
    this_year = int(datetime.datetime.now().strftime ( '%Y' ))
    rights = _(u'Diese Ressource kann für unterrichtliche Zwecke genutzt werden.')
    data = { 'schlagwort': schlagworte_str,
             'sprache': sprache,
             'fach_sachgebiet': faecher, 
             'schulart': schulart, 
             'schulstufe': schulstufe, 
             'zielgruppe': zielgruppen, 
             'rechte': rights,
             'is_browseable': True,
             'max_points': 0,
             'points': '1:\n2:\n3:\n4:\n5:\n',
             'visible_start': datetime.date.today(), 
             'visible_end': datetime.date(int(this_year)+10,12,31),
             'alter_min': -1,
             'alter_max': -1
           }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base',       [ 'name', 'title', 'text', 'fname',
                                'max_points', 'points', 'schlagwort', ]),
           ('tab_course',     [ 'fach_sachgebiet',]),
           ('tab_pupil',       [ 'titel_lang', 'beschreibung_lang', 'alter_min', 'alter_max' ]),
           ('tab_details',    [ 'zielgruppe', 'schulstufe', 'schulart']),
           ('tab_paed',       [ 'lernzeit', 'lernziel', 'methodik', 'lehrplan', 
                                'standards_kmk', 'standards_weitere', ]),
           ('tab_description',[ 'sprache', ]),
           ('tab_formal',     [ 'autor', 'herausgeber', 'publikations_datum', 'isbn',
                                'anbieter_herkunft', 'preis', 'rechte', 'techn_voraus'
                              ]),
           ('tab_visibility', [ 'is_browseable', 'visible_start', 'visible_end', ] ),
          ]
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.cleaned_data, request.FILES, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else:
    vars = get_folderish_vars_add(request, item_container, app_name,
                                  my_title, content, show_errors)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/file/manage_edit.html', vars )
