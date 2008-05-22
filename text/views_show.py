# -*- coding: utf-8 -*-
"""
/dms/text/views_show.py

.. zeigt den Inhalt einer Textseite an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.05.2007  Beginn der Arbeit
"""

from django.http              import HttpResponse

from django.utils.translation import ugettext as _

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def text_show(request,item_container):
  """ zeigt den Inhalt eines Dokumentes """
  return HttpResponse(item_container.item.text, mimetype='text/plain')
