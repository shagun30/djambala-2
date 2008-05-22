# -*- coding: utf-8 -*-
"""
/dms/export_dms/utils.py

.. enthaelt Hilfefunktionen fuer den Export
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.11.2007  Beginn der Arbeit
0.02  30.11.2007  Lernressourcen
"""

import string

from django.db          import transaction

from django.utils.encoding  import smart_unicode
from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_item_container_children
from dms.queries        import get_eduitem
from dms.queries        import get_extra_data

from dms.encode_decode  import encode_html
from dms.encode_decode  import decode_html

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
def get_xml(top_item_container, item_container):

  def get_item_list(query_set):
    res = []
    for q in query_set.all():
      res.append(q.id)
    return res

  def get_iso_date(date, with_time=False):
    if str(date).find('/') > 0:
      y, m, d = string.splitfields(str(date), '/')
    elif str(date).find('-') > 0:
      y, m, d = string.splitfields(str(date), '-')
    if with_time:
      ret = '%s-%s-%s 08:00' % (y, m, d)
    else:
      ret = '%s-%s-%s' % (y, m, d)
    if ret.find('GMT') >= 0:
      arr = string.splitfields(ret, 'GMT')
      ret = arr[0].strip()
    return ret

  def write_xml(name, line):
    if line == None:
      return write_xml(name, '')
    line = unicode(line)
    return '<%s>%s</%s>\n' % (name, line, name)

  def write_xml_text(name, line):
    if line == None:
      return write_xml(name, '')
    elif line.find('&') >= 0:
      return write_xml(name, '<![CDATA[' + line + ']]>')
    else:
      encoded_line = encode_html(line)
      return write_xml(name, '<![CDATA[' + encoded_line.replace('&lt;', '<').replace('&gt;', '>') + ']]>')

  def write_xml_list(names, name, items, default):
    if items == []:
      items = default
    res = ''
    for item in items:
      res += write_xml(name, '<![CDATA[' + smart_unicode(item).strip() + ']]>')
    return write_xml(names, res)

  def write_xml_boolean(name, flag):
    if flag:
      return write_xml(name, 1)
    else:
      return write_xml(name, 0)

  def do_write_xml(obj, name, default=''):
    if obj.hasProperty(name):
      return write_xml_text(name, obj[name])
    elif default == '':
      return ''
    else:
      return write_xml_text(name, default)

  # --------------------------------------------------------------------------
  data_rec = _(u'datensatz')
  res = ''
  res += '<%s>\n' % data_rec
  res += write_xml('zope_name', item_container.item.name)
  res += write_xml('name', item_container.item.name)
  res += write_xml('folder_path', item_container.container.path[len(top_item_container.container.path):])
  res += write_xml('app_name', item_container.item.app.name)
  res += write_xml('app_id', item_container.item.app.id)
  res += write_xml('owner_id', item_container.item.owner.id)
  res += write_xml('license_id', item_container.item.license.id)
  res += write_xml_text('title', item_container.item.title)
  res += write_xml_text('sub_title', item_container.item.sub_title)
  res += write_xml_text('text', item_container.item.text)
  res += write_xml_text('text_more', item_container.item.text_more)
  res += write_xml_text('url_more', item_container.item.url_more)
  res += write_xml_boolean('url_more_extern', item_container.item.url_more_extern)
  res += write_xml_text('image_url', item_container.item.image_url)
  res += write_xml_text('image_url_url', item_container.item.image_url_url)
  res += write_xml_boolean('image_extern', item_container.item.image_extern)
  res += write_xml_boolean('is_wide', item_container.item.is_wide)
  res += write_xml_boolean('is_important', item_container.item.is_important)
  res += write_xml_text('info_slot_right', item_container.item.info_slot_right)
  res += write_xml_boolean('has_user_support', item_container.item.has_user_support)
  res += write_xml_boolean('has_comments', item_container.item.has_comments)
  res += write_xml_boolean('is_moderated', item_container.item.is_moderated)
  res += write_xml_text('string_1', item_container.item.string_1)
  res += write_xml_text('string_2', item_container.item.string_2)
  res += write_xml('integer_1', item_container.item.integer_1)
  res += write_xml('integer_2', item_container.item.integer_2)
  res += write_xml('integer_3', item_container.item.integer_3)
  res += write_xml('integer_4', item_container.item.integer_4)
  res += write_xml('integer_5', item_container.item.integer_5)
  res += write_xml('integer_6', item_container.item.integer_6)
  #res += write_xml_text('extra', item_container.item.extra)
  
  # --- DmsItemContainer
  res += write_xml('container_id', -1)
  res += write_xml('item_id', -1)
  res += write_xml_boolean('is_deleted', item_container.is_deleted)
  res += write_xml('parent_item_id', -1)
  res += write_xml_text('section', item_container.section)
  res += write_xml('order_by', item_container.order_by)
  res += write_xml('part_of_id', item_container.part_of_id)
  res += write_xml_boolean('is_browseable', item_container.is_browseable)
  res += write_xml_boolean('is_data_object', item_container.is_data_object)
  res += write_xml_boolean('is_changeable', item_container.is_changeable)
  res += write_xml('visible_start', item_container.visible_start.strftime('%Y-%m-%d'))
  res += write_xml('visible_end', item_container.visible_end.strftime('%Y-%m-%d'))
  res += write_xml_text('last_modified', item_container.last_modified.strftime('%Y-%m-%d %H:%M:%S'))
  
  # --- DmsContainer
  res += write_xml('this_item_id', -1)
  res += write_xml('site_id', -1)
  res += write_xml('path', item_container.container.path[len(top_item_container.container.path):])
  res += write_xml_boolean('is_top_folder', item_container.container.is_top_folder)
  res += write_xml('min_role_id', item_container.container.min_role_id)
  res += write_xml_text('nav_title', item_container.container.nav_title)
  res += write_xml('menu_top_id', -1)
  res += write_xml('menu_left_id', -1)
  res += write_xml('nav_name_top', '')
  res += write_xml('nav_name_left', '')
  secs = []
  for i in string.splitfields(item_container.container.sections, '\n'):
    s = i.strip()
    if s != '':
      secs.append(i.strip())
  res += write_xml_list('sections', 'section', secs, [''])
  res += write_xml_boolean('show_next', item_container.container.show_next)
  
  # --- DmsEduItem
  data = get_eduitem(item_container.item)
  if data != None:
    extra = get_extra_data(item_container)
    if extra != None:
      schlagworte = []
      for i in string.splitfields(decode_html(extra['schlagwort_org']), '\n'):
        s = i.strip()
        if s != '':
          schlagworte.append(i.strip())
    else:
      schlagworte = []
    res += write_xml_text('autor', data.autor)
    res += write_xml_text('herausgeber', data.herausgeber)
    res += write_xml_text('anbieter_herkunft', data.anbieter_herkunft)
    res += write_xml_text('isbn', data.isbn)
    res += write_xml_text('preis', data.preis)
    res += write_xml_text('titel_lang', data.titel_lang)
    res += write_xml_text('beschreibung_lang', data.beschreibung_lang)
    res += write_xml_text('publikations_datum', data.publikations_datum)
    res += write_xml_text('standards_kmk', data.standards_kmk)
    res += write_xml_text('standards_weitere', data.standards_weitere)
    res += write_xml_text('techn_voraus', data.techn_voraus)
    res += write_xml_text('lernziel', data.lernziel)
    res += write_xml_text('lernzeit', data.lernzeit)
    res += write_xml_text('methodik', data.methodik)
    res += write_xml_text('lehrplan', data.lehrplan)
    res += write_xml_text('rechte', data.rechte)
    res += write_xml_list('fach_sachgebiete', 'fach_sachgebiet', get_item_list(data.fach_sachgebiet), [-1])
    res += write_xml_list('schlagworte', 'schlagwort', schlagworte, [''])
    res += write_xml_list('schularten', 'schulart', get_item_list(data.schulart), [-1])
    res += write_xml_list('schulstufen', 'schulstufe', get_item_list(data.schulstufe), [-1])
    res += write_xml_list('sprachen', 'sprache', get_item_list(data.sprache), [1]) # 'de'
    res += write_xml_list('zielgruppen', 'zielgruppe', get_item_list(data.zielgruppe), [-1])
  res += '</%s>\n\n' % data_rec
  return res

# -----------------------------------------------------
def convert_sql_to_xml(item_container):
  """ konvertiert alle Inhalte unterhalb von item_container in XML  """
  res = ''
  item_containers = get_item_container_children(item_container, True)
  for ic in item_containers:
    if ic != item_container and ic.item.app.is_folderish:
      res += get_xml(item_container, ic)
  for ic in item_containers:
    if ic != item_container and not ic.item.app.is_folderish:
      res += get_xml(item_container, ic)
  return res