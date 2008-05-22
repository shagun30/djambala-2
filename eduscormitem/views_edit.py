# -*- coding: utf-8 -*-
"""
/dms/eduscormitem/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften eines Scorm-Paketes innerhalb der Lernarchive
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

0.01  11.03.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_PATH
from dms.models         import DmsItem
from dms.queries        import get_site_url
from dms.queries        import save_item
from dms.queries        import get_eduitem
from dms.queries        import set_extra_data
from dms.queries        import get_extra_data
from dms.queries        import save_item_container
from dms.edufolder.utils    import get_alter_choices

from dms.utils          import get_tabbed_form
from dms.roles          import require_permission
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices
from dms.utils          import get_section_choices
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.edulinkitem.utils       import get_extra
from dms.edulinkitem.utils       import set_extra
from dms.edulinkitem.utils       import get_lernrestyp_choices
from dms.edulinkitem.utils       import get_medienformat_choices
#from dms.edulinkitem.utils       import get_schlagworte_list
from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_sprachen_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import get_schlagworte
from dms.edulinkitem.utils       import save_modified_schlagworte
from dms.edulinkitem.utils       import save_modified_multiple_checkbox

from dms.eduscormitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def eduscormitem_edit(request, item_container):
  """ Eigenschaften des Ordners aendern """

  @transaction.commit_manually
  def save_extra(item_container, old, new, files):
    """ """
    if files != {}:
      filename = files['fname']['filename']
      # --- Dateien gleichen Namens werden ersetzt
      if filename == item_container.item.name:
        content = files['fname']['content']
        content_type = files['fname']['content-type']
        file_path = DOWNLOAD_PATH + item_container.container.path
        file_name = file_path + filename
        f = open(file_name, 'wb')
        f.write(content)
        f.close()
    old['integer_3'] = old['lernrestyp']
    old['integer_4'] = old['medienformat']
    #old['integer_5'] = old['zertifikat']
    new['integer_3'] = new['lernrestyp']
    new['integer_4'] = new['medienformat']
    #new['integer_5'] = new['zertifikat']
    edu_item = get_eduitem(item_container.item)
    save_modified_schlagworte(edu_item, old, new)
    #old['extra'] = set_extra_data(schlagwort_org=old['schlagwort'])
    #new['extra'] = encode_html(set_extra_data(schlagwort_org=new['schlagwort']))
    old['extra'] = set_extra_data(schlagwort_org=decode_html(old['schlagwort']))
    new['extra'] = set_extra_data(schlagwort_org=encode_html(new['schlagwort']))
    save_modified_multiple_checkbox(old, new, 'fach_sachgebiet', edu_item.fach_sachgebiet)
    save_modified_multiple_checkbox(old, new, 'schulart', edu_item.schulart)
    save_modified_multiple_checkbox(old, new, 'schulstufe', edu_item.schulstufe)
    save_modified_multiple_checkbox(old, new, 'sprache', edu_item.sprache)
    save_modified_multiple_checkbox(old, new, 'zielgruppe', edu_item.zielgruppe)
    edu_item.save_modified_values(old, new)
    if item_container.is_data_object:
      save_item(item_container, old, new)
    else:
      save_item_container(item_container, old, new)
    transaction.commit()

  def get_ids(itemlist):
    """ liefert die IDs """
    ret = []
    for l in itemlist:
      ret.append(l.id)
    return ret

  class DmsItemForm ( forms.Form ) :
    """ Elemente des Eingabeformulars """
    if item_container.is_data_object:
      fname               = forms.CharField(required=False, max_length=200,
                                  widget=forms.FileInput(attrs={'size':40}) )
      title      = forms.CharField(max_length=240,
                        widget=forms.TextInput(attrs={'size':60}) )
      url_more   = forms.CharField(required=False, max_length=200,
                        widget=forms.TextInput(attrs={'size':60}) )
      text       = forms.CharField(
                        widget=forms.Textarea(attrs={'rows':10, 'cols':60, 'id':'ta',
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
                        widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta1',
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
      fach_sachgebiet = forms.MultipleChoiceField(required=False, choices=get_fach_list(),
                      widget=forms.CheckboxSelectMultiple() )
      zielgruppe = forms.MultipleChoiceField(required=False, choices=get_zielgruppen_list(),
                      widget=forms.CheckboxSelectMultiple() )
      schulstufe = forms.MultipleChoiceField(required=False, choices=get_schulstufen_list(),
                      widget=forms.CheckboxSelectMultiple() )
      schulart   = forms.MultipleChoiceField(required=False, choices=get_schularten_list(),
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
                        widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta7',
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
      is_exchangeable = forms.BooleanField(required=False)
      alter_min  = forms.ChoiceField(choices=get_alter_choices(),
                        widget=forms.RadioSelect() )
      alter_max  = forms.ChoiceField(choices=get_alter_choices(),
                        widget=forms.RadioSelect() )
      license         = forms.ChoiceField(choices=get_license_choices(item_container),
                                          widget=forms.RadioSelect() )
    else:
      section    = forms.CharField(required=False,
            widget=forms.Select(choices=
            get_section_choices(item_container.container.sections),
                                attrs={'size':4, 'style':'width:60%'} ) )
      is_browseable   = forms.BooleanField(required=False)
      visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))
      visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'size':10}))

  edu_extra = get_eduitem(item_container.item)
  extra = get_extra_data(item_container)

  #schlagworte = get_schlagworte_list(edu_extra.schlagwort.all())
  if extra != None:
    schlagworte = decode_html(extra['schlagwort_org'])
  else:
    schlagworte = ''
  data_init = {
                'title'             : decode_html(item_container.item.title),
                'text'              : remove_link_icons(item_container.item.text),
                'url_more'          : item_container.item.url_more,
                'section'           : decode_html(item_container.section),
                'lernrestyp'        : item_container.item.integer_3,
                'medienformat'      : item_container.item.integer_4,
                'titel_lang'        : decode_html(edu_extra.titel_lang),
                'beschreibung_lang' : decode_html(edu_extra.beschreibung_lang),
                'schlagwort'        : schlagworte,
                'sprache'           : get_ids(edu_extra.sprache.all()),
                'lernziel'          : decode_html(edu_extra.lernziel),
                'lernzeit'          : decode_html(edu_extra.lernzeit),
                'methodik'          : decode_html(edu_extra.methodik),
                'lehrplan'          : decode_html(edu_extra.lehrplan),
                'standards_kmk'     : decode_html(edu_extra.standards_kmk),
                'standards_weitere' : decode_html(edu_extra.standards_weitere),
                'fach_sachgebiet'   : get_ids(edu_extra.fach_sachgebiet.all()),
                'zielgruppe'        : get_ids(edu_extra.zielgruppe.all()),
                'schulstufe'        : get_ids(edu_extra.schulstufe.all()),
                'schulart'          : get_ids(edu_extra.schulart.all()),
                'autor'             : decode_html(edu_extra.autor),
                'herausgeber'       : decode_html(edu_extra.herausgeber),
                'publikations_datum': decode_html(edu_extra.publikations_datum),
                'isbn'              : decode_html(edu_extra.isbn),
                'rechte'            : decode_html(edu_extra.rechte),
                'anbieter_herkunft' : decode_html(edu_extra.anbieter_herkunft),
                'preis'             : decode_html(edu_extra.preis),
                'techn_voraus'      : decode_html(edu_extra.techn_voraus),
                'image_url'         : item_container.item.image_url,
                'image_url_url'     : item_container.item.image_url_url,
                'image_extern'      : item_container.item.image_extern,
                'is_browseable'     : item_container.is_browseable,
                'visible_start'     : item_container.visible_start,
                'visible_end'       : item_container.visible_end,
                'is_exchangeable'   : item_container.item.is_exchangeable,
                'alter_min'         : edu_extra.alter_min,
                'alter_max'         : edu_extra.alter_max,
                'license'           : item_container.item.license.id
              }
  app_name = u'eduscormitem'
  my_title = _(u'Scorm-Paket innerhalb der Lernarchive ändern')
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  if item_container.is_data_object:
    if item_container.container.sections.strip() != '':
      base = ('tab_base', [ 'lernrestyp', 'title', 'text', 'beschreibung_lang',
                            'section', 'schlagwort', ])
    else:
      base = ('tab_base', [ 'lernrestyp', 'title', 'text', 'beschreibung_lang',
                            'schlagwort', ])
    tabs = [ base,
            ('tab_course',      [ 'fach_sachgebiet',]),
            ('tab_pupil',       [ 'titel_lang', 'beschreibung_lang', 'alter_min', 'alter_max' ]),
            ('tab_details',     [ 'zielgruppe', 'schulstufe', 'schulart']),
            ('tab_paed',        [ 'lernzeit', 'lernziel', 'methodik', 'lehrplan', 
                                  'standards_kmk', 'standards_weitere', ]),
            ('tab_description', [ 'url_more', 'medienformat', 'sprache', ]),
            ('tab_formal',      [ 'is_exchangeable',
                                  'autor', 'herausgeber', 'publikations_datum', 'isbn',
                                  'anbieter_herkunft', 'preis', 'rechte', 'techn_voraus'
                                ]),
            ('tab_image',       [ 'image_url', 'image_url_url', 'image_extern', ] ),
            ( 'tab_update',     [ 'fname', ] ),
            ('tab_license',     [ 'license', ] ),
            ('tab_visibility',  [ 'is_browseable', 'visible_start', 'visible_end', ] ),
            ]
  else:
    my_title = _(u'Einblendung einer Datei im Lernarchiv ändern')
    tabs = [ ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_extra ( item_container, data_init, f.cleaned_data, request.FILES )
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response('app/eduscormitem/manage_edit.html', vars)
