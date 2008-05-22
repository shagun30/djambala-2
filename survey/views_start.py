# -*- coding: utf-8 -*-
"""
/dms/survey/views_start.py

.. enthaelt den View zum Starten der Dateneingabe des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.01.2008  Beginn der Arbeit
"""

from django.http          import HttpResponseRedirect

from dms.roles            import require_permission
from dms.queries          import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def survey_start(request, item_container):
  """ Eingaben in den Fragebogens unterbinden """
  item_container.item.integer_2 = 1
  item_container.item.save()
  return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
