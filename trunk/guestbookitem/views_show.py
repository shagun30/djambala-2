# -*- coding: utf-8 -*-
"""
/dms/guestbookitem/views_show.py

.. zeigt den Inhalt eines Gaestebcheintrags an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.02.2007  Beginn der Arbeit
0.02  05.03.2007  item_comment
0.03  09.05.2007  get_item_vars_show
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def guestbookitem_show(request,item_container):
  """ zeigt den Inhalt eines Gaestebucheintrags """
  app_name = 'guestbookitem'
  vars = get_item_vars_show(request, item_container, app_name)
  return render_to_response ( 'base-full-width.html', vars )
