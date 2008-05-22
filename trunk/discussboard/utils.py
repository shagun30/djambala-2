# -*- coding: utf-8 -*-
"""
/dms/discusscoard/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.07.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

# -----------------------------------------------------
def get_dont():
  return { 'sort_mode': 0, 'navigation_mode': 0}

# -----------------------------------------------------
def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/discussboard/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render(cSection)
  return content
