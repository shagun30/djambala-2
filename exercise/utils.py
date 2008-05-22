# -*- coding: utf-8 -*-
"""
/dms/exercise/utils.py

.. enthaelt Hilfefunktionen fuer Aufgaben
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.05.2008  Beginn der Arbeit
0.02  09.05.2008  Notenspiegel
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

# -----------------------------------------------------
def get_user_support(item_container, user):
  """ """
  if item_container.item.app.name == 'dmsEduExerciseItem':
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/exercise/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render ( cSection)
  return content

# -----------------------------------------------------
def get_points(item_container):
  """ liefert den Notenspiegel """
  if item_container.item.app.name=='dmsExercise':
    if item_container.item.integer_1 <= 0:
      return ''
    else:
      arr = string.splitfields(item_container.item.string_1.strip(), '\n')
      max = item_container.item.integer_1
  if item_container.item.app.name=='dmsEduExerciseItem':
    if item_container.item.integer_6 <= 0:
      return ''
    else:
      arr = string.splitfields(item_container.item.string_2.strip(), '\n')
      max = item_container.item.integer_6
  if len(arr) < 5:
    return ''
  error = False
  p = []
  for n in xrange(5):
    values = string.splitfields(arr[n].strip(), ':')
    if len(values) < 2:
      error = True
    else:
      if values[0].strip() != str(n):
        error = True
      if int(values[1].strip()) > max:
        error = True
      else:
        if n == 0:
          p.append({'max': max, 'min': int(values[1].strip())})
        else:
          p.append({'max': max-1, 'min': int(values[1].strip())})
        max = int(values[1].strip())
  p.append({'max': max, 'min': 0})
  return p

# -----------------------------------------------------
def get_points_min_max(points):
  """ """
  points_header = []
  for point in points:
    if point['max'] == point['min']:
      points_header.append('%i' % point['max'])
    else:
      points_header.append('%i-%i' % (point['max'], point['min']))
  return points_header