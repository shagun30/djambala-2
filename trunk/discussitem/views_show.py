# -*- coding: utf-8 -*-
"""
/dms/discussitem/views_show.py

.. zeigt den Inhalt eines Diskussionsbeitrags an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.02.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def discussitem_show(request,item_container):
  """ zeigt den Inhalt eines Diskussionsbeitrags """
  app_name = 'discussitem'
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars = get_item_vars_show(request, item_container, app_name)
  vars['comments'] = comments
  return render_to_response ( 'base-full-width.html', vars )
