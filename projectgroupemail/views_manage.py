# -*- coding: utf-8 -*-
"""
/dms/projectgroupemail/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.01.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage
from dms.projectgroupemail.utils      import get_dont

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage')
def projectgroupemail_manage(request, item_container):
  """ Pflegemodus des Rundschreibens """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/projectgroupemailitem/'),
                   'info': _(u'Rundschreiben verfassen')}, ]
  add_ons[1] = [ { 'url' : get_site_url(item_container, 'index.html/add/projectgroupemail/'),
                   'info': _(u'Archiv für Rundschreiben')}, ]
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = 'projectgroupemail'
  my_title = _(u'Rundschreiben pflegen')
  my_title_own = ''

  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, 
                   my_title_own, get_dont())
