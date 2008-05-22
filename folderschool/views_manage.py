# -*- coding: utf-8 -*-
"""
/dms/folderschool/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage
from dms.folder.utils         import get_add_ons

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def folderschool_manage(request, item_container):
  """ Pflegemodus des Ordners """
  user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container, False)
  app_name = 'folderschool'
  my_title = _(u'Basisordner für Schulen pflegen')
  my_title_own = _(u'XXX')

  dont = {'navigation_mode': False}
  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, my_title_own, dont)
