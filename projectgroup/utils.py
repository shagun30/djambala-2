# -*- coding: utf-8 -*-
"""
/dms/projectgroup/utils.py

.. enthaelt Hilfefunktionen fuer geschlossene Arbeitsgruppen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.06.2007  Beginn der Arbeit
"""

import string

from django.utils.translation import ugettext as _

from dms.utils          import check_name

from dms.queries        import get_site_url
from dms.queries        import get_all_roles

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_role_choices(my_role):
  """ wandelt Textzeilen in Liste um """
  roles = get_all_roles(my_role)
  for r in roles :
    yield ( r.id, u'%s (%s)' % (r.description, r.name) )

# ----------------------------------------------------------------
def get_user_support(item_container):
  """ """
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/projectgroup/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_menu_left_from_sections(item_container, name, sections, folders):
    url = item_container.get_absolute_url()
    if name != '':
      url = url.replace('index.html', '') + name + '/index.html'
    s_name = 'Start'
    s_info = 'Startseite'
    text = u'0 | %s | %s | %s | %s | <b><i><span class="red">::</span></i></b>\n999\n' % \
           (s_name.lower(), url, s_name, s_info)
    objs = string.splitfields(sections, '\n')
    #assert False
    for obj in objs:
      s_name = obj.strip()
      if s_name in folders:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s%s/index.html | %s\n' % \
                ( s_obj, url.replace('index.html', ''), s_name, s_name)
      elif s_name.lower() in folders:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s%s/index.html | %s\n' % \
                ( s_obj, url.replace('index.html', ''), s_name.lower(), s_name)
      else:
        s_obj = check_name(s_name.lower(), True)
        text += u'1 | %s | %s?section=%s | %s\n' % ( s_obj, url, s_name, s_name)
    return text