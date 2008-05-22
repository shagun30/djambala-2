# -*- coding: utf-8 -*-
"""
/dms/lecture/views_sort.py

.. enthaelt den View zum Sortieren der Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.01.2007  Beginn der Arbeit
0.02  26.01.2007  Beginn zur Umsetzung von drag 'n drop
0.03  27.01.2007  Reihenfolge der Zwischentitel wird ausgewertet
0.04  09.05.2007  Auslagerung der Sortierfunktionalitaet in dmsFolder
"""

from django.utils.translation import ugettext as _

from dms.roles              import *

from dms.folder.views_sort  import do_sort

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def lecture_sort(request, item_container):
  """ Objekte des Ordners umsortieren """

  return do_sort(request, item_container, 'lecture', _(u'Folien umordnen'))
