# -*- coding: utf-8 -*-
"""
/dms/surveyitem/views_show.py

.. zeigt den Inhalt der Frage an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.01.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.survey.utils   import get_form_tab_row
from dms.utils_form     import get_item_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def surveyitem_show(request,item_container):
  """ zeigt den Inhalt eines Dokumentes """
  app_name = u'surveyitem'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = '<table>' + get_form_tab_row(item_container, request.user, None, {}, {}) +'</table>'
  return render_to_response ( 'base-full-width.html', vars )
