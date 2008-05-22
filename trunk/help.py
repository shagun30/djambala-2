# -*- coding: utf-8 -*-
"""
/dms/help.py

.. zeigt Hilfetexte fuer dms-Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.01.2007  Beginn der Arbeit

FUNKTIONIERT NICHT !!!!!!!!!!!!!!!!!!!
"""

from django.utils.translation import ugettext as _

# -----------------------------------------------------
def show_help ( request, app, op ) :
  """ """
  s = app + '.form.get_help_'+op
  assert False
