# -*- coding: utf-8 -*-
"""
/dms/eduexerciseitem/views_sort.py

.. enthaelt den View zum Sortieren der Objekte in Aufgaben
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles              import *

from dms.folder.views_sort  import do_sort

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def eduexerciseitem_sort(request, item_container):
  """ Objekte der Aufgabe fuer Lernarchiv umsortieren """

  return do_sort(request, item_container, 'eduexerciseitem', _(u'Aufgaben umordnen'))

