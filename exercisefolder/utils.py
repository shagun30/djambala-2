# -*- coding: utf-8 -*-
"""
/dms/exercisefolder/utils.py

.. enthaelt Hilfefunktionen fuer Aufgabendatenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
"""

import string

from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

from dms.settings       import EXERCISE_LAYOUT

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_user_support(item_container):
  """ praesentiert die zur Verfuegung stehenden Ergaenzungsoptionen """
  return ''

# -----------------------------------------------------
def get_step_choices(current):
  ret = []
  if current < 1: ret.append((1, _(u'Stufe 1: Hauptthemen')))
  if current <= 2: ret.append((2, _(u'Stufe 2: Unterthemen')))
  if current >= 2: ret.append((3, _(u'Stufe 3: die eigentlichen Aufgaben')))
  return ret

# -----------------------------------------------------
def get_template_choices():
  ret = []
  for layout in EXERCISE_LAYOUT:
    ret.append((layout[0], layout[2]))
  return ret

# -----------------------------------------------------
def get_main_folder_name(item_container):
  """ liefert den Namen der Hauptseite """
  ic = item_container.get_parent()
  while ic.item.integer_2 >=2:
    ic = ic.get_parent()
  return ic.item.name