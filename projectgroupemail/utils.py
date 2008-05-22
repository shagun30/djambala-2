# -*- coding: utf-8 -*-
"""
/dms/projectgroupemail/utils.py

.. enthaelt Hilfefunktionen fuer Rundschreiben
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.01.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_path_and_name
from dms.queries        import get_item_container_by_path
from dms.queries        import count_users_with_email

from dms.utils_base     import html2txt
from dms.utils_base     import ACL_USERS

import re

# -----------------------------------------------------
def get_dont():
  #return { 'sort_mode': 0, 'navigation_mode': 0}
  return { 'navigation_mode': 0}

# -----------------------------------------------------
def get_user_support(item_container, manage_site_mode=False):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/projectgroupemail/user_support.html')
  if manage_site_mode:
    cSection = Context ({ 'path': get_site_url(item_container, ''), 'manage_site_mode': True, })
  else:
    cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render(cSection)
  return content

