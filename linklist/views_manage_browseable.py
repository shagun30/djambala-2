# -*- coding: utf-8 -*-
"""
/dms/linklist/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.05.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles  import *
from dms.folder.views_manage_browseable import do_manage_browseable

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def linklist_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    # --- die "Dateinamen" enthalten den Zeitstempel!
    order = '-name'
  dont = { 'sort_mode': 0, 'navigation_left_mode': 0, 'navigation_mode': 0}
  return do_manage_browseable(request, item_container, 'linklist', 
                              _(u'Verweise freischalten/löschen'),
                              ['dmsLinkItem'], order, dont=dont)
