# -*- coding: utf-8 -*-
"""
/dms/folder/views_sort.py

.. enthaelt den View zum Sortieren der Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.01.2007  Beginn der Arbeit
0.02  26.01.2007  Beginn zur Umsetzung von drag 'n drop
0.03  27.01.2007  Reihenfolge der Zwischentitel wird ausgewertet
"""

import string

from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_tabbed_form
from dms.utils          import get_folderish_actions
from dms.utils_form     import get_base_vars

from dms.encode_decode  import decode_html

from dms.folder.utils       import get_folder_content
from dms.folder.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_drag_list(sections, d_sections):
  """ """
  js_template = '  dragsort.makeListSortable(document.getElementById("order_by_%i"), verticalOnly, saveOrder);\n'
  js_head = ''
  list_str = ''
  input_str = u'<input name="var_order_by_0" type="hidden" value="dummy" />\n'
  header = '--START--'
  js_head += js_template % 0
  n_max = 0
  for section in sections:
    list_str += u'<li style="position:relative;" itemid="ZT_%s"><b>%s: %s</b></li>\n' % \
                (section, 'Zwischentitel', section)
    for item_container in d_sections[section]:
      form_str = u'<li style="position:relative; background-color: #f0f0f0;" ' + \
                 u'itemid="%i">%s [<a href="%s/edit/?id=%i">%s</a>]</li>\n'
      list_str += form_str % \
                  (item_container.item.id, item_container.item.title, 
                   item_container.get_absolute_url(), item_container.id, item_container.item.name)
      n_max += 1
  # --- gibt es unbekannte Zuordnungen
  section = 'unknown'
  if d_sections.has_key(section) and d_sections[section] != []:
    for item_container in d_sections[section]:
      list_str += u'<li style="position:relative; background-color: #f0f0f0;" itemid="%i">%s [%s]</li>\n' % \
                  (item_container.item.id, '*** ' + item_container.item.title + ' ***',
                   item_container.item.name)
      n_max += 1
  list_str = u'<ul id="order_by_0" class="boxy">\n' + list_str + '</ul>\n'
  return js_head, list_str, input_str, n_max

def do_resort(sort_order):
  """ """
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
      curr_section = i[3:]
      sections_str += curr_section + '\n'
  return d, sections_str

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
    s = request.POST['sections']
    if s != item_container.container.sections:
      item_container.container.sections = s
      item_container.container.save()
  change_values = request.POST.has_key('drag_item_form')
  if change_values:
    items, sections, d_sections = get_folder_content(item_container, False, app_types)
    order_by_ids, new_sections_str = do_resort(request.POST['var_order_by_0'])
    n = 0
    c = []
    for i in items:
      if app_types==[] or i.item.app.name in app_types:
        has_changed = False
        if order_by_ids[i.item.id][0] != i.order_by:
          i.order_by = order_by_ids[i.item.id][0]
          has_changed = True
        sec = order_by_ids[i.item.id][1]
        if sec != i.section:
          i.section = sec
          has_changed = True
        if has_changed:
          i.save()
    # --- wurde die Reihenfolge der Zwischentitel geaendert?
    n = new_sections_str
    if item_container.container.sections != n:
      item_container.container.sections = n
      item_container.container.save()
  items, sections, d_sections = get_folder_content(item_container, False, app_types)
  js_head, drag_list, input_str, n_drag_titles = get_drag_list(sections, d_sections)
  max_items = len(items)
  # --- Zwischentitel
  data_init = {'sections' : decode_html(item_container.container.sections,) }
  f = dms_itemForm(data_init)
  tabs = [('tab_sections' , ['sections',]), ]
  sec_content = get_tabbed_form(tabs, help_form, 'lecture' , f, False)

  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage')
  v = { 'objs'      : objs,
        'js_head'   : js_head,
        'drag_list' : drag_list,
        'input_str' : input_str,
        'max_items' : n_drag_titles,
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
  return render_to_response ( 'app/base_sort.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def folder_sort(request, item_container):
  """ Objekte des Ordners umsortieren """
  return do_sort(request, item_container, 'folder', _(u'Ordner, Seiten etc. umordnen'))
