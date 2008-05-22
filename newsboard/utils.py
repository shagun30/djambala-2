# -*- coding: utf-8 -*-
"""
/dms/newsboard/utils.py

.. enthaelt Hilfefunktionen fuer Nachrichtenbretter
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  22.01.2007  navigation_mode
"""

import datetime

from django.utils.translation import ugettext as _

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.models         import DmsItemContainer
from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_folder_own_items(item, order, user_id) :
  """ liefert in dem Ordner enthaltenen Objekte """
  my_filter = [u"parent_item_id=%i AND owner_id=%s" % (item.folder_id, user_id)]
  return DmsItem.objects.select_related().extra(where=my_filter).order_by('-last_modified')

# -----------------------------------------------------
def get_folder_content(item_container, mode='new'):
  # --- mode = 'new', 'old', 'all'
  if mode == 'all':
    items = DmsItemContainer.objects.select_related().filter(parent_item_id=item_container.item.id). \
                                                      filter(is_browseable=True). \
                                                      filter(is_deleted=False). \
                                                      order_by('-item__name')
    #order_by('-dms_dmsitem.name')
  elif mode == 'new':
    today = datetime.datetime.today()
    items = DmsItemContainer.objects.select_related().filter(parent_item_id=item_container.item.id). \
                                                      filter(is_browseable=True). \
                                                      filter(is_deleted=False). \
                                                      filter(visible_start__lte=today). \
                                                      filter(visible_end__gte=today). \
                                                      order_by('-item__name')
  else:
    today = datetime.datetime.today()
    items = DmsItemContainer.objects.select_related().filter(parent_item_id=item_container.item.id). \
                                                      filter(is_browseable=True). \
                                                      filter(is_deleted=False). \
                                                      filter(visible_end__lt=today). \
                                                      order_by('-item__name')
  return items

def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/newsboard/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content
