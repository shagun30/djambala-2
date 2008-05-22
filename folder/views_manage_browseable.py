# -*- coding: utf-8 -*-
"""
/dms/folder/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2007  Beginn der Arbeit
"""

import string
import datetime

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_items
from dms.queries        import get_site_url
from dms.queries        import save_manage_browseable_values

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_folderish_actions
from dms.utils_form     import get_base_vars

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def do_manage_browseable(request, item_container, app_name, my_title,
                         app_types=[], order='', dont={}):
  """ Freigabemodus des Ordners """
  app_name = item_container.item.app.name
  show_delete_mode = (app_name.find('board') > 0) or (app_name == 'dmsGuestbook')
  main_obj = {}
  main_obj['url']  = get_site_url(item_container, 'index.html')
  user_perms = UserEditPerms(request.user.username,request.path)
  objs = []
  if order == '':
    if request.GET.has_key('sort') :
      order = request.GET['sort']
    else :
      order = ''
  item_containers_temp = get_folder_items(item_container, order)

  has_user_folder = False
  items = []
  for ic in item_containers_temp:
    obj = {}
    obj['id'] = ic.item.id
    obj['title'] = ic.item.title
    obj['app_name'] = ic.item.app.name
    obj['name'] = ic.item.name
    obj['is_deleted'] = ic.is_deleted
    obj['is_browseable'] = ic.is_browseable
    #obj['last_modified'] = '2006-11-17'#item_container.last_modified
    my_date = ic.last_modified
    obj['last_modified'] = my_date.strftime('%m/%d/%Y')

    if ic.item.app.name == 'dmsRedirect':
      if string.find(ic.item.url_more, 'http://') < 0:
        site = ic.container.site
        path = ic.container.path + ic.item.url_more
        length=len(site.base_folder)
        if length < len(path):
          obj['url'] = site.url + path[length:]
        else :
          obj['url'] = site.url + '/'
      else:
        obj['url']  = ic.item.url_more
      objs.append(obj)
      items.append(ic)
    elif app_types == []:
      if ic.item.app.is_folderish:
        obj['url'] = get_site_url(ic, 'index.html')
      else:
        obj['url'] = get_site_url(ic, ic.item.name)
      objs.append(obj)
      items.append(ic)
    elif app_types != [] and ic.item.app.name in app_types:
      if ic.item.app.is_folderish:
        obj['url'] = get_site_url(ic, 'index.html')
      else:
        obj['url'] = get_site_url(ic, ic.item.name)
      objs.append(obj)
      items.append(ic)

  if request.method == 'POST':
    save_manage_browseable_values(request, items)
    return HttpResponseRedirect(
               get_site_url(item_container, 'index.html/manage_browseable/'))
  else:
    vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage', in_edit_mode=True)
    v = { 'main_obj' : main_obj,
          'objs'     : objs,
          'id'       : item_container.item.id,
          'title'    : my_title,
          'sub_title': item_container.item.title,
          'action'   : get_folderish_actions(request, user_perms,
                           item_container, app_name, False, dont),
          'add_mode' : user_perms.perm_add,
          'show_delete_mode': show_delete_mode,
          'next'     : get_site_url(item_container,
                                   'index.html/manage_browseable/'),
        }
    vars.update(v)
    vars['image_url'] = ''
    return render_to_response ( 'app/base_manage_browseable.html', vars )

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def folder_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  return do_manage_browseable(request, item_container, 'folder', _(u'Objekte freischalten/löschen'))
