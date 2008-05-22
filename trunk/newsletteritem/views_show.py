# -*- coding: utf-8 -*-
"""
/dms/newsletteritem/views_show.py

.. zeigt den Inhalt eines Diskussionsbeitrags an
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.11.2007  Beginn der Arbeit
0.02  17.12.2007  Autor-Name, Template show_item.html
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def newsletteritem_show(request,item_container):
  """ zeigt den Inhalt eines Beitrags zum Newsletter """
  app_name = 'newsletteritem'
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars = get_item_vars_show(request, item_container, app_name)
  vars['comments'] = comments
  vars['author']           = item_container.item.owner.username
  vars['author_full_name'] =item_container.item.owner.get_full_name()
  #return render_to_response ( 'base-full-width.html', vars )
  return render_to_response ( 'app/newsletter/show_item.html', vars )
