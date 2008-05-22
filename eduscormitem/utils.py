# -*- coding: utf-8 -*-
"""
/dms/eduscormitem/utils.py

.. enthaelt Hilfefunktionen fuer Scorm-Player
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.03.2008  Beginn der Arbeit
"""

import string, os, time
import pickle
from xml.dom import minidom, Node

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_URL
from dms.settings       import DOWNLOAD_PROTECTED_PATH

from dms.utils          import unzip

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_scorm_pathes(item_container, folder_name):
  """ liefert die Scorm-Pfade """
  if item_container.container.is_protected():
    file_path = DOWNLOAD_PROTECTED_PATH
  else:
    file_path = DOWNLOAD_PATH
  file_path += item_container.container.path
  base_folder = file_path + folder_name
  scorm_folder = base_folder + '/scorm/'
  nav_folder = base_folder + '/navigation/'
  return file_path, base_folder, scorm_folder, nav_folder

# -----------------------------------------------------
def walk(node_list, parent_node, level):
  """ http://docs.huihoo.com/homepage/dkuhlman/pyxmlfaq.html """
  for node in parent_node.childNodes:
    if node.nodeType == Node.ELEMENT_NODE:
      this_node = {}
      node_name = node.nodeName
      this_node[node_name] = ''
      attrs = node.attributes
      for attrName in attrs.keys():
        attrNode = attrs.get(attrName)
        attrValue = attrNode.nodeValue
        this_node[attrName] = attrValue
      # Walk over any text nodes in the current node.
      content = []
      for child in node.childNodes:
        if child.nodeType == Node.TEXT_NODE:
          value = child.nodeValue.strip()
          if value != '':
            content.append(value)
      #if content:
      strContent = string.join(content)
      this_node[node_name] = strContent
      this_node['level'] = level
      # Walk the child nodes.
      node_list.append(this_node)
      node_list = walk(node_list, node, level+1)
  return node_list

def convert_xml(inFileName):
  """ erzeugt aus imsmanifest-Datei die Navigationsdatenstruktur """
  doc = minidom.parse(inFileName)
  rootNode = doc.documentElement
  level = 0
  node_list = walk([], rootNode, level)
  # Ressourcen
  res_dir = {}
  for node in node_list:
    if node.has_key('type') and node['type'] == 'webcontent':
      res_dir[node['identifier']] = node['href']
  # Navigationsknoten zusammenbauen
  start_of_items = False
  end_of_items = False
  index = 0
  nav_list = []
  min_level = -1
  for node in node_list:
    if node.has_key('item'):
      start_of_items = True
    if start_of_items and node.has_key('adlcp:scormtype') and node['adlcp:scormtype'] == 'sco':
      break
    if start_of_items and not end_of_items and node.has_key('item'):
      if min_level < 0:
        min_level = node['level']
      nav_list.append( {'level': node['level'] - min_level, 
                        'href': res_dir[node['identifierref']], 
                        'title': node_list[index+1]['title'] } )
    index += 1
  return nav_list
  """
  doc = minidom.parse(inFileName)
  rootNode = doc.documentElement
  level = 0
  node_list = walk([], rootNode, level)
  # Ressourcen
  res_dir = {}
  for node in node_list:
    if node.has_key('adlcp:scormtype') and node['adlcp:scormtype'] == 'sco':
      res_dir[node['identifier']] = node['href']
  # Navigationsknoten zusammenbauen
  start_of_items = False
  end_of_items = False
  index = 0
  nav_list = []
  min_level = -1
  for node in node_list:
    if node.has_key('item'):
      start_of_items = True
    if start_of_items and node.has_key('adlcp:scormtype') and node['adlcp:scormtype'] == 'sco':
      break
    if start_of_items and not end_of_items and node.has_key('item'):
      if min_level < 0:
        min_level = node['level']
      nav_list.append( {'level': node['level'] - min_level, 
                        'href': res_dir[node['identifierref']], 
                        'title': node_list[index+1]['title'] } )
    index += 1
  return nav_list
  """

# -----------------------------------------------------
def create_navigation(item_container, folder_name):
  """ """
  file_path, base_folder, scorm_folder, nav_folder = get_scorm_pathes(item_container, folder_name)
  # --- Manifest auswerten
  nav_list = convert_xml(scorm_folder + 'imsmanifest.xml')
  f = open(nav_folder + 'navigation.pickle', 'w')
  pickle.dump(nav_list, f, 2)
  f.close()

# -----------------------------------------------------
def save_scorm_packet(folder_name, name, files, item_container):
  """ Scorm-Paket speichern und auspacken """

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
  file_path, base_folder, scorm_folder, nav_folder = get_scorm_pathes(item_container, folder_name)
  create_folder(scorm_folder)
  create_folder(nav_folder)
  # --- Scorm-Paket speichern
  scorm_file = '%s/%s.%s' % (base_folder, folder_name, 'zip')
  f = open(scorm_file, 'wb')
  f.write(content)
  f.close()
  os.chmod(scorm_file, 0660)
  # --- Scorm-Paket auspacken
  unzip(scorm_file, scorm_folder)
  # --- Navigation erzeugen
  create_navigation(item_container, folder_name)
  return base_folder

# -----------------------------------------------------
def delete_package(item_container):
  """ loescht alle Datei-Objekte """
  folder_name = item_container.item.name
  file_path, base_folder, scorm_folder, nav_folder = get_scorm_pathes(item_container, folder_name)
  command = 'rm -fr %s' % base_folder
  os.system(command)
