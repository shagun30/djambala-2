# -*- coding: utf-8 -*-
"""
/dms/newsitem/views_show.py

.. zeigt den Inhalt einer Nachricht an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.03.2007  Beginn der Arbeit
0.02  09.05.2007  get_item_vars_show
0.03  21.01.2008  datetime
"""

import datetime

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.utils_base     import show_link
from dms.views_comment  import item_comment

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def newsitem_show(request,item_container):
  """ zeigt Verweis """
  app_name = 'newsitem'
  vars = get_item_vars_show(request, item_container, app_name)
  if vars['url_more'] != '':
    link = show_link(vars['url_more'], _(u'Weitere Infos ...'), vars['url_more_extern'])
    vars['text_more'] += '\n<p>\n' + link + '</p>\n'
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
  if item_container.visible_end < datetime.datetime.now():  #.strftime('%Y-%m-%d'):
    vars['title'] = _(u'Abgelaufene Nachricht') + ' - ' + vars['title']
  return render_to_response ( 'base-full-width.html', vars )
