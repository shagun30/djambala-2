# -*- coding: utf-8 -*-
"""
/dms/faqitem/views_show.py

.. zeigt den Inhalt eines FAQ-Beitrags an
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def faqitem_show(request,item_container):
  """ zeigt den Inhalt eines FAQ-Beitrags """
  app_name = 'faqitem'
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars = get_item_vars_show(request, item_container, app_name)
  vars['comments'] = comments
  return render_to_response ( 'app/faqitem/base-item.html', vars )
