# -*- coding: utf-8 -*-
"""
/dms/linklist/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.03.2007  Beginn der Arbeit
0.02  09.05.2007  UMstellung auf do_manage
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def linklist_manage(request, item_container):
  """ Pflegemodus des Ordners """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/linkitem/'),
                   'info': _(u'Neuer Verweis')},
                 { 'url' : get_site_url(item_container,
                   'index.html/add/imagethumb/?max_width=120&max_height=60'),
                   'info': _(u'Minibild')}, ]
  add_ons[1] = [ { 'url' : get_site_url(item_container, 'index.html/add/linklist/'),
                   'info': _(u'Linkliste')}, ]
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = 'linklist'
  my_title = _(u'Linkliste pflegen')
  my_title_own = _(u'Eigene Verweise pflegen')

  dont = { 'navigation_left_mode': 0, 'navigation_mode': 0}
  return do_manage(request, item_container, user_perms, add_ons, app_name,
                   my_title, my_title_own, dont)
