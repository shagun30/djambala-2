# -*- coding: utf-8 -*-
"""
/dms/folder/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.03.2007  Beginn der Arbeit
"""

import string, datetime

from django.utils.translation import ugettext as _

from dms.settings       import HOME_PATH

from dms.models         import DmsItem
from dms.queries        import get_site_url
from dms.queries        import get_quota

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_folder_content(item, alpha_mode=False ):
  today = datetime.datetime.today()
  if alpha_mode:
    order = 'title'
  else:
    order = 'order_by'
  items = DmsItem.objects.select_related().extra \
              (
                where = [u"parent_item_id=%i \
                          AND is_browseable=1 \
                          AND is_deleted=0 \
                          AND visible_start<='%s'AND '%s'<=visible_end" 
                        % ( item.id, today, today ) ]
              ).order_by(order)
  # --- Welche Zwischentitel gibt es?
  d_sections = {}
  sections = []
  for s in string.splitfields(item.container.sections, '\n'):
    s = string.strip(s)
    if s != '' :
      sections.append(s)
      d_sections[s] = []
  # --- Umsortieren
  if len(sections) == 0 :
    return items, sections, d_sections
  d_sections['unknown'] = []
  curr_section = sections[0]
  for i in items :
    if d_sections.has_key(i.section) :
      d_sections[i.section].append(i)
    else :
      d_sections['unknown'].append(i)
  items = []
  for s in sections :
    items += d_sections[s]
  return items+d_sections['unknown'], sections, d_sections

def get_user_support(item_container, user):
  """ """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/pool/user_support.html')
  if item_container.container.path.find(HOME_PATH) == 0:
    quota = get_quota(user)
    quota_exceeded = quota.value >= quota.max
  else:
    quota_exceeded = False
  cSection = Context ({ 'path': get_site_url(item_container, ''), 
                        'quota_exceeded': quota_exceeded
                      })
  content = tSection.render ( cSection)
  return content
