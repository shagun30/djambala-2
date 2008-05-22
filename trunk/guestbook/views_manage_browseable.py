# -*- coding: utf-8 -*-
"""
/dms/guestbook/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2007  Beginn der Arbeit
0.02  09.05.2007  do_manage_browseable
"""

from django.utils.translation import ugettext as _

from dms.roles  import *
from dms.folder.views_manage_browseable import do_manage_browseable

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def guestbook_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  return do_manage_browseable(request, item_container, 'guestbook', 
                              _(u'Einträge freischalten/löschen'),
                              ['dmsGuestbookItem'], '-name' )
