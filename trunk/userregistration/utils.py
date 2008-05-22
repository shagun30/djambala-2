# -*- coding: utf-8 -*-
"""
/dms/userregistration/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.06.2007  Beginn der Arbeit
0.02  27.06.2007  get_org_groups
"""

import string

from django.utils.translation import ugettext as _

from dms.queries        import get_base_site_url
from dms.queries        import get_site_url
from dms.queries        import get_org_by_town
from dms.queries        import get_org_by_name
from dms.queries        import get_org_by_number
from dms.queries        import get_org_by_town_no_school
from dms.queries        import get_org_by_name_no_school
from dms.queries        import get_user_by_username
from dms.queries        import get_org_groups
from dms.queries        import get_org_by_group

from dms.utils          import check_name

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_username(org_id_prefix, first_name, last_name):
  """ generiert aus Vor- und Nachnamen eine eindeutige Mitglied-ID """
  first_name = check_name(first_name.strip().lower(), True)
  last_name = check_name(last_name.strip().lower(), True)
  n_len = len(first_name)
  for n in xrange(n_len):
    test_name  = u'%s%s.%s' % (org_id_prefix, first_name[0:n+1], last_name)
    if get_user_by_username(test_name) == None:
      return test_name
  curr = 0
  while curr < 100:  # Notbremse!
    curr += 1
    test_name  = u'%s%s.%s_%i' % (org_id_prefix, first_name, last_name, curr)
    if get_user_by_username(test_name) == None:
      return test_name

# -----------------------------------------------------
def get_sex_choices(id=1):
  """ """
  ret = []
  ret.append( ('w', 'Frau') )
  ret.append( ('m', 'Herr') )
  return ret

# -----------------------------------------------------
def get_school_section():
  """ erzeugt die Formulare zur Schule """
  from django.template.loader import get_template
  from django.template import Context
  tSchool = get_template('app/userregistration/school_form.html')
  cSection = Context ( { 'section': _(u'Fall 1: Angehörige(r) einer Schule'),} )
  return tSchool.render(cSection)

# -----------------------------------------------------
def get_edu_institutions_section():
  """ erzeugt die Uebersicht der vorhandenen paed. Einrichtungen """
  from django.template.loader import get_template
  from django.template import Context
  tEduInst = get_template('app/userregistration/edu_inst_form.html')
  insts = get_org_groups()
  cSection = Context ( { 'section': _(u'Fall 2: Angehörige(r) einer speziellen Landesinstitution'),
                         'edu_insts': insts } )
  return tEduInst.render(cSection)

# -----------------------------------------------------
def get_institutions_section():
  """ erzeugt die Uebersicht der vorhandenen Einrichtungen """
  from django.template.loader import get_template
  from django.template import Context
  tInst = get_template('app/userregistration/inst_form.html')
  cSection = Context ( { 'section': _(u'Fall 3: Angehörige(r) anderen Institution') } )
  return tInst.render(cSection)

# -----------------------------------------------------
def get_items(get_data, post_data):
  if get_data.has_key('inst_contains'):
    items = get_org_by_group(get_data['inst_contains'])
    title = _(u'Ausgewählte Einrichtung(en)')
  elif get_data.has_key('school_town'):
    items = get_org_by_town(post_data['town'], True)
    title = _(u'Ausgewählte Schulorte')
  elif get_data.has_key('school_name'):
    items = get_org_by_name(post_data['name'], True)
    title = _(u'Ausgewählte Schulnamen')
  elif get_data.has_key('school_number'):
    items = get_org_by_number(post_data['number'])
    title = _(u'Ausgewählte Schulnummer')
  elif get_data.has_key('inst_town'):
    items = get_org_by_town_no_school(post_data['town'])
    title = _(u'Ausgewählte Orte')
  elif get_data.has_key('inst_name'):
    items = get_org_by_name_no_school(post_data['name'])
    title = _(u'Ausgewählte Namen')
  else:
    items = []
    title = _(u'Unbekannte Suche')
  return items, title

# -----------------------------------------------------
def get_actions ( request, user_perms, site, rHasUserFolder=False ) :
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/userfolder/manage_options.html')
  nPos = string.rfind(request.path, '/manage/')
  if nPos > -1 :
    path = request.path[:nPos]
  else :
    path = request.path
  if string.find ( path, 'index.html' ) < 0 :
    path += 'index.html'
  show_mode = True
  edit_mode = False
  manage_mode = False
  user_mode = False
  navigation_mode = False
  sort_mode = False
  c=Context({'authenticated'  : request.user.is_authenticated(),
             'show_mode'      : show_mode,
             'edit_mode'      : edit_mode,
             'manage_mode'    : manage_mode,
             'navigation_mode': navigation_mode,
             'sort_mode'      : sort_mode,
             'has_user_folder': rHasUserFolder,
             'path'           : get_site_url(site,path),
             'user_perms'     : user_perms,
             'user_name'      : request.user,
             'base_site_url'  : get_base_site_url(),})
  return t.render ( c)

