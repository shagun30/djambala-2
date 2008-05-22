# -*- coding: utf-8 -*-
"""
/dms/gallery/utils.py

.. enthaelt Hilfefunktionen fuer Galerien
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.10.2007  Beginn der Arbeit
0.02  01.11.2007  get_exibition_url
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_dont():
  return { 'navigation_mode': False}

# -----------------------------------------------------
def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/gallery/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_exibition_url(item_container):
  """ liefert die Basis-Adresse der Ausstellung """
  if item_container.item.app.is_folderish:
    obj = item_container
  else:
    obj = item_container.get_parent()
  return obj.get_absolute_url() + '/exibition/'


