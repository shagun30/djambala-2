# -*- coding: utf-8 -*-
"""
/dms/image/views_download.py

.. enthaelt den View zum Donwload einer geschuetzten Grafik/ eines Bildes
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.01.2008  Beginn der Arbeit
"""

from dms.file.views_download import file_download

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def image_download(request, item_container):
  """ Vorbereitungen zum Senden einer geschuetzten Grafik """
  return file_download(request, item_container)
