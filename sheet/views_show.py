# -*- coding: utf-8 -*-
"""
/dms/sheet/views_show.py

.. zeigt den Inhalt eines Dokumentes an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.02.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_item_vars_show
from dms.utils          import get_prev_next_line
from dms.views_comment  import item_comment
from dms.utils          import get_item_actions

from dms.roles          import *

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def sheet_show(request, item_container):
  """ zeigt den Inhalt eines Dokumentes """
  app_name = 'sheet'
  vars = get_item_vars_show(request, item_container, app_name)
  user_perms = UserEditPerms(request.user.username,request.path)
  if item_container.container.show_next:
    prev_next = get_prev_next_line(item_container)
  else:
    prev_next = ''
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars = get_item_vars_show(request, item_container, app_name)
  vars.update ( { 'content_div_style': 'frame-main-manage',
                  'this_site_title'  : parent.item.title,
                  'no_top_main_navigation': True,
                  'text_more'        : '',
                  'is_wide'          : True,
                  'comments'         : comments,
                  'show_next'        : prev_next,
                } )
  return render_to_response ( 'app/sheet/base.html', vars )
