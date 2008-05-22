#-*-coding: utf-8 -*-
"""
/dms/utils_form.py

.. enthaelt Hilfefunktionen zum Aufbau von Formularen
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.05.2007  Beginn der Arbeit
0.02  20.05.2007  Ein- und Ausloggen in Top-Navigation
0.03  26.09.2007  get_item_vars_show fuer Webquests angepasst
0.04  10.11.2007  is_protected
0.05  28.11.2007  Rueckkehradresse beim Ausloggen url_path
0.06  07.03.2008  Integration von check_slot
0.07  28.03.2008  in_edit_mode
0.08  16.04.2008  get_home_url
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_base_site_url

from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_id
from dms.queries        import get_menuitems_navmenu_left
from dms.queries        import get_home_url

from dms.roles          import UserEditPerms
from dms.utils          import get_footer_email
from dms.utils          import get_folderish_actions
from dms.utils          import get_item_add_actions
from dms.utils          import get_item_actions
from dms.utils          import get_breadcrumb
from dms.utils          import get_navigation_top
from dms.utils          import get_navigation_left
from dms.utils          import get_prev_next_line
from dms.utils_base     import instance_dict
from dms.utils_base     import check_slot

from dms.text_icons     import EXTERN_ICON
from dms.views_comment  import item_comment

# -----------------------------------------------------
def check_visual_effects(request, item_container, vars, ignore_own_breadcrumb):
  """ veraendert z.B. bei Webquest den Aufbau der Seite """

  def get_navigation_left_webquest(item_container, sub_menu,
                                   ignore_own_breadcrumb=False):
    """ liefert den linken Navigationsbereich """
    i = item_container.container.menu_left_id
    items = get_menuitems_navmenu_left(i, sub_menu)
    if len(items) > 0:
      return items[0].navigation
    else:
      return '<p>%s<br />%i, %s</p>' % (_('Navigation fehlt:'), i, sub_menu)

  part_of_id = item_container.part_of_id
  if part_of_id <= 0:
    return vars
  id = item_container.id
  master_container = get_item_container_by_id(part_of_id, True)
  if master_container != None and master_container.item.app.name == 'dmsEduWebquestItem':
    if not ignore_own_breadcrumb:
      sub_menu = 'webquest|'
      if item_container.item.app.name in ['dmsDocument', 'dmsPool']:
        sub_menu += item_container.item.name
      elif item_container.item.app.name != 'dmsEduWebquestItem':
        parent = item_container.get_parent()
        sub_menu += parent.item.name
      vars['navigation_left'] = get_navigation_left_webquest(master_container,
                                sub_menu)
      vars['no_top_main_navigation'] = True
      site = instance_dict(vars['site'])
      site['title'] = _('Webquest')
      site['sub_title'] = master_container.item.title
      vars['site'] = site
    else:
      if item_container.item.app.is_folderish:
        parent = item_container
      else:
        parent = item_container.get_parent()
      vars['navigation_left'] = get_navigation_left(parent)
      vars['breadcrumb'] = get_breadcrumb(parent, 
                               ignore_own_breadcrumb=ignore_own_breadcrumb)
  return vars

# -----------------------------------------------------
def get_base_vars(request, item_container, content_div_style, 
                  intro_mode=True, ignore_own_breadcrumb=False, in_edit_mode=False, last_modified=None):
  """ Grundbelegung der Variablen fuer Template """
  user_perms = UserEditPerms(request.user.username, request.path)
  comments = ''
  if request.META.has_key('HTTP_USER_AGENT'):
    user_agent = request.META['HTTP_USER_AGENT']
  else:
    user_agent = ''
  if item_container.item.app.is_folderish:
    url_path = get_site_url(item_container, 'index.html')
  else:
    url_path = get_site_url(item_container.get_parent(), 'index.html')
  if last_modified == None:
    last_modified = item_container.get_last_modified()
  else:
    last_modified = last_modified.strftime('%d.%m.%Y %H:%M')
  if request.user.is_authenticated():
    home_url = get_home_url(request.user)
  else:
    home_url = ''
  vars = { #'is_msie_6'        : is_msie_6,
           'site'             : item_container.container.site,
           'in_edit_mode'     : in_edit_mode,
           'my_name'          : item_container.item.name,
           'header_title'     : item_container.item.title,
           'title'            : item_container.item.title + comments,
           'sub_title'        : item_container.item.sub_title,
           'navigation_top'   : get_navigation_top(item_container),
           'navigation_left'  : get_navigation_left(item_container),
           'slot_right_info'  : '', #item_container.item.info_slot_right,
           'breadcrumb'       : get_breadcrumb(item_container),
           'path'             : item_container.container.path,
           'url_path'         : url_path,
           'base_site_url'    : get_base_site_url(),
           'footer_email'     : get_footer_email(item_container.item),
           'last_modified'    : last_modified,
           'authenticated'    : request.user.is_authenticated(),
           'user_perms'       : user_perms,
           'user_name'        : request.user,
           'url_more'         : item_container.item.url_more,
           'url_more_extern'  : item_container.item.url_more_extern,
           'show_errors'      : request.method == 'POST',
           'ajax_url'         : url_path + '/ajax/',
           'home_url'         : home_url
          }
  if content_div_style != 'frame-main':
    vars['content_div_style'] = content_div_style
  vars = check_visual_effects(request, item_container, vars, ignore_own_breadcrumb)
  if intro_mode:
    v  = { 'text'             : check_slot(request, item_container, item_container.item.text),
           'text_more'        : check_slot(request, item_container, item_container.item.text_more),
           'image_url'        : item_container.item.image_url,
           'image_url_url'    : item_container.item.image_url_url,
           'image_extern'     : item_container.item.image_extern,
           'is_wide'          : item_container.item.is_wide,
           'is_important'     : item_container.item.is_important,
           }
    vars.update(v)
  return vars, user_perms

# -----------------------------------------------------
def get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors, commands={}):
  """ liefert die Grundwerte zum Aufbau von Ordner-Add-Formularen """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage',
                                   False, in_edit_mode=True)
  vars['action'] = get_folderish_actions(request, user_perms, item_container, app_name,
                                                  False, commands)
  vars['content'] = content
  vars['title'] = my_title
  vars['next'] = get_site_url(item_container, 'index.html/add/' + app_name + '/')
  vars['path'] = item_container.container.path+'index.html/add/' + app_name + '/'
  vars['submit'] = my_title
  vars['show_errors'] = show_errors
  vars['no_top_main_navigation'] = True
  return vars

# -----------------------------------------------------
def get_folderish_vars_edit(request, item_container, app_name, my_title, 
                            content, f, dont={}, ignore_own_breadcrumb=True):
  """ liefert die Grundwerte zum Aufbau von Ordner-Edit-Formularen """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage', False,
                                   ignore_own_breadcrumb=ignore_own_breadcrumb, in_edit_mode=True)
  vars['action'] = get_folderish_actions(request, user_perms, item_container, app_name,
                                         False, dont)
  vars['content'] = content
  vars['title'] = my_title
  vars['submit'] = my_title
  if f != None:
    vars['errors'] = f.errors
  vars['no_top_main_navigation'] = True
  return vars

# -----------------------------------------------------
def get_folderish_vars_show(request, item_container, app_name, content,
                            user_support='', last_modified=None):
  """ liefert die Grundwerte zum Aufbau von Ordner-Anzeigeseiten """
  if request.GET.has_key('show_more') :
    show_more = request.GET['show_more']
  else :
    show_more = False
  vars, user_perms = get_base_vars(request, item_container, 'frame-main', last_modified=last_modified)
  if item_container.item.info_slot_right != '':
    vars['slot_right_info'] = check_slot(request, item_container, item_container.item.info_slot_right) + \
                             '<br />\n<br />\n'
  vars['user_support'] = user_support
  vars['action'] = get_folderish_actions(request, user_perms, item_container, app_name,
                                         item_container.item.has_comments)
  vars['show_more'] = show_more
  vars['content'] = content
  vars['item'] = item_container.item
  vars['is_protected'] = item_container.container.is_protected()
  return vars

# -----------------------------------------------------
def get_item_vars_add(request, item_container, app_name, my_title, content,
                      show_errors, commands={}):
  """ liefert die Grundwerte zum Aufbau von Daten-Add-Formularen """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage',
                                   False, in_edit_mode=True)
  vars['action'] = get_item_add_actions(request, user_perms, item_container,
                                        commands=commands)
  vars['content'] = content
  vars['title'] = my_title
  vars['next'] = get_site_url(item_container, 'index.html/add/' + app_name + '/')
  vars['path'] = item_container.container.path+'index.html/add/' + app_name + '/'
  vars['submit'] = my_title
  vars['show_errors'] = show_errors
  vars['no_top_main_navigation'] = True
  return vars

# -----------------------------------------------------
def get_item_vars_edit(request, item_container, app_name, my_title, content, f, commands={}):
  """ liefert die Grundwerte zum Aufbau von Daten-edit-Formularen """
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage', 
                                   False, in_edit_mode=True)
  if commands == {}:
    commands = get_item_commands(item_container)
  vars['action'] = get_item_actions(request, user_perms, item_container, app_name,
                                    item_container.item.has_comments,
                                    commands=commands)
  vars['content'] = content
  vars['title'] = my_title
  vars['submit'] = my_title
  if f != None:
    vars['errors'] = f.errors
  vars['no_top_main_navigation'] = True
  return vars

# -----------------------------------------------------
def get_item_vars_show(request, item_container, app_name, commands={},
                       ignore_own_breadcrumb=False):
  """ liefert die Grundwerte zum Aufbau von Daten-Anzeigeseiten """
  if commands == {}:
    commands = { 'edit_mode': 1, }
  if item_container.container.show_next:
    prev_next = get_prev_next_line(item_container)
  else:
    prev_next = ''
  if item_container.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  if item_container.item.license.id <= 1:
    license = ''
  else:
    s = u'<a href="%s" target="_license" alt="Lizenzbild"><img src="%s"></a><br />'
    license = s % \
              (item_container.item.license.url, item_container.item.license.image_url)
    license += _('Lizenz dieses Objektes: ') + \
              EXTERN_ICON + u'<a href="%s" target="_license">%s</a>' % \
              (item_container.item.license.url, item_container.item.license.name)

  vars, user_perms = get_base_vars(request, item_container, 'frame-main',
                                   ignore_own_breadcrumb=ignore_own_breadcrumb)
  if item_container.item.app.is_folderish:
    vars['action'] = get_folderish_actions(request, user_perms, item_container, 
                                           app_name, False, commands)
  else:
    vars['action'] = get_item_actions(request, user_perms, item_container, 
                                      app_name, item_container.item.has_comments,
                                      commands=commands)
  vars['show_next'] = prev_next
  vars['comments'] = comments
  vars['license'] = license
  vars['item'] = item_container.item
  if item_container.get_parent().container.is_protected():
    vars['is_protected'] = True
  return vars

# -----------------------------------------------------
def get_item_commands(item_container):
  """ liefert die Standardbefehle fuer Datenobjekte """
  #commands = {'show_mode': 1,'export_mode': 1}
  commands = {'show_mode': 1}
  if item_container.is_data_object:
    commands.update( {'rss_mode': 1, 'image_mode': 1,} )

  return commands
