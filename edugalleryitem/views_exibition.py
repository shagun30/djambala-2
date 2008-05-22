# -*- coding: utf-8 -*-
"""
/dms/edugalleryitem/views_exibition.py

.. zeigt den Inhalt einer Galerie eines Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  03.11.2007  Beginn der Arbeit
"""

from dms.gallery.views_exibition            import gallery_exibition

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edugalleryitem_exibition(request, item_container):
  """ zeigt den Inhalt der Galerie als Ausstellung an """
  return gallery_exibition(request, item_container)
