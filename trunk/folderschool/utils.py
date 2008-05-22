# -*- coding: utf-8 -*-
"""
/dms/folderschool/utils.py

.. enthaelt Hilfefunktionen fuer Basisordner der Schulen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
0.02  19.05.2008  create_school
"""

import string

from django.utils.translation import ugettext as _

from dms.utils          import check_name

from dms.queries        import get_site_url
from dms.queries        import get_all_roles
from dms.queries        import save_container_values
from dms.queries        import save_item_values
from dms.queries        import get_role_by_user_path
from dms.queries        import get_min_max_menu_left
from dms.queries        import do_protect_folder
from dms.queries        import get_item_container_by_parent_item_id
from dms.queries        import get_user_by_username
from dms.queries        import get_org_by_number
from dms.queries        import get_role_by_name
from dms.queries        import get_site_by_org_id

from dms.resource.queries   import exist_settings_org_id
from dms.resource.queries   import create_org_settings
from dms.resource.queries   import exist_type_org_id
from dms.resource.queries   import create_org_type
from dms.resource.utils     import get_periods_list

from dms.utils_navigation import save_menus_left
from dms.utils_base       import ACL_USERS

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_role_choices(my_role):
  """ wandelt Textzeilen in Liste um """
  roles = get_all_roles(my_role)
  for r in roles :
    yield ( r.id, u'%s (%s)' % (r.description, r.name) )

# ----------------------------------------------------------------
def get_user_support(item_container):
  """ User-Support fuer Startseite """
  return ''

# -----------------------------------------------------
def get_menu_left_from_sections(item_container, name, sections, url=None):
    if url == None:
      url = item_container.get_absolute_url()
    if name != '':
      url = url.replace('index.html', '') + name + '/index.html'
    s_name = 'Start'
    s_info = 'Startseite'
    text = u'0 | %s | %s | %s | %s | <b><i><span class="red">::</span></i></b>\n999\n' % \
           (s_name.lower(), url, s_name, s_info)
    objs = string.splitfields(sections, '\n')
    for obj in objs:
      obj = obj.strip()
      if obj != '':
        arr = string.splitfields(obj, '|')
        m_name = arr[0].strip()
        if len(arr) == 1:
          arr.append(m_name.lower())
          f_name = check_name(arr[1].strip(), True)
        else:
          f_name = arr[1].strip()
        n_pos = f_name.find('/')
        if n_pos > 0:
          menu = f_name[:n_pos]
        else:
          menu = f_name
        s_name = obj.strip()
        text += u'1 | %s | %s%s/index.html | %s\n' % \
                ( menu, url.replace('index.html', ''), f_name, m_name)
    return text

# -----------------------------------------------------
#@transaction.commit_manually
def create_school(name, new, item_container):
  """ erzeugt Schule """
  # Zugangsnamen der Schulen!
  org_id = int(new['integer_1'])
  school = get_org_by_number(org_id)
  if len(school) < 1:
    return
  school = school[0]
  address = _(u"""<pre>
    %s
    %s
    %s %s
    Fon: %s 
    Fax: %s
    E-Mail: %s
</pre>
""") % (school.organisation, school.street, school.zip, school.town, school.phone, school.fax, school.email)

  new = {}
  username = 's_%i' % org_id
  user = get_user_by_username(username)
  school_name = new['title'] = school.organisation
  n_min, n_max = get_min_max_menu_left()
  menu_left_id = 1 + max(abs(n_min), n_max)
  new['text'] = _(u'<h4>Herzlich wilkommen!</h4>\n') + address
  sections = u"""Aktuelles|aktuell/news
Schulprofil
Schulgemeinde
Schulleben
Fächer
Klassen / Kurse | klassen
Internes
"""
  new['sections'] = sections
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['nav_title'] = _(u'Start')
  new['menu_left_id'] = menu_left_id
  new['nav_name_left'] = 'start|'
  new['integer_1'] = org_id
  new['string_2'] = '/aktuell/events/'
  new['is_exchangeable'] = False
  folderschool_item_container = save_container_values(user,
                                    'dmsFolderSchool', name, new, item_container)
  folderschool_item_container.container.site = get_site_by_org_id(org_id)
  folderschool_item_container.container.is_top_folder = True
  folderschool_item_container.container.save()
  folderschool_item_container.set_is_changeable(False)
  text = get_menu_left_from_sections(folderschool_item_container, '', sections)
  save_menus_left(menu_left_id, text)
  # --- Aktuelles
  new = {}
  new['name'] = name = _(u'aktuell')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = _(u'Aktuelles')
  new['nav_title'] = _(u'Aktuelles')
  new['nav_name_left'] = _(u'start|aktuell') #Aktuelles - aktuell !
  new['is_browseable'] = False
  akt_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  new = {}
  new['name'] = name = _(u'news')
  new['has_user_support'] = True
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Schwarzes Brett')
  new['nav_name_left'] = _(u'start|aktuell') #Aktuelles - aktuell !
  news_item_container = save_container_values(user,
                        'dmsNewsboard', name, new, akt_item_container)
  new = {}
  new['name'] = name = _(u'events')
  new['has_user_support'] = True
  new['is_moderated'] = True
  new['title'] = _(u'Terminkalender')
  new['nav_title'] = _(u'Terminkalender')
  new['nav_name_left'] = _(u'start|aktuell') #Aktuelles - aktuell !
  new['integer_4'] = 1 # nur Community-Mitglieder duerfen ergänzen
  news_item_container = save_container_values(user,
                        'dmsEventboard', name, new, akt_item_container)
  # --- Schulprofil
  new = {}
  new['name'] = name = _(u'schulprofil')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Schulprofil')
  new['sections'] = _(u'Schulprogramm\nBesondere Schwerpunkte/Angebote\n')
  new['nav_name_left'] = _(u'start|schulprofil')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  school_profile_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  school_profile_item_container.set_is_changeable(False)
  # --- Schulgemeinde
  new = {}
  new['name'] = name = _(u'schulgemeinde')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Schulgemeinde')
  new['sections'] = _(u'Gruppen\nSchulkonferenz\nOrgane\n')
  new['nav_name_left'] = _(u'start|schulgemeinde')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  school_community_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  school_community_item_container.set_is_changeable(False)
  # --- Schulleben
  new = {}
  new['name'] = name = _(u'schulleben')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Schulleben')
  new['sections'] = _(u'Feiern\nVeranstaltungen\nAusstellungen\n')
  new['nav_name_left'] = _(u'start|schulleben')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  school_life_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  school_life_item_container.set_is_changeable(False)
  new = {}
  new['name'] = name = _(u'treffpunkt')
  new['title'] = new['nav_title'] = _(u'Treffpunkt')
  new['sections'] = _(u'Austausch\n')
  new['nav_name_left'] = _(u'start|schulleben')
  comm_community_item_container = save_container_values(user,
                        'dmsFolder', name, new, school_life_item_container)
  new = {}
  new['name'] = name = _(u'pinnwand')
  new['title'] = new['nav_title'] = _(u'Pinnwand')
  new['section'] = _(u'Austausch')
  new['has_user_support'] = True
  new['is_moderated'] = True
  new['integer_4'] = 1 # nur Community-Mitglieder duerfen ergänzen
  new['nav_name_left'] = _(u'start|schulleben')
  pin_item_container = save_container_values(user,
                        'dmsPinboard', name, new, comm_community_item_container)
  # --- Faecher
  new = {}
  new['name'] = name = _(u'faecher')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Fächer')
  new['sections'] = _(u'Sprachlich-literarisch-künstlerisch\nGesellschaftswissenschaftlich\n') + \
                    _(u'Mathematisches\nSport\nWeitere Aufgabenfelder\n')
  new['nav_name_left'] = _(u'start|faecher')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  courses_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  courses_item_container.set_is_changeable(False)
  # --- Klassen
  new = {}
  new['name'] = name = _(u'klassen')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Klassen / Kurse')
  new['sections'] = _(u'1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n')
  new['nav_name_left'] = _(u'start|klassen')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  classes_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  classes_item_container.set_is_changeable(False)
  # --- Internes
  new = {}
  new['name'] = name = _(u'internes')
  new['has_user_support'] = False
  new['is_moderated'] = True
  new['title'] = new['nav_title'] = _(u'Internes')
  new['sections'] = _(u'Reservierung\nArbeitsgruppen\nVerwaltung\n')
  new['nav_name_left'] = _(u'start|internes')
  new['is_browseable'] = False
  new['integer_1'] = org_id
  internal_item_container = save_container_values(user,
                        'dmsFolder', name, new, folderschool_item_container)
  internal_item_container.set_is_changeable(False)
  new = {}
  new['name'] = name = _(u'reservierung')
  new['title'] = _(u'Reservierung von Räumen, Laptops etc.')
  new['nav_title'] = _(u'Reservierung')
  new['section'] = _(u'Reservierung')
  new['nav_name_left'] = _(u'start|internes')
  new['integer_1'] = org_id
  new['min_role_id'] = get_role_by_name('no_rights_micro').id
  if not exist_settings_org_id(org_id):
    if org_id > 0 : # Schulen ...
      per_list = get_periods_list(org_id, "")
      create_org_settings(org_id, per_list)
  if not exist_type_org_id(org_id):
    create_org_type(org_id)
  resource_item_container = save_container_values(user,
                        'dmsResource', name, new, internal_item_container)
  resource_item_container.set_is_changeable(False)
  # --- allgemeine Verwaltung
  new = {}
  new['name'] = name = _(u'lehrer')
  new['title'] = _(u'Verwaltungsoptionen für Lehrer/innen')
  new['nav_title'] = _(u'Lehrer/innen')
  new['section'] = _(u'Verwaltung')
  new['nav_name_left'] = _(u'start|internes')
  new['integer_1'] = org_id
  new['min_role_id'] = get_role_by_name('no_rights_mini').id
  teacher_item_container = save_container_values(user,
                        'dmsFolder', name, new, internal_item_container)
  new = {}
  new['name'] = name = _(u'lehrer.html')
  new['title'] = _(u'Verwaltungsoptionen für Lehrer/innen')
  save_item_values(user, 'dmsSchoolmanagement', name, new, teacher_item_container, True, False)
  new = {}
  new['title'] = _(u'User-Verwaltung')
  new['nav_title'] = new['title']
  new['is_browseable'] = False
  new['integer_1'] = org_id
  acl_item_container = save_container_values(user, 'dmsUserFolder', ACL_USERS, new, teacher_item_container)
  acl_item_container.set_is_changeable(False)
  # --- Optionen fuer Systembetreuer
  new = {}
  new['name'] = name = _(u'systembetreuer')
  new['title'] = new['nav_title'] = _(u'Verwaltungsoptionen für Systembetreuer')
  new['nav_title'] = _(u'Systembetreuer')
  new['section'] = _(u'Verwaltung')
  new['nav_name_left'] = _(u'start|internes')
  new['min_role_id'] = get_role_by_name('top_manager').id
  new['integer_1'] = org_id
  sysmaster_item_container = save_container_values(user,
                        'dmsFolder', name, new, internal_item_container)
  new = {}
  new['name'] = name = _(u'systembetreuer.html')
  new['title'] = _(u'Verwaltungsoptionen für Systembetreuer')
  save_item_values(user, 'dmsSchoolmanagement', name,
                    new, sysmaster_item_container, True, False)
  # --- User-Verwaltung einer Institution
  new = {}
  new['name'] = name = _(u'user_management.html')
  new['title'] = _(u'Verwaltung der Community-Mitglieder dieser Schule')
  new['integer_1'] = org_id
  save_item_values(user, 'dmsUserManagementOrg', name,
                    new, sysmaster_item_container, True, False)
  # --- User-Verwaltung
  new = {}
  new['title'] = _(u'User-Verwaltung')
  new['nav_title'] = new['title']
  new['is_browseable'] = False
  acl_item_container = save_container_values(user,
                'dmsUserFolder', ACL_USERS, new, folderschool_item_container)
  acl_item_container.set_is_changeable(False)
  # Webmaster mit den entsprechenden Rechten anlegen
  """
  try:
    user_id = get_user_by_username(username).id
    role_id = get_role_by_name('top_manager').id
    container_id = folderschool_item_container.container.id
    items = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)
    if len(items) == 0:
      DmsUserUrlRole.save_user_url_role(DmsUserUrlRole(), user_id, container_id, role_id)
    else:
      item = items[0]
      item.role_id = role_id
      item.save()
  """
  # --- Impressum
  new = {}
  name = 'impress.html'
  new['title'] = _(u'Impressum')
  new['text'] = _(u"""<p>Verantwortlich für diese Homepage ist</p>
%s
<p>Namentlich gekennzeichnete Beiträge in Diskussionsforen etc. 
werden von den jeweiligen Autoren verantwortet.</p>

<P>Ohne vorherige schriftliche Genehmigung ist eine kommerzielle Verbreitung der 
auf diesem Web-Angebot vorhandenen Dokumente ausdrücklich untersagt.</p>
""") % address
  impress_item = save_item_values(user, 'dmsDocument', name, new, folderschool_item_container, False, False)
  impress_item.set_is_changeable(False)
  # --- robots.txt
  new = {}
  name = 'robots.txt'
  new['title'] = _(u'Steuerung der Suchmaschinen')
  new['text'] = _(u"""# go away
User-agent: *
Disallow: */event_item_*
""")
  robots_item = save_item_values(user, 'dmsText', name, new, folderschool_item_container, False, False)
  robots_item.set_is_changeable(False)

  #do_protect_folder(folderschool_item_container, acl_item_container, True)
  #transaction.commit()
