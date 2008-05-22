# -*- coding: utf-8 -*-
"""
/dms/surveyitem/utils.py

.. enthaelt Hilfsroutinen fuer Fragen des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.01.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_yes_no_choices():
  """ liefert Ja/Nein-Feld """
  ret = []
  ret.append( (1, _(u'Ja')) )
  ret.append( (0, _(u'Nein')) )
  return ret

