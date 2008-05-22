# -*- coding: utf-8 -*-
"""
/dms/edugalleryitem/utils.py

.. enthaelt Hilfefunktionen fuer Edu-Galerien
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_user_support(item_container, authenticated):
  """ """
  if item_container.item.has_user_support and authenticated:
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/edugalleryitem/user_support.html')
    cSection = Context ({ 'path': get_site_url(item_container, ''), })
    content = tSection.render ( cSection)
    return content
  else:
    return ''
