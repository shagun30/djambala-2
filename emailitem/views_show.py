# -*- coding: utf-8 -*-
"""
/dms/emailitem/views_show.py

.. zeigt den Inhalt der Frage an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.01.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.survey.utils   import get_form_tab_row
from dms.utils_form     import get_item_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def emailitem_show(request,item_container):
  """ zeigt den Inhalt der betreffenden Frage """
  app_name = u'emailitem'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = '<table>' + get_form_tab_row(item_container, request.user, None, {}, {}) +'</table>'
  return render_to_response ( 'base-full-width.html', vars )
