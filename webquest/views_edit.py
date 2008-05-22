# -*- coding: utf-8 -*-
"""
/dms/webquest/views_edit.py

.. enthaelt den View zurm Aendern der Eigenschaften des Webquests
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import set_extra_data
from dms.queries        import get_extra_data
from dms.queries        import get_eduitem

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices

from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_sprachen_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import save_modified_schlagworte
from dms.edulinkitem.utils       import save_modified_multiple_checkbox

from dms.webquest.help_form   import help_form


from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def webquest_edit(request, item_container):
  """ Eigenschaften des Lernarchivs aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
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
    transaction.commit()

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
      nav_title = forms.CharField(required=False, max_length=60,
            widget=forms.TextInput(attrs={'size':30}) )
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

  schlagworte = ''
  if extra != None:
    try:
      schlagworte = decode_html(extra['schlagwort_org'])
    except:
      pass
  data_init = {
                'title'             : decode_html(item_container.item.title),
                'text'              : remove_link_icons(item_container.item.text),
                'url_more'          : item_container.item.url_more,
                'image_url'         : item_container.item.image_url,
                'image_url_url'     : item_container.item.image_url_url,
                'image_extern'      : item_container.item.image_extern,
                'has_user_support': item_container.item.has_user_support,
                'has_comments'    : item_container.item.has_comments,
                'is_moderated'    : item_container.item.is_moderated,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'     : item_container.visible_start,
                'visible_end'       : item_container.visible_end,
                'license'           : item_container.item.license.id
              }

  app_name = 'webquestitem'
  my_title = _(u'Webquest ändern')

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm ( data )
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  if item_container.is_data_object:
    tabs = [ ('tab_base',        [ 'title', 'nav_title', 'text', ]),
            ('tab_image',       [ 'image_url', 'image_url_url', 'image_extern', ] ),
            ('tab_user_support', ['has_user_support', 'is_moderated', 'has_comments']),
            ('tab_license',     [ 'license', ] ),
            ('tab_visibility',  [ 'is_browseable', 'visible_start', 'visible_end', ] ),
            ]
  else:
    my_title = _(u'Einblendung eines Webquests ändern')
    tabs = [ ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ), ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.cleaned_data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else:
    dont = { 'navigation_mode': 0, }
    vars = get_folderish_vars_edit(request, item_container,
                                   app_name, my_title, content, f, dont=dont,
                                   ignore_own_breadcrumb=True)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/base_edit.html', vars )