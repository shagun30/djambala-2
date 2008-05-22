# -*- coding: utf-8 -*-
"""
/dms/newsletter/utils.py

.. enthaelt Hilfefunktionen fuer Newsletter
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.11.2007  Beginn der Arbeit
0.02  22.01.2008  count_users
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_path_and_name
from dms.queries        import get_item_container_by_path
from dms.queries        import count_users_with_email

from dms.utils_base     import html2txt
from dms.utils_base     import ACL_USERS

from dms.userfolder.utils     import get_all_users_with_email

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
  tSection = get_template('app/newsletter/user_support.html')
  if manage_site_mode:
    cSection = Context ({ 'path': get_site_url(item_container, ''), 'manage_site_mode': True, })
  else:
    cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render(cSection)
  return content

# -----------------------------------------------------
def remove_html( html):
  """ Einfache Umwandlung von HTML in plain text (Fuer E-Mail) """
  return html2txt(html)

# -----------------------------------------------------
def check_userfolder(item_container):
  """ gibt es zu diesem Pfad einen Userfolder """
  return get_item_container_by_path_and_name(item_container.container.path + ACL_USERS + '/', '')

# -----------------------------------------------------
def get_recipients(item_container):
  """ liefert entsprechenden User zurueck """
  if item_container.item.string_1 != '':
    user_folder = get_item_container_by_path(item_container.item.string_1)
    return get_all_users_with_email(user_folder)
  else:
    while not check_userfolder(item_container):
      item_container = item_container.get_parent()
    return get_all_users_with_email(item_container)

# -----------------------------------------------------
def count_recipients(item_container):
  """ liefert die Anzahl der Empfaenger """
  if item_container.item.string_1 != '':
    user_folder = get_item_container_by_path(item_container.item.string_1)
    return count_users_with_email(user_folder)
  else:
    while not check_userfolder(item_container):
      item_container = item_container.get_parent()
    return count_users_with_email(item_container)

