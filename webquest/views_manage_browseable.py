# -*- coding: utf-8 -*-
"""
/dms/webquest/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht des Webquests
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles        import require_permission
from dms.folder.views_manage_browseable import do_manage_browseable

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def webquest_manage_browseable(request, item_container):
  """ Freigabemodus des Webquests """
  return do_manage_browseable(request, item_container, 'webquestitem', 
                              _(u'Lernressourcen freischalten/löschen') )
