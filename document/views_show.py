# -*- coding: utf-8 -*-
"""
/dms/document/views_show.py

.. zeigt den Inhalt eines Dokumentes an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.01.2007  Beginn der Arbeit
0.02  16.01.2007  text_more, is_wide, is_important direkt gesetzt
0.03  29.01.2007  get_prev_next_line
0.04  05.03.2007  has_comments
0.05  09.05.2007  get_item_vars_show
0.06  22.02.2008  Ausblenden der Hauptnavigation
"""

import re
import string

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_container
from dms.queries        import get_role_by_name

from dms.utils_form     import get_item_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def document_show(request,item_container):
  """ zeigt den Inhalt eines Dokumentes """
  app_name = u'document'
  vars = get_item_vars_show(request, item_container, app_name)
  parent = get_parent_container(item_container.container)
  vars['no_top_main_navigation'] = (parent.min_role_id < get_role_by_name('no_rights').id) or \
                                   item_container.container.nav_name_left.find('webquest') >= 0
  return render_to_response ( 'base-full-width.html', vars )
