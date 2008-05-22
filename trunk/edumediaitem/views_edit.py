# -*- coding: utf-8 -*-
"""
/dms/edumediaitem/views_edit.py

.. enthaelt den View zurm Aendern der Eigenschaften des Medienpakets
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.09.2007  Beginn der Arbeit
0.02  24.09.2007  is_exchangeable
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import set_extra_data
from dms.queries        import get_extra_data
from dms.queries        import get_extra_var
from dms.queries        import get_eduitem

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import remove_link_icons

from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html
from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_sprachen_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import save_modified_schlagworte
from dms.edulinkitem.utils       import save_modified_multiple_checkbox
from dms.edulinkitem.utils       import get_lernrestyp_choices
from dms.edulinkitem.utils       import get_medienformat_choices
from dms.edufolder.utils    import get_alter_choices

from dms.edumediaitem.help_form   import help_form

from dms.encode_decode  import encode_html

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edumediaitem_edit(request, item_container):
  """ Eigenschaften des Lernarchivs aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')

  # @ transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
    old['integer_3'] = old['lernrestyp']
    old['integer_4'] = old['medienformat']
    #old['integer_5'] = old['zertifikat']
    new['integer_3'] = new['lernrestyp']
    new['integer_4'] = new['medienformat']
    #new['integer_5'] = new['zertifikat']
    item_container.container.save_values(old, new)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    edu_item = get_eduitem(item_container.item)
    save_modified_schlagworte(edu_item, old, new)
    #old['extra'] = set_extra_data(schlagwort_org=old['schlagwort'])
    #new['extra'] = encode_html(set_extra_data(schlagwort_org=new['schlagwort']))
    old['extra'] = set_extra_data(schlagwort_org=decode_html(old['schlagwort']))
    new['extra'] = set_extra_data(schlagwort_org=encode_html(new['schlagwort']))
    save_modified_multiple_checkbox(old, new, 'fach_sachgebiet',
                                    edu_item.fach_sachgebiet)
    save_modified_multiple_checkbox(old, new, 'schulart',
                                    edu_item.schulart)
    save_modified_multiple_checkbox(old, new, 'schulstufe',
                                    edu_item.schulstufe)
    save_modified_multiple_checkbox(old, new, 'sprache',
                                    edu_item.sprache)
    save_modified_multiple_checkbox(old, new, 'zielgruppe',
                                    edu_item.zielgruppe)
    edu_item.save_modified_values(old, new)
    # transaction.commit()

  def get_ids(itemlist):
    """ liefert die IDs """
    ret = []
    for l in itemlist:
      ret.append(l.id)
    return ret

  class dms_itemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    if item_container.is_data_object:
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
      medienformat = forms.CharField(widget=forms.Select(choices=get_medienformat_choices(),
                                      attrs={'style':'width:60%'} ) )
      titel_lang = forms.CharField(required=False, max_length=240,
            widget=forms.TextInput(attrs={'size':60}) )
      nav_title = forms.CharField(required=False, max_length=60,
            widget=forms.TextInput(attrs={'size':30}) )
      beschreibung_lang = forms.CharField(required=False,
            widget=forms.Textarea(attrs={'rows':8, 'cols':60, 'id':'ta1',
                                        'style':'width:100%;'}) )
      schlagwort = forms.CharField(required=False,
            widget=forms.Textarea( attrs={'rows':4, 'cols':40, 'style':'width:60%;'}) )
      sprache    = forms.MultipleChoiceField(required=False, 
            choices=get_sprachen_list(),
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
      fach_sachgebiet = forms.MultipleChoiceField(required=False,
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
      rechte     = forms.CharField(required=False, 
            widget=forms.Textarea( attrs={'rows':8, 'cols':60, 'id':'ta7',
                                          'style':'width:100%;'}) )
      anbieter_herkunft = forms.CharField(required=False, max_length=240,
            widget=forms.TextInput(attrs={'size':60}) )
      preis      = forms.CharField(required=False, max_length=20,
            widget=forms.TextInput(attrs={'size':20}) )
      techn_voraus = forms.CharField(required=False, 
            widget=forms.Textarea( attrs={'rows':8, 'cols':60, 'id':'ta8',
                                          'style':'width:100%;'}) )
      image_url  = forms.CharField(required=False, max_length=200,
            widget=forms.TextInput(attrs={'size':60}) )
      image_url_url = forms.URLField(required=False, max_length=200,
            widget=forms.TextInput(attrs={'size':60}) )
      image_extern = forms.BooleanField(required=False)
      has_user_support  = forms.BooleanField(required=False)
      has_comments      = forms.BooleanField(required=False)
      is_moderated      = forms.BooleanField(required=False)
      is_browseable     = forms.BooleanField(required=False)
      visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
            widget=forms.TextInput(attrs={'size':10}))
      visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
            widget=forms.TextInput(attrs={'size':10}))
      is_exchangeable = forms.BooleanField(required=False)
      sections       = forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':5, 'cols':40, 'style':'width:50%;'}) )
      alter_min  = forms.ChoiceField(choices=get_alter_choices(),
                        widget=forms.RadioSelect() )
      alter_max  = forms.ChoiceField(choices=get_alter_choices(),
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

  extra = get_extra_data(item_container)

  app_name = u'edumediaitem'
  my_title = _(u'Medienpaket ändern')
  if item_container.item.string_1 == '':
    string1 = _(u'Wikipedia')
  else:
    string1 = item_container.item.string_1
  edu_extra = get_eduitem(item_container.item)
  extra_data = get_extra_data(item_container)
  fach = get_extra_var(extra_data, 'fach', '')
  schulart = get_extra_var(extra_data, 'schulart', '')
  freie_suche = get_extra_var(extra_data, 'freie_suche', '')
  schlagworte = ''
  if extra != None:
    try:
      schlagworte = decode_html(extra['schlagwort_org'])
    except:
      pass
  data_init = {
                'title'             : decode_html(item_container.item.title),
                'nav_title'         : decode_html(item_container.container.nav_title),
                'text'              : remove_link_icons(item_container.item.text),
                'lernrestyp'        : item_container.item.integer_3,
                'medienformat'      : item_container.item.integer_4,
                'sections'          : decode_html(item_container.container.sections),
                'url_more'          : item_container.item.url_more,
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
                'has_user_support': item_container.item.has_user_support,
                'has_comments'    : item_container.item.has_comments,
                'is_moderated'    : item_container.item.is_moderated,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'     : item_container.visible_start,
                'visible_end'       : item_container.visible_end,
                'is_exchangeable'   : item_container.item.is_exchangeable,
                'alter_min'         : edu_extra.alter_min,
                'alter_max'         : edu_extra.alter_max,
              }

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm ( data )
  if item_container.is_data_object:
    tabs = [ ('tab_base',        [ 'lernrestyp', 'title', 'nav_title', 'text', 'sections', 'schlagwort', ]),
             ('tab_course',      [ 'fach_sachgebiet',]),
             ('tab_pupil',       [ 'titel_lang', 'beschreibung_lang', 'alter_min', 'alter_max' ]),
             ('tab_details',     [ 'zielgruppe', 'schulstufe', 'schulart']),
             ('tab_paed',        [ 'lernzeit', 'lernziel', 'methodik', 'lehrplan', 
                                   'standards_kmk', 'standards_weitere', ]),
             ('tab_description', [ 'medienformat', 'sprache', ]),
             ('tab_formal',      [ 'is_exchangeable',
                                   'autor', 'herausgeber', 'publikations_datum', 'isbn',
                                   'anbieter_herkunft', 'preis', 'rechte', 'techn_voraus'
                                 ]),
             ('tab_image',       [ 'image_url', 'image_url_url', 'image_extern', ] ),
             ('tab_user_support', ['has_user_support', 'is_moderated', 'has_comments']),
             ('tab_visibility',  [ 'is_browseable', 'visible_start', 'visible_end', ] ),
            ]
  else:
    my_title = _(u'Einblendung eines Medienpakets ändern')
    tabs = [ ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ), ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.cleaned_data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_folderish_vars_edit(request, item_container, app_name,
                                   my_title, content, f)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/base_edit.html', vars )
