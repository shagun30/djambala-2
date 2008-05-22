# -*- coding: utf-8 -*-
"""
/dms/newsboard/views_manage.py

.. enthaelt den View fuer die RSS-Feed-Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.07.2007  Beginn der Arbeit
"""

from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.queries              import get_folder_items
from dms.queries              import get_top_url
from dms.queries              import get_site_url

from dms.utils                import get_folderish_actions
from dms.utils_form           import get_base_vars

from dms.feeds                import get_all_feeds

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def do_manage(request, item_container, user_perms, add_ons, app_name, my_title, my_title_own, dont={}):
  """ Pflegemodus des Ordners """

  def get_feed_objs():
    objs = []
    for feed in get_all_feeds():
      obj = {}
      obj['id'] = feed.id
      obj['title'] = feed.title
      obj['app_name'] = 'dmsRssFeed'
      obj['url']  = get_top_url(my_item_container) + 'feeds/rss/' + feed.name
      obj['feed_url']  = get_site_url(item_container, feed.name)
      obj['name'] = feed.name
      obj['app_description'] = _(u'RSS-Feed')
      obj['last_modified'] = feed.last_modified.strftime ( '%d.%m.%Y %H:%M' )
      obj['is_deleted'] = feed.is_deleted
      obj['is_renameable'] = True
      obj['no_clipboard'] = True
      objs.append(obj)
    return objs

  t_standard = get_template('app/rssfeedmanager/manage_standard.html')
  my_item_container = item_container
  main_obj = {}
  main_obj['item_container_id'] = my_item_container.id
  main_obj['name'] = my_item_container.item.name
  main_obj['url']  = get_site_url(item_container, 'index.html')
  main_obj['app_name'] = my_item_container.item.app.name
  main_obj['is_sortable'] = True
  main_obj['top_url'] = get_top_url(my_item_container)
  main_obj['title'] = my_item_container.item.title
  main_obj['last_modified'] = my_item_container.last_modified.strftime('%d.%m.%Y %H:%M')
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    order = ''
  user_perms = UserEditPerms(request.user.username, request.path)
  if user_perms.perm_manage or user_perms.perm_manage_folderish:
    items = get_folder_items(my_item_container, order)
  elif user_perms.perm_edit_own or user_perms.perm_manage_own:
    items = get_folder_own_items(my_item_container.item, order, request.user.id)
    my_title = my_title_own
  else:
    items = []
    my_title = _(u'Geeignete Überschrift')

  objs = get_feed_objs()
  tab_standard = t_standard.render(Context({'objs': objs, 'main_obj': main_obj}))
  vars, user_perms = get_base_vars(request, my_item_container, 'frame-main-manage', False)
  v = { 'tab_standard'     : tab_standard,
        'title'            : my_item_container.item.title,
        'action'           : get_folderish_actions(request, user_perms, my_item_container,
                                                   app_name, False, dont),
        'add_mode'         : user_perms.perm_add,
        'add_ons_0'        : add_ons[0],
        'add_ons_1'        : add_ons[1],
        'add_ons_2'        : add_ons[2],
        'add_ons_3'        : add_ons[3]
      }
  vars.update(v)
  return render_to_response ( 'app/rssfeedmanager/manage_rss_feeds.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage_site')
def rssfeedmanager_manage(request, item_container):
  """ Pflegemodus des Ordners """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/rssfeed/'),
                   'info': _(u'RSS-Feed')}, ]
  add_ons[1] = []
  add_ons[2] = []
  add_ons[3] = []

  app_name = 'rssfeedmanager'
  my_title = _(u'RSS-Feeds pflegen')
  my_title_own = _(u'Eigene RSS-Feeds pflegen')

  dont = { 'sort_mode': False, 'navigation_left_mode': False, 'navigation_mode': False,
           'import_mode': False, 'empty_mode': False, 'search_mode': False}
  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, my_title_own, dont)
