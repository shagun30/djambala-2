# -*- coding: utf-8 -*-
"""
/dms/import_dms/utils.py

.. enthaelt Hilfefunktionen fuer den Import
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  27.04.2007  Beginn der Arbeit
"""

import string
import xml.dom.minidom
#from elementtree import ElementTree as et

from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.auth.models    import User

from dms.models         import DmsItem
from dms.models         import DmsItemContainer
from dms.models         import DmsContainer
from dms.models         import DmsApp
from dms.edufolder.models   import DmsEduItem

from dms.queries        import get_site_url
from dms.queries        import get_new_item_container
from dms.queries        import get_null_license
from dms.queries        import get_license_by_id
from dms.queries        import exist_item
from dms.queries        import get_new_container
from dms.queries        import get_item_container_by_path
from dms.queries        import get_app_by_id
from dms.queries        import get_container_by_id
from dms.queries        import get_min_max_menu_left

from dms.utils          import check_name
from dms.edulinkitem.utils      import save_schlagworte
from dms.utils_navigation       import save_menus_left
from dms.projectgroup.utils     import get_menu_left_from_sections
from dms.utils_navigation         import save_menus_left

# -----------------------------------------------------
def get_actions(request, user_perms, item_container):
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/file/manage_options.html')
  nPos = request.path.rfind('/add/')
  path = request.path[:nPos]
  show_mode = True
  c = Context ( { 'authenticated'  : request.user.is_authenticated(),
                  'show_mode'      : show_mode,
                  'user_perms'     : user_perms,
                  'user_name'      : request.user,
                  'path'           : get_site_url(item_container, 'index.html'), } )
  return t.render ( c)

# -----------------------------------------------------
def remove_control_chars ( rDocument ) :
  """ entfernt Sonderzeichen kleiner als Leerzeichen - primitiv!!! """
  ret = ''
  for c in rDocument :
    if c >= ' ' :
      ret += c
    elif c== '\r' or c=='\n' or c=='\t' :
      ret += c
  return ret

# -----------------------------------------------------
def convert_file(document):
  """ ersetzt Sonderzeichen - primitiv!! """
  document = string.replace ( document, '<br>', '<br />' )
  document = string.replace ( document, '&quot;' , '"' )
  document = string.replace ( document, '&#8364;' , 'Euro' )
  document = string.replace ( document, '&euro;'  , 'Euro' )
  document = string.replace ( document, u'ä'  , '&#228;' )
  document = string.replace ( document, 'ä'  , '&#228;' )
  document = string.replace ( document, u'ö'  , '&#246;' )
  document = string.replace ( document, 'ö'  , '&#246;' )
  document = string.replace ( document, u'ü'  , '&#252;' )
  document = string.replace ( document, 'ü'  , '&#252;' )
  document = string.replace ( document, u'ß' , '&#223;' )
  document = string.replace ( document, 'ß' , '&#223;' )
  document = string.replace ( document, u'Ä'  , '&#196;' )
  document = string.replace ( document, 'Ä'  , '&#196;' )
  document = string.replace ( document, u'Ö'  , '&#214;' )
  document = string.replace ( document, 'Ö'  , '&#214;' )
  document = string.replace ( document, u'Ü'  , '&#220;' )
  document = string.replace ( document, 'Ü'  , '&#220;' )
  document = string.replace ( document, '&Agrave;', '&#192;' )
  document = string.replace ( document, '&agrave;', '&#224;' )
  document = string.replace ( document, '&Acirc;' , '&#194;' )
  document = string.replace ( document, '&acirc;' , '&#226;' )
  document = string.replace ( document, '&AElig;' , '&#198;' )
  document = string.replace ( document, '&aelig;' , '&#230;' )
  document = string.replace ( document, '&Ccedil;', '&#199;' )
  document = string.replace ( document, '&ccedil;', '&#231;' )
  document = string.replace ( document, '&Egrave;', '&#200;' )
  document = string.replace ( document, '&egrave;', '&#232;' )
  document = string.replace ( document, '&Eacute;', '&#201;' )
  document = string.replace ( document, '&eacute;', '&#233;' )
  document = string.replace ( document, '&Ecirc;' , '&#202;' )
  document = string.replace ( document, '&ecirc;' , '&#234;' )
  document = string.replace ( document, '&Euml;'  , '&#203;' )
  document = string.replace ( document, '&euml;'  , '&#235;' )
  document = string.replace ( document, '&Icirc;' , '&#206;' )
  document = string.replace ( document, '&icirc;' , '&#238;' )
  document = string.replace ( document, '&Iuml;'  , '&#207;' )
  document = string.replace ( document, '&iuml;'  , '&#239;' )
  document = string.replace ( document, '&Ocirc;' , '&#212;' )
  document = string.replace ( document, '&ocirc;' , '&#244;' )
  #document = string.replace ( document, '&OElig;' , '&#338;' )
  #document = string.replace ( document, '&oelig;' , '&#339;' )
  document = string.replace ( document, '&Ugrave;', '&#217;' )
  document = string.replace ( document, '&ugrave;', '&#249;' )
  document = string.replace ( document, '&Ucirc;' , '&#219;' )
  document = string.replace ( document, '&ucirc;' , '&#251;' )
  #document = string.replace ( document, '&Yuml;'  , '&#376;' )
  document = string.replace ( document, '&yuml;'  , '&#255;' )
  document = string.replace ( document, '&raquo;' , '&#187;' )
  document = string.replace ( document, '&laquo;' , '&#171;' )
  document = string.replace ( document, '&iexcl;' , '&#161;' )
  document = string.replace ( document, '&ordf;'  , '&#170;' )
  document = string.replace ( document, '&ordm;'  , '&#186;' )
  document = string.replace ( document, '&iquest;', '&#191;' )
  document = string.replace ( document, '&OElig;' , 'XX' ) #338
  document = string.replace ( document, '&oelig;' , 'XX' ) #339
  document = string.replace ( document, '&Yuml;'  , 'XX' ) #376
  document = string.replace ( document, '&Aacute;', '&#193;' )
  document = string.replace ( document, '&Iacute;', '&#205;' )
  document = string.replace ( document, '&Ntilde;', '&#209;' )
  document = string.replace ( document, '&Oacute;', '&#211;' )
  document = string.replace ( document, '&Uacute;', '&#218;' )
  document = string.replace ( document, '&aacute;', '&#225;' )
  document = string.replace ( document, '&iacute;', '&#237;' )
  document = string.replace ( document, '&ntilde;', '&#241;' )
  document = string.replace ( document, '&oacute;', '&#243;' )
  document = string.replace ( document, '&uacute;', '&#250;' )
  document = remove_control_chars ( document )
  return document

def convert_line(line):
  line = string.replace ( line, '"', '&quot;' )
  #line = string.replace ( line, '&euro;'  , 'Euro' )
  line = string.replace ( line, u'&#228;', u'ä'   )
  line = string.replace ( line, u'&#246;', u'ö'   )
  line = string.replace ( line, u'&#252;', u'ü'   )
  line = string.replace ( line, u'&#223;', u'ß'  )
  line = string.replace ( line, u'&#196;', u'Ä'   )
  line = string.replace ( line, u'&#214;', u'Ö'   )
  line = string.replace ( line, u'&#220;', u'Ü'   )
  line = string.replace ( line, u'&#192;', u'&Agrave;' )
  line = string.replace ( line, u'&#224;', u'&agrave;' )
  line = string.replace ( line, u'&#194;', u'&Acirc;'  )
  line = string.replace ( line, u'&#226;', u'&acirc;'  )
  line = string.replace ( line, u'&#198;', u'&AElig;'  )
  line = string.replace ( line, u'&#230;', u'&aelig;'  )
  line = string.replace ( line, u'&#199;', u'&Ccedil;' )
  line = string.replace ( line, u'&#231;', u'&ccedil;' )
  line = string.replace ( line, u'&#200;', u'&Egrave;' )
  line = string.replace ( line, u'&#232;', u'&egrave;' )
  line = string.replace ( line, u'&#201;', u'&Eacute;' )
  line = string.replace ( line, u'&#233;', u'&eacute;' )
  line = string.replace ( line, u'&#202;', u'&Ecirc;'  )
  line = string.replace ( line, u'&#234;', u'&ecirc;'  )
  line = string.replace ( line, u'&#203;', u'&Euml;'   )
  line = string.replace ( line, u'&#235;', u'&euml;'   )
  line = string.replace ( line, u'&#206;', u'&Icirc;'  )
  line = string.replace ( line, u'&#238;', u'&icirc;'  )
  line = string.replace ( line, u'&#207;', u'&Iuml;'   )
  line = string.replace ( line, u'&#239;', u'&iuml;'   )
  line = string.replace ( line, u'&#212;', u'&Ocirc;'  )
  line = string.replace ( line, u'&#244;', u'&ocirc;'  )
  #line = string.replace ( line, '&OElig;' , '&#338;' )
  #line = string.replace ( line, '&oelig;' , '&#339;' )
  line = string.replace ( line, u'&#217;', u'&Ugrave;' )
  line = string.replace ( line, u'&#249;', u'&ugrave;' )
  line = string.replace ( line, u'&#219;', u'&Ucirc;'  )
  line = string.replace ( line, u'&#251;', u'&ucirc;'  )
  #line = string.replace ( line, '&Yuml;'  , '&#376;' )
  line = string.replace ( line, u'&#255;', u'&yuml;'   )
  line = string.replace ( line, u'&#187;', u'&raquo;'  )
  line = string.replace ( line, u'&#171;', u'&laquo;'  )
  line = string.replace ( line, u'&#161;', u'&iexcl;'  )
  line = string.replace ( line, u'&#170;', u'&ordf;'   )
  line = string.replace ( line, u'&#186;', u'&ordm;'   )
  line = string.replace ( line, u'&#191;', u'&iquest;' )
  #line = string.replace ( line, '&OElig;' , 'XX' ) #338
  #line = string.replace ( line, '&oelig;' , 'XX' ) #339
  #line = string.replace ( line, '&Yuml;'  , 'XX' ) #376
  line = string.replace ( line, u'&#193;', u'&Aacute;' )
  line = string.replace ( line, u'&#205;', u'&Iacute;' )
  line = string.replace ( line, u'&#209;', u'&Ntilde;' )
  line = string.replace ( line, u'&#211;', u'&Oacute;' )
  line = string.replace ( line, u'&#218;', u'&Uacute;' )
  line = string.replace ( line, u'&#225;', u'&aacute;' )
  line = string.replace ( line, u'&#237;', u'&iacute;' )
  line = string.replace ( line, u'&#241;', u'&ntilde;' )
  line = string.replace ( line, u'&#243;', u'&oacute;' )
  line = string.replace ( line, u'&#250;', u'&uacute;' )
  line = remove_control_chars ( line )
  return line

# -----------------------------------------------------
@transaction.commit_manually
def save_container(user, app, name, new, my_folder, license):
  """ Daten in DmsItem, Verbindung zu Container in DmsItemContainer """
  owners = User.objects.filter(username=new['owner'])
  if len(owners) > 0:
    owner = owners[0]
  else:
    owner = User.objects.filter(username=user)[0]
  container = get_new_container(name, my_folder)
  if new['nav_title'] != '' :
    container.nav_title = new['nav_title']
  else :
    container.nav_title = new['title']
    if len(container.nav_title) > 60:
      container.nav_title = container.nav_title[:60]
  container.sections = new['sections']
  container.save()
  # --- Eigenschaften des Ordners festlegen
  item = DmsItem.get_new_item(DmsItem(), name, new, my_folder, app, owner, license)
  item.save ()
  # --- Rueckverweis eintragen
  container.this_item_id = item.id
  container.save()
  try:
    section = new['section']
  except:
    section = ''
  if new.has_key('is_browseable'):
    is_browseable = new['is_browseable']
  else:
    is_browseable = True
  item_container = DmsItemContainer.save_values(
                      DmsItemContainer(), container, item, owner, is_browseable,
                      section, my_folder.item.id, order_by=new['order_by'])
  transaction.commit()
  return item_container

# -----------------------------------------------------
#@ transaction.commit_manually
def save_item(user, app, name, new, my_item_container, license):
  """ Daten in DmsItem, Verbindung zu Container in DmsItemContainer """
  owners = User.objects.filter(username=new['owner'])
  if len(owners) > 0:
    owner = owners[0]
  else:
    owner = User.objects.filter(username=user)[0]
  if len(new['sub_title']) > 199:
    new['sub_title'] = new['sub_title'][:199]
  item = DmsItem.get_new_item(DmsItem(), name, new, my_item_container,
                              app, owner, license)
  item.save()
  if new['visible_start'] == '':
    new['visible_start'] = '2007-01-01'
  if new['visible_end'] == '':
    new['visible_end'] = '2017-12-31'
  item_container = get_new_item_container(new, my_item_container, owner)
  item_container.item = item
  item_container.parent_item_id = my_item_container.container.this_item_id
  item_container.save()
  #transaction.commit()
  return item_container

# -----------------------------------------------------
def convert_xml_to_sql(user, content, my_folder):
  """ konvertiert content """
  
  def get_item_container(my_item_container, folder_path):
    if folder_path == '':
      return my_item_container
    if not folder_path.endswith('/'):
      folder_path += '/'
    new_path = my_item_container.container.path + folder_path
    folders = string.splitfields(folder_path, '/')
    container = DmsContainer.objects.filter(\
                    path=my_item_container.container.path + folders[0] + '/')[0]
    return DmsItemContainer.objects.filter(item__id=container.this_item_id)[0]

  #def getText(nodelist):
  #  rc = ""
  #  for node in nodelist:
  #    if node.nodeType == node.TEXT_NODE or node.nodeType == node.CDATA_SECTION_NODE:
  #      rc += node.data
  #  return rc
  
  def getText(nodelist):
      rc = ""
      for node in nodelist:
        if node.nodeType in [ node.TEXT_NODE, node.CDATA_SECTION_NODE]:
          rc += node.data
      return convert_line(rc)

  def getItem(rSatz, rName, default=''):
    try:
      nameObj = rSatz.getElementsByTagName(rName)[0]
      return getText(nameObj.childNodes)
    except:
      return default
  
  def getListItems(rSatz, rName, default=[]):
    items = rSatz.getElementsByTagName(rName)
    temp = []
    for i in items :
      temp.append(getText(i.childNodes))
    if temp == []:
      return default
    return temp
  
  def handle(rDom):
    """ """
    saetze = rDom.getElementsByTagName("datensatz")
    n = 0
    for satz in saetze:
      n += 1
      #print n
      new = {}
      new['zope_name']   = getItem(satz,'zope_name')
      new['folder_path'] = getItem(satz,'folder_path').replace(' ', '_')
      # --- DmsItem
      new['app_name']           = getItem(satz,'app_name')
      new['app_id']             = int(getItem(satz,'app_id', -1))
      new['owner_id']           = int(getItem(satz,'owner_id', -1))
      if not new.has_key('license'):
        new['license'] = get_null_license()
      else:
        new['license'] = get_license_by_id(new['license'])
      new['name']               = getItem(satz,'name')
      new['title']              = getItem(satz,'title')
      if new['title'] == '':
        dummy = getItem(satz,'my_title')
        new['title'] = getItem(satz,'my_title')
      if len(new['title']) >= 240:
        new['title'] = new['title'][:240]
      #if new['zope_name'] == 'afl/aflbio':
      #  assert False
      new['sub_title']          = getItem(satz,'sub_title')
      new['text']               = getItem(satz,'text').replace('&quot;', '"')
      new['text_more']          = getItem(satz,'text_more').replace('&quot;', '"')
      new['url_more']           = getItem(satz,'url_more')
      if len(new['url_more']) > 200:
        new['url_more'] = new['url_more'][:200]
      new['url_more_extern']    = int(getItem(satz,'url_more_extern', 0))
      new['image_url']          = getItem(satz,'image_url')
      new['image_url_url']      = getItem(satz,'image_url_url')
      new['image_extern']       = int(getItem(satz,'image_extern', 0))
      new['is_wide']            = int(getItem(satz,'is_wide', 0))
      new['is_important']       = int(getItem(satz,'is_important', 0))
      new['info_slot_right']    = getItem(satz,'info_slot_right')
      new['has_user_support']   = int(getItem(satz,'has_user_support', 0))
      new['has_comments']       = int(getItem(satz,'has_comments', 0))
      new['is_moderated']       = int(getItem(satz,'is_moderated', 1))
      new['string_1']           = getItem(satz,'string_1')
      new['string_2']           = getItem(satz,'string_2')
      if new['app_name'] in ['dmsPool']:
        new['string_1'] = ''
        new['string_2'] = ''
      new['integer_1']          = int(getItem(satz,'integer_1', -1))
      new['integer_2']          = int(getItem(satz,'integer_2', -1))
      new['integer_3']          = int(getItem(satz,'integer_3', -1))
      new['integer_4']          = int(getItem(satz,'integer_4', -1))
      new['integer_5']          = int(getItem(satz,'integer_5', -1))
      new['integer_6']          = int(getItem(satz,'integer_6', -1))
      new['extra']              = getItem(satz,'extra')
      new['last_modified']      = getItem(satz,'last_modified')
      # --- DmsItemContainer
      new['container_id']       = int(getItem(satz,'container_id', -1))
      new['item_id']            = int(getItem(satz,'item_id', -1))
      new['owner_id']           = int(getItem(satz,'owner_id', -1))
      new['is_deleted']         = int(getItem(satz,'is_deleted', 0))
      new['parent_item_id']     = int(getItem(satz,'parent_item_id', -1))
      new['section']            = getItem(satz,'section')
      new['order_by']           = int(getItem(satz,'order_by', 100))
      new['part_of_id']         = int(getItem(satz,'part_of_id', -1))
      new['is_browseable']      = int(getItem(satz,'is_browseable', 1))
      new['is_data_object']     = int(getItem(satz,'is_data_object', 1))
      new['is_changeable']      = int(getItem(satz,'is_changeable', 1))
      new['visible_start']      = getItem(satz,'visible_start')
      new['visible_end']        = getItem(satz,'visible_end')
      new['last_modified']      = getItem(satz,'last_modified')
      # --- DmsEduItem
      new['autor']              = getItem(satz,'autor')
      new['herausgeber']        = getItem(satz,'herausgeber')
      new['anbieter_herkunft']  = getItem(satz,'anbieter_herkunft')
      new['isbn']               = getItem(satz,'isbn')
      new['preis']              = getItem(satz,'preis')
      new['titel_lang']         = getItem(satz,'titel_lang')
      new['beschreibung_lang']  = getItem(satz,'beschreibung_lang')
      new['publikations_datum'] = getItem(satz,'publikations_datum')
      new['standards_kmk']      = getItem(satz,'standards_kmk')
      new['standards_weitere']  = getItem(satz,'standards_weitere')
      new['techn_voraus']       = getItem(satz,'techn_voraus')
      new['lernziel']           = getItem(satz,'lernziel')
      new['lernzeit']           = getItem(satz,'lernzeit')
      new['methodik']           = getItem(satz,'methodik')
      new['lehrplan']           = getItem(satz,'lehrplan')
      new['rechte']             = getItem(satz,'rechte')

      new['fach_sachgebiet']    = getListItems(satz, 'fach_sachgebiet', [-1] )
      new['schlagwort']         = getListItems(satz, 'schlagwort', [] )
      new['schulart']           = getListItems(satz, 'schulart', [-1] )
      new['schulstufe']         = getListItems(satz, 'schulstufe', [-1] )
      new['sprache']            = getListItems(satz, 'sprache', [-1] )
      new['zielgruppe']         = getListItems(satz, 'zielgruppe', [-1] )

      # --- Speicherung in integer_1 ...
      new['valid_days']         = int(getItem(satz,'valid_days', -1))
      new['has_timetable']      = int(getItem(satz,'has_timetable', 0))
      new['owner']              = getItem(satz,'owner')
      new['owner_email']        = getItem(satz,'owner_email')
      # --- DmsContainer
      new['this_item_id']       = int(getItem(satz,'this_item_id', -1))
      new['site_id']            = int(getItem(satz,'site_id', -1))
      new['path']               = getItem(satz,'path').replace(' ', '_')
      new['is_top_folder']      = int(getItem(satz,'is_top_folder', 0))
      new['min_role_id']        = int(getItem(satz,'min_role_id', -1))
      new['nav_title']          = getItem(satz,'nav_title')
      if len(new['nav_title']) >= 60:
        new['nav_title'] = new['nav_title'][:60]
      new['menu_top_id']        = int(getItem(satz,'menu_top_id', 1))
      new['menu_left_id']       = int(getItem(satz,'menu_left_id', 1))
      new['nav_name_top']       = getItem(satz,'nav_name_top')
      new['nav_name_left']      = getItem(satz,'nav_name_left')
      # Leerzeichen entfernen
      sec = getItem(satz,'sections')
      arr = string.splitfields(sec, '\n')
      sec = ''
      for i in arr:
        s = i.strip()
        if s != '':
          sec += i.strip() + '\r\n'
      new['sections']  = sec
      new['show_next'] = int(getItem(satz,'show_next', 0))
      # --- eventuell Owner korrigieren
      if new['owner_id']==-1 and new['string_2'].find('@')>0:
        users = User.objects.filter(email=new['string_2'])
        if len(users) > 0:
          new['owner_id'] = users[0].id
      if new['owner_id']==-1 and new['owner_email'].find('@')>0:
        users = User.objects.filter(email=new['owner_email'])
        if len(users) > 0:
          new['owner_id'] = users[0].id

      if new['app_name'] == '' and new['app_id'] > -1:
        new['app_name'] = get_app_by_id(new['app_id']).name
      if new['app_name'] != '':
        is_file = (new['app_name'] in ['dmsFile', 'dmsEduFile', 
                                       'dmsImage', 'dmsImagethumb'])
        app = DmsApp.objects.filter(name=new['app_name'])[0]
        name = check_name(new['name'], app.is_folderish or is_file)

        if new['container_id'] < 0:
          abs_path = my_folder.container.path + new['folder_path']
        else:
          abs_path = get_container_by_id(new['container_id']).path
        if not abs_path.endswith('/'):
          abs_path += '/'
        # --- Gibt es schon ein Objekt gleichen Namens?
        item_container = get_item_container_by_path(abs_path)
        #e = exist_item(item_container, name)
        if item_container == None or not exist_item(item_container, name):
          if item_container == None and app.is_folderish:
            if item_container == None:
              parent_path = abs_path[:1+abs_path[:-1].rfind('/')]
              item_container = get_item_container_by_path(parent_path)
            if item_container != None:
              #assert False
              item_container_new = save_container(user, app, name, new, item_container, new['license'])
          elif item_container != None and not app.is_folderish:
            item_container_new = save_item(user, app, name, new,
                                           item_container, new['license'])
          elif app.is_folderish:
            item_container_new = save_container(user, app, name, new, item_container, new['license'])
          app_id = new['app_id']
          if app_id == 26:  # Arbeitsgruppe
            n_min, n_max = get_min_max_menu_left()
            menu_left_id = 1 + max(abs(n_min), n_max)
            new['sections'] = _(u'Kommunikation\nKooperation\nDokumente\n')
            text = get_menu_left_from_sections(item_container_new, name, new['sections'],
                                              ['kommunikation', 'dokumente', 'kooperation'])
            save_menus_left(menu_left_id, text)
            item_container_new.item.menu_left_id = menu_left_id
            item_container_new.item.nav_name_left = 'start|'
            item_container_new.item.save()
          elif app_id == 30 or app_id in [38, 39, 40, 41]:
            edu_item = DmsEduItem.save_values(DmsEduItem(), item_container_new,
                                              new, True)
            for i in new['fach_sachgebiet']:
              edu_item.fach_sachgebiet.add(i)
            for i in new['schulart']:
              edu_item.schulart.add(i)
            for i in new['schulstufe']:
              edu_item.schulstufe.add(i)
            for i in new['sprache']:
              try:
                edu_item.sprache.add(int(i))
              except:
                if i == 'en':
                  i = 2
                elif i == 'fr':
                  i = 3
                else:
                  i = 1
                edu_item.sprache.add(int(i))
            for i in new['zielgruppe']:
              edu_item.zielgruppe.add(i)
            schlagworte = ''
            for s in new['schlagwort']:
              schlagworte += s + '\n'
            new['schlagwort'] = schlagworte
            save_schlagworte(edu_item, new)

  #content = convert_file(content)
  if content != '':
    if content.find('<?xml') < 0:
      content = """<?xml version="1.0" encoding="ISO-8859-15"?>
<!DOCTYPE lieferung SYSTEM "http://www.bildungsserver.de/lieferung/lieferung.dtd">
<lieferung>""" + content + '</lieferung>'
    # Korrektur von Unicode-Zeichen
    #content = content.replace(u'–', u'-').replace(u'€', u'&euro;').replace(u'„', u'"').replace(u'“', u'"')
    dom = xml.dom.minidom.parseString(content)
    handle(dom)
    dom.unlink()
