# -*- coding: utf-8 -*-
"""
/dms/eventboard/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.06.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles  import *
from dms.folder.views_manage_browseable import do_manage_browseable

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def eventboard_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  dont = { 'sort_mode': 0, 'navigation_left_mode': 0, 'navigation_mode': 0}
  return do_manage_browseable(request, item_container, 'eventboard', 
                              _(u'Termine freischalten/löschen'),
                              ['dmsEventItem'], '-name', dont=dont )
