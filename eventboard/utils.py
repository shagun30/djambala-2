# -*- coding: utf-8 -*-
"""
/dms/eventboard/utils.py

.. enthaelt Hilfefunktionen fuer Terminkalender
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.06.2007  Beginn der Dokumentation
"""

import datetime

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.models         import DmsItemContainer
from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_folder_own_items(item, order, user_id) :
  """ liefert in dem Ordner enthaltenen Objekte """
  my_filter = [u"parent_item_id=%i AND owner_id=%s" % (item.folder_id, user_id)]
  return DmsItem.objects.select_related().\
                 extra(where=my_filter).order_by('-last_modified')

# -----------------------------------------------------
def get_folder_content(item_container, mode='new', order_increasing=True):
  # --- mode = 'new', 'old', 'all'
  if order_increasing:
    ordering = 'visible_start'
  else:
    ordering = 'visible_end'
  if mode == 'all':
    items = DmsItemContainer.objects.select_related().\
                             filter(parent_item_id=item_container.item.id). \
                             filter(is_browseable=True). \
                             filter(is_deleted=False). \
                             order_by(ordering)
  elif mode == 'new':
    today = datetime.datetime.today()
    items = DmsItemContainer.objects.select_related().\
                             filter(parent_item_id=item_container.item.id). \
                             filter(is_browseable=True). \
                             filter(is_deleted=False). \
                             filter(visible_end__gte=today). \
                             order_by(ordering)
  else:
    today = datetime.datetime.today()
    items = DmsItemContainer.objects.select_related().\
                             filter(parent_item_id=item_container.item.id). \
                             filter(is_browseable=True). \
                             filter(is_deleted=False). \
                             filter(visible_end__lt=today). \
                             order_by(ordering)
  return items

def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/eventboard/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content
