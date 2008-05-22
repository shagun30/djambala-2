# -*- coding: utf-8 -*-
"""
/dms/todolist/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def todolist_manage(request, item_container):
  """ Pflegemodus der To-Do-Liste """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/todoitem/'),
                   'info': _(u'Neuer Auftrag')},
               ]
  add_ons[1] = [ { 'url' : get_site_url(item_container, 'index.html/add/todolist/'),
                   'info': _(u'To-Do-Liste')}, ]
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = 'todolist'
  my_title = _(u'To-Do-iste pflegen')
  my_title_own = _(u'Aufträge pflegen')

  dont = { 'navigation_left_mode': 0, 'navigation_mode': 0}
  return do_manage(request, item_container, user_perms, add_ons, app_name,
                   my_title, my_title_own, dont)
