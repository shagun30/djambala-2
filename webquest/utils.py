# -*- coding: utf-8 -*-
"""
/dms/webquestitem/utils.py

.. enthaelt Hilfefunktionen fuer Webquests
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
"""

import string

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_menuitems_navmenu_left
from dms.utils_base     import instance_dict

from dms.utils_navigation   import get_navigation_menu

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_view_mode(item_container, view_mode):
  """ duerfen Ergaenzungen vorgenommen werden """
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/eduwebquestitem/view_mode.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''),
                        'view_mode': view_mode,
                      })
  return tSection.render ( cSection)

# -----------------------------------------------------
def get_user_support(item_container, authenticated):
  """ duerfen Ergaenzungen vorgenommen werden """
  from django.template.loader import get_template
  from django.template import Context
  content = ''
  if item_container.item.has_user_support and authenticated:
    tSection = get_template('app/webquest/user_support.html')
    cSection = Context ({ 'path': get_site_url(item_container, ''), })
    content += tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_menu_left_webquest(item_containers, item_container, sub_menu=None):
  """ .. liefert das Webquest-Menu """
  start_name = 'webquest_start'
  content = """
0 | %s | %s?view_mode=webquest | Webquest | Startseite | %s
999
""" % (start_name, item_container.get_absolute_url(), 
      '<b><i><span class="red">::</span></i></b>')
  for i in item_containers:
    if i.item.app.name in ['dmsDocument', 'dmsPool']:
      content += '1 | %s | %s | %s\n' % \
                (i.item.name, i.get_absolute_url(), i.item.title)
  content = get_navigation_menu(string.splitfields(content, '\n'),
                                start_name, sub_menu)
  return content

# -----------------------------------------------------
def get_navigation_left(item_container, sub_menu):
  """ liefert den linken Navigationsbereich """
  i = item_container.container.menu_left_id
  items = get_menuitems_navmenu_left(i, sub_menu)
  if len(items) > 0:
    return items[0].navigation
  else:
    return '<p>%s<br />%i, %s</p>' % (_(u'Navigation fehlt!'), i, sub_menu)

# -----------------------------------------------------
def check_webquest(item_container, vars):
  """ """
  parent = item_container.get_parent()
  if parent.item.app.name == 'dmsWebques':
    vars['navigation_left'] = get_navigation_left(parent, 
                              'webquest|'+item_container.item.name)
    vars['view_options'] = get_view_mode(parent, '')
    vars['no_top_main_navigation'] = True
    site = instance_dict(vars['site'])
    site['title'] = _(u'Webquest')
    site['sub_title'] = parent.item.title
    vars['site'] = site
  return vars