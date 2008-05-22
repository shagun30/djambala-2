# -*- coding: utf-8 -*-
"""
/dms/edugalleryitem/views_show.py

.. zeigt den Inhalt der Galerie in einem Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.11.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_eduitem
from dms.utils_form     import get_item_vars_show
from dms.edulinkitem.views_show import get_details
from dms.gallery.views_show   import gallery_show

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edugalleryitem_show(request, item_container):
  """ zeigt den Inhalt eines Materialpools """

  app_name = u'edugalleryitem'
  # --- Detail-Ansicht
  if request.GET.has_key('show_details'):
    vars = get_item_vars_show(request, item_container, app_name,
                              ignore_own_breadcrumb=True)
    data = get_eduitem(item_container.item)
    vars['text_more'] += get_details(item_container, True, data)
    if item_container.item.has_comments:
      comments = item_comment(request, item_container=item_container)
    else:
      comments = ''
    vars['comments'] = comments
    return render_to_response ( 'base-full-width.html', vars )

  return gallery_show(request, item_container)
