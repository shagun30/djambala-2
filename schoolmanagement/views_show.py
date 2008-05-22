# -*- coding: utf-8 -*-
"""
/dms/schoolmanagement/views_show.py

.. zeigt Verwaltung der Schulseiten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  20.05.2005  Beginn der Arbeit
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
def schoolmanagement_show(request,item_container):
  """ zeigt den Inhalt eines Dokumentes """
  app_name = u'schoolmanagement'
  vars = get_item_vars_show(request, item_container, app_name)
  parent = get_parent_container(item_container.container)
  vars['no_top_main_navigation'] = (parent.min_role_id < get_role_by_name('no_rights').id) or \
                                   item_container.container.nav_name_left.find('webquest') >= 0
  return render_to_response ( 'base-full-width.html', vars )
