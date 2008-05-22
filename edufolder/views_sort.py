# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_sort.py

.. enthaelt den View zum Sortieren der Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
"""

import string

from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_lernrestyp_by_name
from dms.queries        import get_lernrestyp_by_id
from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_tabbed_form
from dms.utils          import get_folderish_actions
from dms.utils_form     import get_base_vars

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.folder.utils       import get_folder_content
from dms.edufolder.utils    import get_edufolder_content
from dms.folder.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_drag_folder_list(sections, d_sections):
  """ """
  js_template = '  dragsort.makeListSortable(document.getElementById("folder_order_by_%i"), verticalFolderOnly, saveFolderOrder);\n'
  js_head = ''
  list_str = ''
  input_folder_str = u'<input name="var_folder_order_by_0" type="hidden" value="dummy" />\n'
  header = '--START--'
  js_head += js_template % 0
  n_max = 0
  for section in sections:
    list_str += u'<li style="position:relative;" itemid="ZT_%s"><b>%s: %s</b></li>\n' % \
                (section, 'Zwischentitel', section)
    for item_container in d_sections[section]:
      list_str += u'<li style="position:relative; background-color: #f0f0f0;" itemid="%i">%s [%s]</li>\n' % \
                  (item_container.item.id, item_container.item.title, item_container.item.name)
      n_max += 1
  # --- gibt es unbekannte Zuordnungen
  section = 'unknown'
  if d_sections.has_key(section) and d_sections[section] != []:
    for item_container in d_sections[section]:
      list_str += u'<li style="position:relative; background-color: #f0f0f0;" itemid="%i">%s [%s]</li>\n' % \
                  (item_container.item.id, '*** ' + item_container.item.title + ' ***',
                   item_container.item.name)
      n_max += 1
  list_str = u'<ul id="folder_order_by_0" class="boxy">\n' + list_str + '</ul>\n'
  return js_head, list_str, input_folder_str, n_max

# -----------------------------------------------------
def get_drag_res_list(js_head, sections, d_sections):
  """ """
  js_template = '  dragsort.makeListSortable(document.getElementById("res_order_by_%i"), verticalResOnly, saveResOrder);\n'
  #js_head = ''
  list_str = ''
  input_res_str = u'<input name="var_res_order_by_0" type="hidden" value="dummy" />\n'
  header = '--START--'
  js_head += js_template % 0
  n_max = 0
  for section in sections:
    list_str += u'<li style="position:relative;" itemid="ZT_%s"><b>%s: %s</b></li>\n' % \
                (section, _(u'Materialtyp'), section)
    for item_container in d_sections[get_lernrestyp_by_name(section).id]:
      list_str += u'<li style="position:relative; background-color: #f0f0f0;" itemid="%i">%s [%s]</li>\n' % \
                  (item_container.item.id, item_container.item.title, item_container.item.name)
      n_max += 1
  # --- gibt es unbekannte Zuordnungen
  section = 'unknown'
  if d_sections.has_key(section) and d_sections[section] != []:
    for item_container in d_sections[section]:
      list_str += u'<li style="position:relative; background-color: #f0f0f0;" itemid="%i">%s [%s]</li>\n' % \
                  (item_container.item.id, '*** ' + item_container.item.title + ' ***',
                   item_container.item.name)
      n_max += 1
  if list_str != '':
    list_str = u'<ul id="res_order_by_0" class="boxy">\n' + list_str + '</ul>\n'
  return js_head, list_str, input_res_str, n_max

# -----------------------------------------------------
def do_resort(sort_order):
  """ sortiert Lernarchive um """
  d = {}
  sections_str = ''
  item_ids = string.splitfields(sort_order, '|')
  curr = 100
  curr_section = ''
  for i in item_ids:
    try:
      d[int(i)] = (curr, curr_section)
      curr += 10
    except:
      curr_section = i[3:] # ZT_ entfernen
      sections_str += curr_section + '\n'
  return d, sections_str

# -----------------------------------------------------
def do_res_resort(sort_order):
  """ sortiert Lernressourcen um """
  d = {}
  item_ids = string.splitfields(sort_order, '|')
  curr = 100
  curr_section = ''
  for i in item_ids:
    try:
      d[int(i)] = (curr, curr_section)
      curr += 10
    except:
      curr_section = i[3:] # ZT_ entfernen
  return d

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def do_sort(request, item_container, app_name, my_title, app_types=[]):
  """ Objekte des Ordners umsortieren """

  class dms_itemForm ( forms.Form ) :
    sections = forms.CharField(required=False,
                     widget=forms.Textarea( attrs={'rows':5, 'cols':40,
                                                   'style':'width:50%;'}) )

  my_item = item_container.item
  objs = []
  has_user_folder = False
  user_perms = UserEditPerms(request.user.username,request.path)

  # wurden Zwischentitel geloescht, ergaenzt, umgeordnet?
  if request.POST.has_key('sections_form'):
    s = encode_html(request.POST['sections'])
    if s != item_container.container.sections:
      item_container.container.sections = s
      item_container.container.save()
  # --- gegebenenfalls Reihenfolge der Lernarchive aendern
  if request.POST.has_key('drag_item_folder_form'):
    items, sections, d_sections = get_folder_content(item_container, False, app_types)
    order_by_ids, new_sections_str = do_resort(request.POST['var_folder_order_by_0'])
    n = 0
    c = []
    for i in items:
      if app_types==[] or i.item.app.name in app_types:
        has_changed = False
        if order_by_ids[i.item.id][0] != i.order_by:
          i.order_by = order_by_ids[i.item.id][0]
          has_changed = True
        sec = encode_html(order_by_ids[i.item.id][1])
        if sec != i.section:
          i.section = sec
          has_changed = True
        if has_changed:
          i.save()
    # --- wurde die Reihenfolge der Zwischentitel geaendert?
    n = encode_html(new_sections_str)
    if item_container.container.sections != n:
      item_container.container.sections = n
      item_container.container.save()
  
  # --- gegebenenfalls Reihenfolge der Lernressourcen aendern
  if request.POST.has_key('drag_item_res_form'):
    items, sections, d_sections = get_edufolder_content(item_container)
    order_by_ids = do_res_resort(request.POST['var_res_order_by_0'])
    n = 0
    c = []
    for i in items:
      has_changed = False
      if order_by_ids[i.item.id][0] != i.order_by:
        i.order_by = order_by_ids[i.item.id][0]
        i.save()
      sec = encode_html(order_by_ids[i.item.id][1])
      if sec != get_lernrestyp_by_id(i.item.integer_3).name:
        i.item.integer_3 = get_lernrestyp_by_name(sec).id
        i.item.save()
  # --- Online-Lernarchive
  items, sections, d_sections = get_folder_content(item_container, False, app_types)
  js_head, drag_folder_list, input_folder_str, n_drag_titles = \
           get_drag_folder_list(sections, d_sections)
  max_items = len(items)
  
  # --- Lernressourcen
  items, sections, d_sections = get_edufolder_content(item_container)
  js_head, drag_res_list, input_res_str, n_drag_res_titles = \
           get_drag_res_list(js_head, sections, d_sections)
  
  # --- Zwischentitel
  data_init = {'sections' : decode_html(item_container.container.sections,) }
  f = dms_itemForm(data_init)
  tabs = [('tab_sections' , ['sections',]), ]
  sec_content = get_tabbed_form(tabs, help_form, 'lecture' , f, False)

  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage')
  v = { 'objs'      : objs,
        'js_head'   : js_head,
        'drag_folder_list' : drag_folder_list,
        'input_folder_str' : input_folder_str,
        'max_folder_items' : n_drag_titles,
        'drag_res_list'    : drag_res_list,
        'input_res_str'    : input_res_str,
        'max_res_items'    : n_drag_res_titles,
        'id'        : my_item.id,
        'title'     : my_title,
        'sub_title' : my_item.title,
        'name'      : my_item.name,
        'action'    : get_folderish_actions(request, user_perms, item_container, app_name,
                                            item_container.item.has_comments,
                                            {'browseable_mode': False,
                                             'navigation_mode': False}),
        'sec_content': sec_content
      }
  vars.update(v)
  vars['image_url'] = ''
  vars['text'] = ''
  vars['text_more'] = ''
  return render_to_response ( 'app/edufolder/base_sort.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def edufolder_sort(request, item_container):
  """ Objekte des Lernarchivs umsortieren """

  return do_sort(request, item_container, 'edufolder', _(u'Lernressourcen umordnen'),
                 ['dmsEduFolder', 'dmsRedirect'])

