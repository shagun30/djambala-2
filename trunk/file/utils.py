# -*- coding: utf-8 -*-
"""
/dms/file/utils.py

.. enthaelt Hilfefunktionen fuer Informationsseiten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.02.2007  Beginn der Arbeit
"""

import string, os, time

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_id
from dms.queries        import get_item_container_by_item_id
from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_URL
from dms.settings       import DOWNLOAD_PROTECTED_PATH

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_item_container_base(item_container):
  """ liefert das wahre item_container-Objekt """
  if item_container.is_data_object:
    return item_container
  else:
    return get_item_container_by_id(item_container.part_of_id)

# -----------------------------------------------------
def get_actions(request, user_perms, item_container):
  """ liefer moegliche Aktionen """
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/file/manage_options.html')
  nPos = max ( string.rfind ( request.path, '/add/' ),
               string.rfind ( request.path, '/edit/' ),
             )
  if nPos > -1 :
    path = request.path[:nPos]
    show_mode = True
  else :
    path = request.path
    show_mode = False
  if ( string.find(request.path, '/add/') >= 0 ) :
    edit_mode = False
  elif ( string.find(request.path, '/edit/') >= 0 ) :
    edit_mode = False
  else :
    edit_mode = request.user.is_authenticated()
  c = Context ( { 'authenticated'  : request.user.is_authenticated(),
                  'show_mode'      : show_mode,
                  'edit_mode'      : edit_mode,
                  'user_perms'     : user_perms,
                  'user_name'      : request.user,
                  'path'           : get_site_url(item_container, item_container.item.name), } )
  return t.render ( c)

# -----------------------------------------------------
def get_folder_name(item_container, is_protected):
  """ liefert den Pfad der Datei """
  ic = get_item_container_base(item_container)
  if is_protected:
    return DOWNLOAD_PROTECTED_PATH + ic.container.path
  else:
    return DOWNLOAD_PATH + ic.container.path

# -----------------------------------------------------
def get_file_name(item_container, is_protected):
  """ liefert den Pfad der Datei """
  ic = get_item_container_base(item_container)
  if is_protected:
    return DOWNLOAD_PROTECTED_PATH + ic.container.path + item_container.item.name
  else:
    return DOWNLOAD_PATH + ic.container.path + item_container.item.name

# -----------------------------------------------------
def get_file_size(item_container, is_protected=False):
  """ liefert die Dateigroesse """
  filename = get_file_name(item_container, is_protected)
  try:
    st = os.stat(filename)
    return st[6]
  except:
    return -1

# -----------------------------------------------------
def get_file_modification_date(item_container, format='german', is_protected=False):
  """ liefert das Datum der letzten Aenderung """
  filename = get_file_name(item_container, is_protected)
  try:
    st = os.stat(filename)
    if format == '':
      return st[8]
    elif format == 'german':
      return time.strftime('%d.%m.%Y %H:%M',time.localtime(st[8]))
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(st[8]))
  except:
    return '0.0.000'

# -----------------------------------------------------
def get_file_url(item_container, is_protected=False):
  """ liefert die entsprechende URL """
  ic = get_item_container_base(item_container)
  #filename = get_file_name(item_container, is_protected)
  if is_protected:
    return get_site_url(ic, item_container.item.name) + '/download/'
  else:
    return DOWNLOAD_URL + ic.container.path + item_container.item.name

# -----------------------------------------------------
def get_file_path(item_container):
  """ """
  ic = get_item_container_base(item_container)
  if item_container.container.is_protected():
    file_path = DOWNLOAD_PROTECTED_PATH
  else:
    file_path = DOWNLOAD_PATH
  if item_container.item.app.is_folderish:
    return file_path + ic.container.path
  else:
    return file_path + ic.container.path + item_container.item.name

# -----------------------------------------------------
def save_file(name, files, item_container, fname='fname'):
  """ Datei speichern """
  content = files[fname]['content']
  content_type = files[fname]['content-type']
  filename = files[fname]['filename']
  if item_container.container.is_protected():
    file_path = DOWNLOAD_PROTECTED_PATH
  else:
    file_path = DOWNLOAD_PATH
  file_path += item_container.container.path
  try:
    os.makedirs(file_path)
  except:
    pass
  os.chmod(file_path, 0750)
  file_name = file_path + name
  f = open(file_name, 'wb')
  f.write(content)
  f.close()
  os.chmod(file_name, 0660)
  return file_name