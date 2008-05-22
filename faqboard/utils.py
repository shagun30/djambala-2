# -*- coding: utf-8 -*-
"""
/dms/faqboard/utils.py

.. enthaelt Hilfefunktionen fuer FAQ-Listen
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

# -----------------------------------------------------
def get_dont():
  #return { 'sort_mode': 0, 'navigation_mode': 0}
  return { 'navigation_mode': 0}

# -----------------------------------------------------
def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/faqboard/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render(cSection)
  return content
