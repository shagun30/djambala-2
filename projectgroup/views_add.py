# -*- coding: utf-8 -*-
"""
/dms/projectgroup/views_add.py

.. enthaelt den View zum Anlegen einer geschlossenen Arbeitsgruppe
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.06.2007  Beginn der Arbeit
0.02  17.07.2007  Pinnwand
0.03  18.12.2007  do_protect_folder
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import save_container_values
from dms.queries        import save_item_values
from dms.queries        import exist_item
from dms.queries        import get_site_url
from dms.queries        import get_role_by_user_path
from dms.queries        import get_min_max_menu_left
from dms.queries        import do_protect_folder
from dms.queries        import get_item_container_by_parent_item_id

from dms.roles          import require_permission
from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_base     import ACL_USERS
from dms.utils_form     import get_folderish_vars_add

from dms.utils_navigation         import save_menus_left
from dms.projectgroup.utils       import get_role_choices
from dms.projectgroup.utils       import get_menu_left_from_sections
from dms.projectgroup.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def projectgroup_add(request, item_container):
  """ neue Arbeitsgruppe anlegen """

  #@transaction.commit_manually
  def save_values(name, new, my_item_container):
    """ Daten sichern """
    n_min, n_max = get_min_max_menu_left()
    menu_left_id = 1 + max(abs(n_min), n_max)
    new['text'] = _(u'<p>Beschreiben Sie hier bitte knapp die Funktion dieser Arbeits-/Lerngruppe ...</p>')
    new['sections'] = _(u'Kommunikation\nKooperation\nDokumente\n')
    text = get_menu_left_from_sections(my_item_container, name, new['sections'],
                                       ['kommunikation', 'dokumente', 'kooperation'])
    save_menus_left(menu_left_id, text)
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['nav_title'] = _(u'Start')
    new['menu_left_id'] = menu_left_id
    new['nav_name_left'] = 'start|'
    new['string_2'] = '/kooperation/events/'
    projectgroup_item_container = save_container_values(request.user,
                                       'dmsProjectgroup', name, new, my_item_container)
    #projectgroup_item_container.is_changeable = False
    #projectgroup_item_container.save()
    new['text'] = ''
    # --- Kommunikation
    new['name'] = name = _(u'kommunikation')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Kommunikation')
    new['nav_title'] = _(u'Kommunikation')
    new['section'] = _(u'Kommunikation')
    new['sections'] = _(u'Kommunikation')
    new['nav_name_left'] = 'start|kommunikation'
    komm_item_container = save_container_values(request.user,
                          'dmsFolder', name, new, projectgroup_item_container)
    new['name'] = name = _(u'rundschreiben')
    new['title'] = _(u'Rundschreiben')
    new['nav_title'] = _(u'Rundschreiben')
    new['section'] = _(u'Kommunikation')
    new['sections'] = _(u'Aufgaben\nBesprechung\nProtokolle\nTreffen\n')
    new['nav_name_left'] = 'start|kommunikation'
    item_container = save_container_values(request.user,
                          'dmsProjectgroupEmail', name, new, komm_item_container)
    new['name'] = name = _(u'pinnwand')
    new['title'] = _(u'Pinnwand')
    new['nav_title'] = _(u'Pinnwand')
    new['section'] = _(u'Kommunikation')
    new['sections'] = _(u'Allgemeines\nAustausch')
    new['nav_name_left'] = 'start|kommunikation'
    item_container = save_container_values(request.user,
                          'dmsPinboard', name, new, komm_item_container)
    # --- Dokumente
    new['name'] = name = _(u'dokumente')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Dokumente')
    new['nav_title'] = _(u'Dokumente')
    new['section'] = _(u'Dokumente')
    new['sections'] = 'Dokumente'
    new['nav_name_left'] = 'start|dokumente'
    mat_item_container = save_container_values(request.user,
                          'dmsFolder', name, new, projectgroup_item_container)
    new['name'] = name = _(u'protokoll')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Protokolle')
    new['nav_title'] = _(u'Protokolle')
    new['section'] = _(u'Dokumente')
    new['sections'] = ''
    new['nav_name_left'] = 'start|dokumente'
    item_container = save_container_values(request.user,
                          'dmsPool', name, new, mat_item_container)
    new['name'] = name = _(u'unterlagen')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Sitzungsunterlagen')
    new['nav_title'] = _(u'Unterlagen')
    new['section'] = _(u'Dokumente')
    new['sections'] = ''
    new['nav_name_left'] = 'start|dokumente'
    item_container = save_container_values(request.user,
                          'dmsPool', name, new, mat_item_container)
    # --- Kooperation
    new['name'] = name = _(u'kooperation')
    new['has_user_support'] = True
    new['is_moderated'] = False
    new['title'] = _(u'Kooperation')
    new['nav_title'] = _(u'Kooperation')
    new['section'] = _(u'Kooperation')
    new['sections'] = 'Kooperation'
    new['nav_name_left'] = 'start|kooperation'
    coop_item_container = save_container_values(request.user,
                          'dmsFolder', name, new, projectgroup_item_container)
    new['name'] = name = _(u'events')
    new['title'] = _(u'Terminkalender')
    new['nav_title'] = _(u'Termine')
    new['section'] = _(u'Kooperation')
    new['nav_name_left'] = 'start|kooperation'
    item_container = save_container_values(request.user,
                          'dmsEventBoard', name, new, coop_item_container)
    new['name'] = name = _(u'todo')
    new['title'] = _(u'To-Do-Liste')
    new['nav_title'] = _(u'To-Do-Liste')
    new['section'] = _(u'Kooperation')
    new['nav_name_left'] = 'start|kooperation'
    item_container = save_container_values(request.user,
                          'dmsToDoList', name, new, coop_item_container)
    # Wert sichern
    new={}
    new['title'] = _(u'User-Verwaltung')
    new['nav_title'] = new['title']
    new['is_browseable'] = False
    new['min_role_id'] = 2000
    acl_item_container = save_container_values(request.user,
                   'dmsUserFolder', ACL_USERS, new, projectgroup_item_container)
    do_protect_folder(projectgroup_item_container, acl_item_container, True)
    #ic = get_item_container_by_parent_item_id(item_container.item.id)
    #folders = []
    #for i in ic:
    #  if i.item.app.is_folderish and not i.item.app.is_userfolder:
    #    folders.append(i.item.name)
    #text = get_menu_left_from_sections(item_container, '', item_container.container.sections, folders)
    #save_menus_left(item_container.container.menu_left_id, text)
    #transaction.commit()


  my_role = get_role_by_user_path(request.user, item_container.container.path)

  class DmsItemForm(forms.Form):
    name        = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':20}) )
    title       = forms.CharField(max_length=240,
                        widget=forms.TextInput(attrs={'size':60}) )
    section     = forms.CharField(required=False,
                        widget=forms.Select(choices=
                               get_section_choices(item_container.container.sections),
                                            attrs={'size':4, 'style':'width:40%'} ) )
    min_role_id = forms.CharField(required=True,
                        widget=forms.Select(choices=get_role_choices(my_role),
                                            attrs={'size':6, 'style':'width:100%'} ) )

  app_name = 'projectgroup'
  my_title = _(u'Geschlossene Arbeits- bzw. Lerngruppe anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'name': _(u'ag'),
             'title': _(u'Arbeitsgruppe ...'),
             'owner': item_container.item.owner.get_full_name(),
             'owner_email': item_container.item.owner.email,
             'min_role_id': 50 }
  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_base',['name','title','section', 'min_role_id' ]),]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name,
                                  my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
