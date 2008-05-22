# -*- coding: utf-8 -*-
"""
/dms/rssfeed/utils.py

.. enthaelt Hilfsroutinen fuer RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  06.07.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_global_choices():
  """ """
  ret = []
  ret.append( (2, 'Globaler RSS-Feed') )
  ret.append( (1, 'Spezieller RSS-Feed') )
  return ret
