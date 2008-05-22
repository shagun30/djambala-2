# -*- coding: utf-8 -*-
"""
/dms/edufileitem/utils.py

.. enthaelt Hilfefunktionen fuer Dateien in Lernarchiven
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_URL

from dms.queries        import get_item_container_data_object_by_id

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_edu_file_url(item_container):
  """ liefert die URL der eigentlichen Datei """
  # --- PROBLEM Einblendung
  if item_container.is_data_object:
    file_url = DOWNLOAD_URL + item_container.container.path
  else:
    real_item_container = get_item_container_data_object_by_id(item_container.item.id)
    if real_item_container != None:
      file_url = DOWNLOAD_URL + real_item_container[0].container.path
    else:
      file_url = ''
  return file_url + item_container.item.name
  ## --- ..[:-5] entfernt '.html' von <name>
  #return file_url + item_container.item.name[:-5]
