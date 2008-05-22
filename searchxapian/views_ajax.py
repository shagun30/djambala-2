#-*-coding: utf-8 -*-
"""
/dms/searchxapian/views_ajax.py

.. enthaelt Ajax-Funktion fuer User-Management
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.12.2007  Beginn der Arbeit
"""

from django.http              import HttpResponse

from django.utils.translation import ugettext as _

from dms.queries              import get_schlagworte

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def searcheduxapian_ajax_get_schlagwort(request, item_container):
  """ moegliche Schlagworte """
  schlagworte = get_schlagworte(request.GET['query'])
  res = '<items>\n'
  for schlagwort in schlagworte:
    res += '<schlagwort>\n<name><![CDATA[%s]]></name>\n</schlagwort>\n' % schlagwort.name
  res += '</items>\n'
  return HttpResponse(res, mimetype="text/xml; charset=utf-8")
