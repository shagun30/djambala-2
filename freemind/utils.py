# -*- coding: utf-8 -*-
"""
/dms/freemind/utils.py

.. enthaelt Hilfefunktionen fuer Informationsseiten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.03.2008  Beginn der Arbeit
"""

import string, os, time

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_URL
from dms.settings       import DOWNLOAD_PROTECTED_PATH
from dms.settings       import FREEMIND_PATH

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_file_size(item_container, is_protected=False):
  """ liefert die Dateigroesse """
  file_path, base_folder = get_freemind_pathes(item_container, item_container.item.name)
  try:
    st = os.stat(base_folder + '/this.mm')
    return st[6]
  except:
    return -1

# -----------------------------------------------------
def get_file_modification_date(item_container, format='german', is_protected=False):
  """ liefert das Datum der letzten Aenderung """
  file_path, base_folder = get_freemind_pathes(item_container, item_container.item.name)
  try:
    st = os.stat(base_folder + '/this.mm')
    if format == '':
      return st[8]
    elif format == 'german':
      return time.strftime('%d.%m.%Y %H:%M',time.localtime(st[8]))
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(st[8]))
  except:
    return '0.0.000'

# -----------------------------------------------------
def get_freemind_pathes(item_container, folder_name):
  """ liefert die Freemind-Pfade """
  if item_container.container.is_protected():
    file_path = DOWNLOAD_PROTECTED_PATH
  else:
    file_path = DOWNLOAD_PATH
  file_path += item_container.container.path
  base_folder = file_path + folder_name
  return file_path, base_folder

# -----------------------------------------------------
def save_mindmap(folder_name, name, files, item_container):
  """ Freemind-Datei speichern und mit Flash-Player versehen """

  def create_folder(path):
    """ erzeugt das Verzeichnis und setzt die Zugriffsrechte """
    try:
      os.makedirs(path)
    except:
      pass
    os.chmod(path, 0750)

  content = files['fname']['content']
  content_type = files['fname']['content-type']
  filename = files['fname']['filename']
  file_path, base_folder = get_freemind_pathes(item_container, folder_name)
  create_folder(base_folder)
  # --- Scorm-Paket speichern
  freemind_file = '%s/this.mm' % base_folder
  f = open(freemind_file, 'wb')
  f.write(content)
  f.close()
  os.chmod(freemind_file, 0660)
  # --- umhuellende Dateien kopieren
  command = 'cp -p %s/* %s' % (FREEMIND_PATH, base_folder)
  os.system(command)
  return base_folder

# -----------------------------------------------------
def delete_package(item_container):
  """ loescht alle Datei-Objekte """
  folder_name = item_container.item.name
  file_path, base_folder = get_freemind_pathes(item_container, folder_name)
  command = 'rm -fr %s/' % base_folder
  os.system(command)
