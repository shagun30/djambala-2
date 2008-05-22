# -*- coding: utf-8 -*-
"""
/dms/edumediaitem/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht des Medienpakts
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles        import require_permission
from dms.folder.views_manage_browseable import do_manage_browseable

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edumediaitem_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  return do_manage_browseable(request, item_container, 'edumediaitem', 
                              _(u'Lernressourcen freischalten/löschen') )
