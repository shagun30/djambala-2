# -*- coding: utf-8 -*-
"""
/dms/edufolder/utils.py

.. enthaelt Hilfefunktionen fuer Lernarchive
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
0.02  27.08.2007  get_folder_content
0.03  19.11.2007  get_edufolder_content
0.04  28.11.2007  EDUFOLDER_INST_LOGO_URL
0.05  05.05.2008  get_data_url
0.06  06.05.2008  do_link_copy
"""

import string

from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

from dms.settings       import ELIXIER_LOGOS_PATH
from dms.settings       import ELIXIER_LOGOS_URL
from dms.settings       import EDUFOLDER_INST_LOGO_URL

from dms.models         import DmsItemContainer

from dms.queries        import get_site_url
from dms.queries        import get_extra_data
from dms.queries        import get_folder_filtered_items
from dms.queries        import get_lernrestyp_all
from dms.queries        import get_image_items
from dms.queries        import get_lernrestyp_all
from dms.queries        import get_lernrestyp_by_name
from dms.queries        import get_base_site_url
from dms.queries        import get_data_item_container
from dms.queries        import is_file_by_item_container
from dms.queries        import get_new_container_with_data
#from dms.queries        import get_new_item_container_instance
from dms.queries        import get_item_container_by_id
from dms.queries        import get_item_container_by_parent_item_id

from dms.views_clipboard  import do_link_copy

from dms.roles          import get_user_roles

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_edufolder_content(item_container):
  """ .. liefert die <item-container> vorhandenen Lernressourcen """
  app_types = ['dmsEduLinkItem', 'dmsEduTextItem', 'dmsEduFileItem',
               'dmsEduMediaItem', 'dmsEduWebquestItem', 'dmsEduGalleryItem',
               'dmsEduExerciseItem']
  items = get_folder_filtered_items(item_container, False, app_types)
  d_sections = {}
  sections = []
  lernrestypen = get_lernrestyp_all()
  for l in lernrestypen:
    sections.append(l.name)
    d_sections[l.id] = []
  #for s in string.splitfields(item_container.container.sections, '\n'):
  #  s = s.strip()
  #  if s != '':
  #    sections.append(s)
  #    d_sections[s] = []
  # --- Umsortieren
  d_sections['unknown'] = []
  for i in items :
    if d_sections.has_key(i.item.integer_3):
      d_sections[i.item.integer_3].append(i)
    else :
      d_sections['unknown'].append(i)
  items = []
  for s in sections :
    items += d_sections[get_lernrestyp_by_name(s).id]
  return items+d_sections['unknown'], sections, d_sections

# -----------------------------------------------------
def get_image_url(item_container):
  """ liefert die erste passende image_url """
  if item_container.item.image_url != '':
    return item_container.item.image_url
  item_container = item_container.get_parent()
  while item_container.item.app.name == 'dmsEduFolder':
    if item_container.item.image_url != '':
      return item_container.item.image_url
    item_container = item_container.get_parent()
  if item_container.item.app.name != 'dmsEduFolder':
    return ''

# -----------------------------------------------------
def get_extra(item_container):
  """ liefert die erste passende image_url """
  if item_container.item.extra != '':
    return get_extra_data(item_container)
  item_container = item_container.get_parent()
  while item_container.item.app.name == 'dmsEduFolder':
    if item_container.item.extra != '':
      return get_extra_data(item_container)
    item_container = item_container.get_parent()
  if item_container.item.app.name != 'dmsEduFolder':
    return None

# -----------------------------------------------------
def get_folder_content(item_container):
  """ .. liefert die in item_container enthaltenen Objekte: Verzeichnisse, Daten """
  items_temp = get_folder_filtered_items(item_container, False)
  # --- Anordnung von EduFoldern ueber "section"
  d_sections = {}
  l_sections = [] # EduFolder
  for s in string.splitfields(item_container.container.sections, '\n'):
    s = s.strip()
    if s != '' :
      l_sections.append(s)
      d_sections[s] = []
  d_sections['unknown'] = []
  # --- Anordnung der Lernressourcen
  d_lrtypen = {}
  l_lrtypen = []  # Lernobjekte
  lernrestyps = get_lernrestyp_all()
  for lernrestyp in lernrestyps:
    l_lrtypen.append(lernrestyp.id)
    d_lrtypen[lernrestyp.id] = []
  d_lrtypen['unknown'] = []
  # --- Listen fuer spezielle Objekte
  redirects = []  # Einblendungen
  news_item_container = -1
  # Listen mit Objekten belegen
  for i in items_temp:
    if i.item.app.name in ['dmsEduFolder', 'dmsRedirect']:
      if d_sections.has_key(i.section) :
        d_sections[i.section].append(i)
      else :
        d_sections['unknown'].append(i)
    elif i.item.app.name == 'dmsNewsboard':
      news_item_container = i
    else:
      if d_lrtypen.has_key(i.item.integer_3):
        d_lrtypen[i.item.integer_3].append(i)
      else :
        d_lrtypen['unknown'].append(i)
  items = []
  for s in l_sections:
    if s != []:
      items += d_sections[s]
  lrtypen = []
  lr_typen = []
  for lernrestyp in lernrestyps:
    if d_lrtypen[lernrestyp.id] != []:
      lrtypen += d_lrtypen[lernrestyp.id]
      lr_typen.append(lernrestyp)
  return news_item_container, items + d_sections['unknown'], l_sections, \
         lrtypen + d_lrtypen['unknown'], lernrestyps, lr_typen

# -----------------------------------------------------
def get_user_support(item_container, user, news_item_container=-1):
  """ praesentiert die zur Verfuegung stehenden Ergaenzungsoptionen """
  content = ''
  # Nur autorisierte Personen duerfen ergaenzen
  if item_container.item.has_user_support and user.is_authenticated():
    tSection = get_template('app/edufolder/user_support.html')
    cSection = Context ({ 'path': get_site_url(item_container, ''), })
    content = tSection.render ( cSection)
    roles = get_user_roles(user, item_container.container.path)
    # nur User mit genuegenden Rechten duerfen Medienpakete und
    # Webquests ergaenzen
    rights = ['the_manager', 'top_manager', 'manager', 'co_manager']
    if set(roles).intersection(set(rights)) != set([]):
      tSection = get_template('app/edufolder/user_support_ext.html')
      cSection = Context ({ 'path': get_site_url(item_container, ''), })
      content += tSection.render ( cSection)
    # nur falls ein Nachrichtenbrett vorhanden ist, koennen Nachrichten
    # ergaenzt werden
    if news_item_container >= 0:
      tSection = get_template('app/edufolder/user_support_news.html')
      cSection = Context ({ 'path': get_site_url(item_container, ''),
                            'news_name': news_item_container.item.name,
                        })
      content += tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_org_image_url(url, insert_own_log=False):
  """ liefert gegebenenfalls die URL zum Logo der betreffenden Institution """
  #n_pos = url[7:].find('/')  # [7:] um http:// zu ueberspringen
  #org_url = url[:n_pos+7+1]  # einschliesslich '/'
  item_containers = get_image_items(ELIXIER_LOGOS_PATH)
  image_url = image_url_url = ''
  image_url_extern = True
  for ic in item_containers:
    arr = string.splitfields(ic.item.sub_title, '|')
    for a in arr:
      b = a.strip()
      if b != '' and url.find(b) >= 0:
        image_url = ELIXIER_LOGOS_URL + ic.item.name
        image_url_url = ic.item.title
        image_url_extern = True
        break
      if image_url != '':
        break
  if insert_own_log and image_url == '':
    image_url = EDUFOLDER_INST_LOGO_URL
    image_url_url = get_base_site_url()
    image_url_extern = False
  return image_url, image_url_url, image_url_extern

# -----------------------------------------------------
def get_data_url(item_container):
  """ liefert die reale Adresse (eines eingeblendeten Objekts """
  tSection = get_template('app/edufolder/real_url.html')
  cSection = Context ({ 'data_url': get_data_item_container(item_container).get_absolute_url(), })
  return tSection.render(cSection)

# -----------------------------------------------------
def do_copy(request, paste_item_container, item_container):
  """ Objekte werden z.T. wirklich kopiert; andere Teile werden eingeblendet """
  is_file = is_file_by_item_container(paste_item_container)
  container = item_container.container
  if paste_item_container.item.app.is_folderish:
    container = get_new_container_with_data(paste_item_container.item.name,
                                            item_container,
                                            paste_item_container.container)
    container.save()
  item_container_old_id = paste_item_container.id
  new_item = paste_item_container.item.copy()
  new_item_container = DmsItemContainer()
  # --- Trick!
  if paste_item_container.item.app.is_folderish or \
    (paste_item_container.item.app.name == 'dmsDocument' or not paste_item_container.is_data_object):
    new_item_container = new_item_container.copy(paste_item_container, container, new_item, item_container.item.id)
  else:
      do_link_copy(request, paste_item_container, item_container)
  if paste_item_container.item.app.is_folderish:
    item_container_old = get_item_container_by_id(item_container_old_id)
    item_containers = get_item_container_by_parent_item_id(item_container_old.item.id)
    for i in item_containers:
      do_copy(request, i, paste_item_container)
  return new_item_container

# -----------------------------------------------------
def get_alter_choices():
  """ liefert die verschiedenen Lebensalter """
  ret = []
  ret.append((-1, 0))
  ret.append((5, u'V'))
  ret.append((6, 1))
  ret.append((7, 2))
  ret.append((8, 3))
  ret.append((9, 4))
  ret.append((10, 5))
  ret.append((11, 6))
  ret.append((12, 7))
  ret.append((13, 8))
  ret.append((14, 9))
  ret.append((15, 10))
  ret.append((16, 11))
  ret.append((17, 12))
  ret.append((18, 13))
  ret.append((20, u'E'))
  return ret
