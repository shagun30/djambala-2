# -*- coding: utf-8 -*-
"""
/dms/rssfeedmanager/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.03.2007  Beginn der Arbeit
"""

from django.utils.encoding  import smart_unicode
from django.http            import HttpResponseRedirect
from django.shortcuts       import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_all_feed_items

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.utils          import get_folderish_actions

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def rssfeedmanager_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """

  def save_values(request, items):
    """ """
    checked = request.POST.copy()
    for i in items:
      visible_key = 'visible_' + smart_unicode(i.id)
      delete_key  = 'delete_' + smart_unicode(i.id)
      if checked.has_key(delete_key):
        i.delete()
      else:
        if i.is_browseable and not checked.has_key(visible_key):
          i.is_browseable = False
          i.save()
        elif not i.is_browseable and checked.has_key(visible_key):
          i.is_browseable = True
          i.save()

  app_name = 'rssfeedmanager'
  my_title = _(u'Beiträge für RSS-Feeds freischalten/löschen')
  main_obj = {}
  main_obj['url']  = get_site_url(item_container, 'index.html')
  user_perms = UserEditPerms(request.user.username,request.path)
  objs = []
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    order = ''
  my_item = item_container.item
  items = get_all_feed_items(order)

  has_user_folder = False
  for feed_item in items :
    obj = {}
    obj['id'] = feed_item.id
    obj['title'] = feed_item.item_container.item.title
    obj['feed_title'] = feed_item.feed.title
    obj['url']  = get_site_url(feed_item.item_container, feed_item.item_container.item.name)
    obj['is_deleted'] = feed_item.is_deleted
    obj['last_modified'] = feed_item.last_modified.strftime('%m/%d/%Y %H:%M')
    obj['is_browseable'] = feed_item.is_browseable
    objs.append ( obj )

  if request.method == 'POST' :
    save_values(request, items)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html/manage_browseable/'))
  else:
    dont = { 'navigation_mode': False, 'sort_mode': False, 'manage_mode': False, 'import_mode': False }
    vars={'content_div_style': 'frame-main-manage',
          'site'             : item_container.container.site,
          'user_perms'       : user_perms,
          'main_obj'         : main_obj,
          'objs'             : objs,
          'id'               : my_item.id,
          'title'            : my_title,
          'sub_title'        : my_item.title,
          'action'           : get_folderish_actions(request, user_perms, item_container, app_name, 
                                                    has_user_folder, dont),
          'breadcrumb'       : get_breadcrumb(item_container),
          'add_mode'         : user_perms.perm_add,
          'content'          : '',
          'next'             : get_site_url(item_container, 'index.html/manage_browseable/'),
          'footer_email'     : get_footer_email(item_container.item),
          'last_modified'    : item_container.get_last_modified()
        }
    return render_to_response ( 'app/rssfeedmanager/base_manage_browseable.html', vars )

