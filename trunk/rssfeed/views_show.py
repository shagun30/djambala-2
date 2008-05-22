# -*- coding: utf-8 -*-
"""
/dms/rssfeed/views_show.py

.. zeigt RSS-Feed an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.07.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def rssfeed_show(request,item_container):
  """ zeigt den Inhalt eines Dokumentes """
  app_name = 'rssfeed'
  vars = get_item_vars_show(request, item_container, app_name)
  return render_to_response ( 'base-full-width.html', vars )
