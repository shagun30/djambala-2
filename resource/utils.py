# -*- coding: utf-8 -*-
"""
/dms/resource/utils.py

.. enthaelt Hilfefunktionen fuer Ressourcenverwaltungen
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.01.2008  Beginn der Arbeit
....  ....
0.05  09.04.2008  time_overlap, get_free_resource_list
"""

from django.template import Context

from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries              import get_site_url
from dms.utils_form           import get_folderish_vars_show

from dms.resource.queries     import get_type_list
from dms.resource.queries     import get_resource_list
from dms.resource.queries     import get_org_settings
from dms.resource.queries     import get_event_list

import string
import mx.DateTime

# -----------------------------------------------------
def get_dont():
  #return { 'sort_mode': 0, 'navigation_mode': 0}
  return { 'navigation_mode': 0}

# -----------------------------------------------------
def get_user_support(item_container):
  """ """
  if not item_container.item.has_user_support:
    return ''
  tSection = get_template('app/faqboard/user_support.html')
  cSection = Context ({ 'path': get_site_url(item_container, ''), })
  content = tSection.render(cSection)
  return content


# -----------------------------------------------------
def get_default_settings( org_id):
  if org_id>0:
    return _(u"""00:00|Früh
05:55|0. Stunde
07:45|1. Stunde
08:35|2. Stunde
09:20|1. gr. Pause
09:35|3. Stunde
10:25|4. Stunde
11:10|2. gr. Pause
11:30|5. Stunde
12:20|6. Stunde
13:05|Mittagspause
13:40|7. Stunde
14:30|8. Stunde
15:25|9. Stunde
16:15|10. Stunde
17:00|17:00
17:30|17:30
18:00|18:00
18:30|18:30
19:00|19:00
19:30|19:30
20:00|20:00
20:30|20:30
21:00|21:00
21:30|21:30
22:00|22:00
22:30|22:30
23:00|Nachts""")
  else:
    return _(u"""00:00|Früh
06:00|06:00
07:00|07:00
08:00|08:00
09:00|09:00
10:00|10:00
11:00|11:00
12:00|12:00
13:00|13:00
14:00|14:00
15:00|15:00
16:00|16:00
17:00|17:00
18:00|18:00
19:00|19:00
20:00|20:00
21:00|Spät""")

# -----------------------------------------------------
def add_periods_endtime( l):
  """ Fuegt Endzeitpunkte der Zeitspannen ein """
  l.reverse()
  old = u"24:00"
  #for i in l[:]:
  for i in l:
    i.append(old)
    old = i[0]
  l.reverse()
  return l

# -----------------------------------------------------
def get_periods_list( org_id, text):
  """ Erzeugt aus der Texteingabe der Zeitspannen eine Liste mit Endzeitpunkt
      Listenelement: [Startzeitpunkt, Benennung, Endzeitpunkt]
  """
  if text=="":
    text = get_default_settings( org_id)
  lines = string.splitfields(text,'\n')
  per_list0 = []
  for line in lines:
    array = string.splitfields(line,'|')
    if (len(array)==2):
      per_list0 += [[array[0].strip(), array[1].strip()]]
  ret = add_periods_endtime( per_list0)
  return ret

# -----------------------------------------------------
def show_org_settings(org_id):
  """ """
  sets = get_org_settings(org_id)
  ret=u""
  if len(sets)>0:
    for s in sets:
      ret += u'%s|%s\n' % (s.time_start.strftime('%H:%M'),s.name)
  return ret

# -----------------------------------------------------
def get_periods_by_id(org_id, id_list ):
  """ """
  objs = get_org_settings(org_id)
  ret=[]
  for ob in objs:
    for i in id_list:
      if ob.id == int(i):
        ret += [(ob.time_start.strftime('%H:%M'), ob.time_end.strftime('%H:%M'), ob.is_period)]
  return [ret[0], ret[len(ret)-1]] # keinste, groesste
  

# -----------------------------------------------------
def get_type_res_list(org_id, all=True):
  """
  Liste der in org_id verfuegbaren Typen (Kategorien) und Ressourcen
  [ [typ, [res1, res2, ...], nres] ... ]
  Wenn all!=True: nur die Typen, in denen Ressourcen definiert sind
  """
  ret = []
  for t in get_type_list(org_id):
    r_t = []
    for r in get_resource_list(t.id):
      r_t.append(r)
    if (all or (r_t!=[])):
      ret.append([t, r_t, len(r_t)])
  return ret

# -----------------------------------------------------
def get_form_tab_row(res_type_descr, res_list, is_required=1):
  """ baut eine Spalte von Checkboxen auf """
  t_form = get_template('app/resource/checkbox.html')
  options = []
  for res in res_list:
    options.append({'id'   : res.id,
                    'name' : res.description})
  if len(options)>0:
    """
    context = Context({'header'  : res_type_descr,
                      'options'  : options,
                      'required' : is_required,
                      'name'     : 'type_'+ str(res.res_type_id) } )
    """
    context = Context({'options'  : options,
                      'required' : is_required,
                      'name'     : 'type_'+ str(res.res_type_id) } )
  else:
    """
    context = Context({'header'    : res_type_descr,
                      'options'    : options,
                      'required'   : is_required,
                      'name'       : 'dummy',
                      'no_entries' : 1 } )
    """
    context = Context({'options'    : options,
                      'required'   : is_required,
                      'name'       : 'dummy',
                      'no_entries' : 1 } )
    
  return t_form.render(context)

# -----------------------------------------------------
def time_overlap(tf1, tt1, tf2, tt2):
  """
  Eingaben als Strings, z.B. '1.1.2004 15:13'
  Logik von '<' bzw. '<=' ?
  """
  if mx.DateTime.Parser.DateTimeFromString(tf1)<mx.DateTime.Parser.DateTimeFromString(tf2):
    #x1 = tf1
    x2 = tt1
    y1 = tf2
    #y2 = tt2
  else: 
    #x1 = tf2
    x2 = tt2
    y1 = tf1
    #y2 = tt1
  if mx.DateTime.Parser.DateTimeFromString(y1)<=mx.DateTime.Parser.DateTimeFromString(x2):
    return 1
  else:
    return 0

# -----------------------------------------------------
def get_free_resource_list(type_id, dt_from, dt_to):
  """ Die im Zeitraum nicht belegten und belegten Ressourcen dieser Kategorie """
  ret_free = []
  ret_used = []
  for r in get_resource_list(type_id):
    is_used = 0
    for e in get_event_list(r.id):
      if time_overlap(e.datetime_start.strftime("%d.%m.%Y %H:%M"), e.datetime_end.strftime("%d.%m.%Y %H:%M"), dt_from, dt_to):
        is_used = 1
        break
    if is_used:
      ret_used += [r]
    else:
      ret_free += [r]
  return ret_free, ret_used

# -----------------------------------------------------
def resource_unused(res_id):
  """ !(Ist die Ressource (irgendwann) belegt?) """
  ret = True
  for e in get_event_list(res_id):
    ret = False
    break
  return ret

# -----------------------------------------------------
def get_app_name():
  """ liefert ressource """
  return 'resource'

# -----------------------------------------------------
def feedback_vars(request, item_container, app_name, info, arg_str=''):
  """
  erzeugt die vars fuer die Feedback-Seite
  arg_str ohne "?"
  """
  vars = get_folderish_vars_show(request, item_container, app_name, '', 
                                False)
  vars['next'] = item_container.get_absolute_url() + '?' + arg_str
  vars['feedback'] = info
  return vars
  
