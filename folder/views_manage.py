#-*-coding: utf-8 -*-
"""
/dms/folder/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  15.01.2007  Paste-Funktion verallgemeinert
0.03  23.01.2007  Redirect
0.04  06.02.2007  is_usermanagement
0.05  03.10.2007  get_site_actions
"""

import time

from django.http              import HttpResponse
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.queries              import get_folder_items
from dms.queries              import get_top_url
from dms.queries              import get_site_url
from dms.queries              import get_base_site_url
from dms.queries              import is_protected_app
from dms.queries              import get_role_by_user_path

from dms.views_clipboard      import get_paste_obj
from dms.views_clipboard      import get_paste_app_name
from dms.utils                import get_folderish_actions
from dms.utils                import get_site_actions
from dms.utils_form           import get_base_vars
from dms.utils_base           import ACL_USERS

from dms.folder.utils         import get_add_ons

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_single_obj(item_container, allow_copy, my_role):
  """ baut obj zusammen """
  obj = {}
  obj['id'] = item_container.id
  obj['title'] = item_container.item.title
  obj['app_name'] = item_container.item.app.name
  obj['is_folderish'] = item_container.item.app.is_folderish
  obj['is_userfolder'] = item_container.item.app.is_userfolder
  obj['is_linkable'] = item_container.item.app.is_linkable and \
                        item_container.is_data_object
  obj['allow_copy'] = allow_copy
  is_wiki_start = item_container.item.app.name == 'dmsWikiItem' \
                  and item_container.item.name == 'start.html'
  special_progs = ['dmsEduScormItem', 'dmsFreemind', 'dmsFolderOrg']
  # 10 = the_manager
  obj['is_changeable'] = ((item_container.is_changeable or my_role <= 10 ) and not is_wiki_start)
  obj['is_renameable'] = not obj['is_userfolder'] \
                         and not item_container.item.app.name in special_progs \
                         and not is_protected_app(item_container) \
                         and not is_wiki_start \
                         and obj['is_changeable']
  if item_container.item.app.is_folderish:
    if item_container.is_data_object:
      obj['url']  = get_site_url(item_container, 'index.html')
    else:
      obj['url']  = get_site_url(item_container, item_container.item.name)
  else :
    obj['url']  = get_site_url(item_container, item_container.item.name)
  obj['name'] = item_container.item.name
  if item_container.item.name == ACL_USERS:
    has_user_folder = True
  obj['app_description'] = item_container.item.app.description
  obj['last_modified'] = item_container.last_modified.strftime ( '%d.%m.%Y %H:%M' )
  obj['is_deleted'] = item_container.is_deleted
  return obj

# -----------------------------------------------------
def get_objs(request, my_item_container, allow_copy):
  """ liefert die in dem Ordner enthaltenen Objekte """
  main_obj = {}
  main_obj['item_container_id'] = my_item_container.id
  main_obj['name'] = my_item_container.item.name
  main_obj['url']  = get_site_url(my_item_container, 'index.html')
  main_obj['app_name'] = my_item_container.item.app.name
  main_obj['is_sortable'] = True
  main_obj['top_url'] = get_top_url(my_item_container)
  main_obj['paste_obj'] = get_paste_obj(request, my_item_container)
  main_obj['paste_app_name'] = get_paste_app_name(request)
  main_obj['title'] = my_item_container.item.title
  main_obj['last_modified'] = my_item_container.last_modified.\
                              strftime('%d.%m.%Y %H:%M')
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    order = ''
  user_perms = UserEditPerms(request.user.username, request.path)
  if user_perms.perm_manage or user_perms.perm_manage_folderish:
    item_containers = get_folder_items(my_item_container, order)
  elif user_perms.perm_edit_own or user_perms.perm_manage_own:
    try:
      item_containers = get_folder_own_items(my_item_container.item, order, request.user.id)
    except:
      item_containers = []
  else:
    item_containers = []
  objs = []
  objs_linkable = []
  my_role = get_role_by_user_path(request.user, my_item_container.container.path)
  for item_container in item_containers:
    obj = get_single_obj(item_container, allow_copy, my_role)
    objs.append(obj)
    if item_container.item.app.is_linkable:
      objs_linkable.append(obj)
  return main_obj, objs, objs_linkable

# -----------------------------------------------------
@require_permission('perm_add')
def do_manage(request, item_container, user_perms, add_ons, app_name,
              my_title, my_title_own, dont={}, allow_copy=True):
  """ Pflegemodus des Ordners """
  has_user_folder = False
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage', False,
                                   ignore_own_breadcrumb=True, in_edit_mode=True)
  for k in dont.items():
    vars[k] = ''
  v = { 'allow_copy'       : allow_copy,
        'title'            : my_title,
        'this_title'       : item_container.item.title,
        'action'           : get_folderish_actions(request, user_perms, item_container,
                                 app_name, has_user_folder, dont),
        'action_site'      : get_site_actions(request, user_perms, item_container),
        'add_mode'         : user_perms.perm_add,
        'add_ons_0'        : add_ons[0],
        'add_ons_1'        : add_ons[1],
        'add_ons_2'        : add_ons[2],
        'add_ons_3'        : add_ons[3],
        'ajax_url'         : get_site_url(item_container, 'index.html/ajax/')
      }
  vars.update(v)
  return render_to_response ( 'app/base_manage.html', vars )

# -----------------------------------------------------
def get_allow_copy(item_container):
  """ """
  return item_container.item.app.name != 'dmsEduFolder'

# -----------------------------------------------------
@require_permission('perm_add')
def folder_manage(request, item_container):
  """ Pflegemodus des Ordners """
  user_perms, add_ons = get_add_ons(request.user.username,
                                    request.path, item_container)
  app_name = 'folder'
  my_title = _(u'Ordner pflegen')
  my_title_own = _(u'Eigene Objekte pflegen')

  return do_manage(request, item_container, user_perms, add_ons,
                   app_name, my_title, my_title_own)

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_standard(request, item_container):
  """ Informationen der Standardseite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_standard = get_template('app/base_manage_standard.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_standard.render(Context({'objs': objs, 'main_obj': main_obj,
                                   'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_delete(request, item_container):
  """ Informationen der Loeschen-Seite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_delete = get_template('app/base_manage_delete.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_delete.render(Context({'objs': objs, 'main_obj': main_obj,
                                 'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_undo(request, item_container):
  """ Informationen der Undo-Seite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = (item_container.item.app.name != 'dmEduFolder')
  t_undo = get_template('app/base_manage_undo.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_undo.render(Context({'objs': objs, 'main_obj': main_obj,
                               'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_delete_total(request, item_container):
  """ Informationen der Schreddern-Seite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_delete_total = get_template('app/base_manage_delete_total.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_delete_total.render(Context({'objs': objs, 'main_obj': main_obj,
                                       'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_cut(request, item_container):
  """ Informationen der Ausschneide-Seite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_cut = get_template('app/base_manage_cut.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_cut.render(Context({'objs': objs, 'main_obj': main_obj,
                              'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_copy(request, item_container):
  """ Informationen der Kopier-Seite """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_copy = get_template('app/base_manage_copy.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_copy.render(Context({'objs': objs, 'main_obj': main_obj,
                               'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def folder_ajax_get_link(request, item_container):
  """ Informationen der Seite zum Einblenden """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  allow_copy = get_allow_copy(item_container)
  t_link = get_template('app/base_manage_link.html')
  main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  res = t_link.render(Context({'objs': objs_linkable, 'main_obj': main_obj,
                               'base_site_url': get_base_site_url()}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

