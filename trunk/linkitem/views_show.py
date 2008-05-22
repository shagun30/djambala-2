# -*- coding: utf-8 -*-
"""
/dms/linkitem/views_show.py

.. zeigt den Inhalt eines Verweises in einer Linkliste an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  10.05.2007  Beginn der Arbeit
0.02  17.05.2007  show_link
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def linkitem_show(request, item_container):
  """ zeigt Verweis """
  app_name = 'linkitem'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text_more'] = vars['text_more'] + show_link(item_container.item.url_more)
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars['comments'] = comments
  visibility = u', <i>[' + u'%s-%s' % \
                ( item_container.visible_start.strftime('%d.%m.%Y'),
                  item_container.visible_end.strftime('%d.%m.%Y') ) + u']</i>'
  vars['last_modified'] = item_container.get_last_modified() + visibility
  return render_to_response ( 'base-full-width.html', vars )
