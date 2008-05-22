# -*- coding: utf-8 -*-
"""
/dms/webquest/views_add.py

.. enthaelt den View zum Ergaenzen eines Webquests
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
0.02  05.05.2008  Kopplung an Lernarchiv-Webquest
"""

import datetime

from django.utils.translation import ugettext as _

from dms.views_error    import show_error_object_exist
from dms.models         import DmsItem

from django.template.loader import get_template
from django.template    import Context
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from dms.queries        import save_container_values
from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import get_edu_sprache_id
from dms.queries        import set_extra_data
from dms.queries        import save_item_values
from dms.queries        import get_item_container_by_url
from dms.queries        import get_item_container_children
from dms.queries        import is_file_by_item_container
from dms.queries        import get_app

from dms.mail           import send_control_email

from dms.roles          import *
from dms.views_error    import show_error_object_exist
from dms.utils          import show_link
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.utils_form     import get_folderish_vars_add
from dms.utils_base     import ACL_USERS

from dms.edufolder.utils  import do_copy
from dms.encode_decode    import encode_html

from dms.webquest.views_navigation_left  import create_new_menu_webquest

from dms.webquest.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def webquest_add(request, item_container):
  """ neuen Webquest anlegen """

  def save_values(request, name, new, item_container):
    """ Daten sichern """
    community_id = 0
    schulverbund_id = 0
    new['is_exchangeable'] = item_container.item.is_exchangeable
    new['is_browseable'] = True
    new['has_user_support'] = True
    edu_ic = None
    if new.has_key('string_2') and new['string_2'].strip() != '':
      url = new['string_2'].strip()
      edu_ic = get_item_container_by_url(url)
      if edu_ic != None:
        if edu_ic.item.app.name != 'dmsEduWebquestItem':
          return
        item_container_new = do_copy(request, edu_ic, item_container)
        item_container_new.item.app = get_app('dmsWebquest') # !!!!!
        item_container_new.item.save()
        #if new.has_key('name') and new['name'].strip() == '':
        #  item_container_new.name = new['name'].strip()
        do_save = False
        if new.has_key('title') and new['title'].strip() == '':
          item_container_new.title = new['title'].strip()
          do_save = True
        if new.has_key('nav_title') and new['nav_title'].strip() == '':
          item_container_new.nav_title = new['nav_title'].strip()
          do_save = True
        if do_save:
          item_container_new.save()
    # --- muss explizit gesetzt werden
    if edu_ic == None:
      item_container_new = item_container = save_container_values(request.user,
                                  'dmsWebquest', name, new, item_container)
      # --- Informationsseite
      new={}
      new['name'] = name = _(u'einleitung.html')
      new['title'] = _(u'Einleitung')
      new['text'] = _(u'<p>\nEinleitung des Webquest\n</p>\n')
      ic = save_item_values(request.user, 'dmsDocument', name, new,
                            item_container_new, True, False)
      #ic.part_of_id = part_of_id
      ic.order_by = 1000
      ic.save()
      new={}
      new['name'] = name = _(u'aufgabe.html')
      new['title'] = _(u'Aufgabe')
      new['text'] = _(u'<p>\nAufgabe des Webquest\n</p>\n')
      ic = save_item_values(request.user, 'dmsDocument', name, new,
                            item_container_new, True, False)
      #ic.part_of_id = part_of_id
      ic.order_by = 1010
      ic.save()
      new={}
      new['name'] = name = _(u'vorgehen.html')
      new['title'] = _(u'Vorgehen')
      new['text'] = _(u'<p>\nEmpfehlungen zum Vorgehen\n</p>\n')
      ic = save_item_values(request.user, 'dmsDocument', name, new,
                            item_container_new, True, False)
      #ic.part_of_id = part_of_id
      ic.order_by = 1020
      ic.save()
      new={}
      new['name'] = name = _(u'erwartung.html')
      new['title'] = _(u'Erwartung')
      new['text'] = _(u'<p>\nErwartung und Hinweise zur Bewertung des Webquest\n</p>\n')
      ic = save_item_values(request.user, 'dmsDocument', name, new,
                            item_container_new, True, False)
      #ic.part_of_id = part_of_id
      ic.order_by = 1100
      ic.save()
      # --- Materialpool
      new={}
      new['name'] = name = _(u'material')
      new['has_user_support'] = False
      new['is_moderated'] = True
      new['title'] = _(u'Material')
      new['nav_title'] = _(u'Material')
      new['sections'] = ''
      ic_pool = item_container = save_container_values(request.user,
                            'dmsPool', name, new, item_container_new)
      ic_pool.order_by = 1050
      ic_pool.save()
    # --- Ordner
    new={}
    new['name'] = name = _(u'ergebnisse')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Ergebnisse')
    new['nav_title'] = _(u'Ergebnisse')
    new['nav_name_left'] = 'webquest|ergebnisse'
    new['sections'] = ''
    ic_folder = item_container = save_container_values(request.user,
                                'dmsPool', name, new, item_container_new)
    #ic_folder.part_of_id = item_container.part_of_id
    ic_folder.order_by = 1200
    ic_folder.save()
    # --- User-Verwaltung
    new = {}
    new['title'] = _(u'User-Verwaltung')
    new['nav_title'] = new['title']
    new['is_browseable'] = False
    acl_item_container = save_container_values(request.user,
                  'dmsUserFolder', ACL_USERS, new, ic_folder)
    acl_item_container.set_is_changeable(False)
    # --- linke Navigation
    create_new_menu_webquest(item_container_new)
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    string_2   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    name       = forms.CharField(required=False, max_length=60,
                       widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    nav_title  = forms.CharField(required=False, max_length=60,
                       widget=forms.TextInput(attrs={'size':30}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                         attrs={'rows':10, 'cols':60, 'id':'ta',
                                'style':'width:100%;'}) )
    section    = forms.CharField(required=False, widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                                           attrs={'size':4, 'style':'width:60%'} ) )
    license         = forms.ChoiceField(choices=get_license_choices(item_container),
                                        widget=forms.RadioSelect() )

  app_name = 'webquest'
  my_title = _(u'Webquest anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else :
    data = { 'license': 1, }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_base',       [ 'string_2', 'section']),
           ('tab_base_2',     [ 'name', 'title', 'nav_title', 'text', ]),
           ('tab_license',    [ 'license', ] ),
          ]
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    new = f.cleaned_data
    if not exist_item(item_container, name):
      save_values(request, name, new, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else:
    tEduFolder = get_template('app/webquest/target_edufolder.html')
    vars = get_folderish_vars_add(request, item_container, app_name, my_title,
                                  content, show_errors)
    vars['text_intro'] = help_form['copyright']['help']
    #select_edufolder = show_link('javascript:select_dest_url(document.form_input.dest_folder)',
    #                    _(u'Webquest auswählen ...'), url_extern="_extern")
    #vars['top_of_form'] = tEduFolder.render( Context( {'get_eduwebquest': select_edufolder }) )
    return render_to_response ( 'app/base_edit.html', vars )
