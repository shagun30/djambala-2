#-*-coding: utf-8 -*-
"""
/dms/utils_navigation.py

.. enthaelt Hilfsroutinen zurm Aendern des linken Navigationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.03.2007  Beginn der Arbeit
0.02  11.10.2007  item.is_main_menu
"""

import string

from django.utils.safestring  import SafeData, mark_safe, SafeUnicode
from django.utils.translation import ugettext as _

from dms.queries        import delete_menuitem_navmenu_left
from dms.queries        import get_menuitems_by_menu_id_left
from dms.queries        import get_new_navmenu_left
from dms.queries        import delete_menuitem_navmenu_top
from dms.queries        import get_new_navmenu_top

from dms.encode_decode  import decode_html

# -----------------------------------------------------
def get_navmenu_choices_left(menu_id):
  """ Auswahl des Navigationsmenus """
  ret = []
  ret.append( ('|', mark_safe(_('<b><i>(Lokale) Startseite</i></b>'))) )
  menu = get_menuitems_by_menu_id_left(menu_id)[0]
  lines = string.splitfields(menu.navigation, '\n')
  nav_main = ''
  nav_sub = ''
  for line in lines:
    line = string.strip(line)
    if line != '' and line[0] != '#':
      arr = string.splitfields(line, '|')
      if len(arr) > 1:
        my_depth = int(string.strip(arr[0]))
        my_alias = string.strip(arr[1])
        if my_depth == 0:
          nav_main = my_alias
          nav_sub = ''
        else:
          nav_sub = my_alias
        info = string.strip(arr[3])
        if my_depth == 0:
          info = '<b>' + info + '</b>'
        ret.append( (nav_main + '|' + nav_sub, mark_safe(info)) )
  return ret

# -----------------------------------------------------
def get_data_left(line):
  """ Beschreibung der linken Navigation """
  line = string.strip(line)
  if line == '' or line[0] == '#':
    return -1, -1, ''
  arr = string.splitfields(line, '|')
  if len(arr) == 1:
    return -999, -1, '<div style="padding:0.3em;"></div>\n'
  else:
    ret = ''
    my_depth = int(string.strip(arr[0]))
    my_alias = string.strip(arr[1])
    link = string.strip(arr[2])
    info = string.strip(arr[3])
    if len(arr) > 4:
      title = string.replace(string.strip(arr[4]), '"', '&quot;')
    else:
      title = ''
    if len(arr) > 5 :
      ret += string.replace(arr[5], '&quot;', '"') + '&nbsp;'
      ret += u'<a class="navLink" href="%s" title="%s">' % (link, title)
      ret += '<b>' + info + '</b></a><span class="invisible">|</span>'
    else:
      ret += u'<a class="navLink" href="%s" title="%s">' % (link, title)
      ret += info + '</a><span class="invisible">|</span>'
  return my_depth, my_alias, ret

# -----------------------------------------------------
def get_top_navigation_menu_left(lines):
  """ Beschreibung der oberen Navigation """
  ret = ''
  for line in lines:
    my_depth, my_alias, res = get_data_left(line)
    if my_depth == 0:
      if res != '' and string.find(res, '<div') < 0:
        res_start = '<div class="menu_border_bottom">'
        res_end = '</div>\n'
      else:
        res_start = ''
        res_end = ''
      ret += res_start + res + res_end
    elif my_depth == -999:
      ret += res
  return ret

# -----------------------------------------------------
def get_data_top(line, nav_main='', profi_mode=False):
  """ get_data_top ??? """
  line = string.strip(line)
  if line == '' or line[0] == '#':
    return -1, ''
  arr = string.splitfields(line, '|')
  if len(arr) > 1:
    ret = ''
    my_alias = string.strip(arr[0])
    link = string.strip(arr[1])
    info = string.strip(arr[2])
    if len(arr) > 3:
      title = string.replace(string.strip(arr[3]), '"', '&quot;')
    else:
      title = ''
    if len(arr) > 4 :
      prefix = string.replace(arr[4], '&quot;', '"') + '&nbsp;'
    else:
      prefix = ''
    if len(arr) > 5:
      target = ' target="_extern"'
    else:
      target = ''
    if nav_main != '' and nav_main == my_alias:
      link = u'<span class="navTopBoxSelected"><span class="navTopLinkSelected">' + \
             '&nbsp;&nbsp;%s&nbsp;&nbsp;</span></span>' % info
      ret += prefix + link
    else:
      c = 'navTopLink'
      start_of_link = ''
      end_of_link = ''
      ret += u'<a class="%s" href="%s" title="%s"%s>' % (c, link, title, target)
      ret += prefix + start_of_link + info + end_of_link + '</a>'
  #assert False
  return my_alias, ret

# -----------------------------------------------------
def get_top_navigation_menu_top(lines, profi_mode):
  """ liefert das oberste Menu """
  ret = ''
  for line in lines:
    my_alias, res = get_data_top(line, 'start', profi_mode)
    if my_alias > -1:
      if ret != '':
        ret += ' <span class="navTop">|</span> '
      ret += res
  return ret

# -----------------------------------------------------
def get_top_navigation_menu(lines, nav_main, profi_mode):
  """ liefert das obere Hauptmenu """
  ret = ''
  for line in lines:
    my_alias, res = get_data_top(line, nav_main, profi_mode)
    if my_alias > -1:
      if ret != '':
        ret += ' <span class="navTop">|</span> '
      ret += res
  return ret

# -----------------------------------------------------
def get_navigation_menu(lines, *args):
  """ liefert das linke Menu """
  n_args = 0
  menu = []
  for n in xrange(4):
    try:
      menu.append(args[n])
      n_args += 1
    except:
      menu.append('')
  ret = u''
  select = 0
  for line in lines:
    my_depth, my_alias, res = get_data_left(line)
    if res != '' and string.find(res, '<div') < 0:
      res_start = '<div class="menu_border_bottom">'
      res_end = '</div>\n'
    else:
      res_start = ''
      res_end = ''
    if my_depth == 0:
      if select == 2:
        ret += '</div>\n</div>\n</div>\n'
        select = 3
      elif select == 0 and my_alias == menu[0]:
        select = 1
        ret += '<div class="menu_area">\n<div style="padding-left:2px;">'
    if my_depth == -999:
      ret += res
    elif my_depth == -1:
      if res != '':
        if select == 2:
          ret += '</div>\n</div>\n</div>\n'
          select = 3
      ret += res_start + res + res_end
    elif (select in [1, 2, 3] ) and my_alias == menu[n_args-1]:
      ret += '\n<div class="tabHeaderBg">\n' + res_start + res + '&raquo;' + res_end + '</div>\n'
    elif my_depth == 0 or select == 2:
      ret += res_start + res + res_end
    if select == 1:
      ret += '<div style="margin-left:15px;">\n'
      select = 2
  if select == 2:
    ret += '</div>\n</div>\n</div>\n'
  return ret

# -----------------------------------------------------
def get_menu_data(id=1):
  """ liefert die Menudaten """
  menu = get_menuitems_by_id_navmenu_left(id)[0]
  return menu.navigation

# -----------------------------------------------------
def save_menus_left(menu_id, text, is_main_menu=False):
  """ speichert die Menues in der Datenbank """

  def save_this_menu (menu_id, name, navigation, is_main_menu):
    item = get_new_navmenu_left()
    item.menu_id = menu_id
    item.name = name
    item.navigation = navigation
    item.is_main_menu = is_main_menu
    item.save()

  lines = string.splitfields(text, '\n')

  delete_menuitem_navmenu_left(menu_id)
  menu = get_top_navigation_menu_left(lines)
  save_this_menu(menu_id, '|', menu, is_main_menu)

  nav_main = ''
  nav_sub = ''
  nav_sub_sub = ''
  for line in lines:
    line = string.strip(line)
    if line != '' and line[0] != '#':
      arr = string.splitfields(line, '|')
      if len(arr) > 1:
        my_depth = int(string.strip(arr[0]))
        my_alias = string.strip(arr[1])
        if my_depth == 0:
          nav_main = my_alias
          nav_sub = ''
          nav_sub_sub = ''
        elif my_depth == 1:
          nav_sub = my_alias
          nav_sub_sub = ''
        else:
          nav_sub_sub = my_alias
        info = string.strip(arr[3])
        if nav_sub == '':
          menu = get_navigation_menu(lines, nav_main)
        elif nav_sub_sub == '':
          menu = get_navigation_menu(lines, nav_main, nav_sub)
        else:
          menu = get_navigation_menu(lines, nav_main, nav_sub, nav_sub_sub)
        save_this_menu(menu_id, nav_main + '|' + nav_sub, menu, is_main_menu)

# -----------------------------------------------------
def save_menus_top(menu_id, text, profi_mode=False):
  """ speichert das obere Hauptmenu """

  def save_this_menu (menu_id, name, navigation):
    item = get_new_navmenu_top()
    item.menu_id = menu_id
    item.name = name
    item.navigation = navigation
    item.save()

  #if not profi_mode:
  #  text = decode_html(text)
  lines = string.splitfields(text, '\n')

  delete_menuitem_navmenu_top(menu_id)
  menu = get_top_navigation_menu_top(lines, profi_mode)
  save_this_menu(menu_id, '|', menu)

  nav_main = ''
  for line in lines:
    line = string.strip(line)
    if line != '' and line[0] != '#':
      arr = string.splitfields(line, '|')
      if len(arr) > 1:
        my_alias = string.strip(arr[0])
        nav_main = my_alias
        info = string.strip(arr[3])
        menu = get_top_navigation_menu(lines, nav_main, profi_mode)
        save_this_menu(menu_id, nav_main, menu)

# -----------------------------------------------------
def save_menu_left_new(menu_id, name, description, navigation, is_main_menu=False):
  """ legt neues Menue in der Datenbank an """
  item = get_new_navmenu_left()
  item.menu_id = menu_id
  item.name = name
  item.description = description
  item.navigation = navigation
  item.is_main_menu = is_main_menu
  item.save()
