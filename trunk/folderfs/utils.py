# -*- coding: utf-8 -*-
"""
/dms/folderfs/utils.py

.. enthaelt Hilfefunktionen fuer FS-Ordner
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.01.2007  Beginn der Arbeit
0.02  14.04.2008  calculate_quota
"""

import os

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_path
from dms.queries        import get_home_path
from dms.queries        import set_quota

from dms.file.utils     import get_folder_name

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_dont():
  return { 'sort_mode': 0, 'navigation_mode': 0, 'add_mode': 0,
           'import_mode': 0, 'export_mode': 0, 'browseable_mode': 0, 'comment_mode': 0,
           'user_mode': 0, 'sort_mode': 0, 'search_mode': 0, 'empty_mode': 0
         }

# -----------------------------------------------------
def get_user_support(item_container):
  """ moeglicher User-Support """
  #if not item_container.item.has_user_support:
  #  return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/folderfs/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def calculate_quota(user, do_save=True):
  """ berechnet die aktuelle Quota-Auslastung """
  item_container = get_item_container_by_path(get_home_path(user))
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  total = 0
  for root, dirs, files in os.walk(base_path):
    total += sum(os.path.getsize(os.path.join(root, name)) for name in files)
  if do_save:
    set_quota(user.username, total)
  return total
