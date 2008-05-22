#-*-coding: utf-8 -*-
"""
queries.py

.. beschreibt Abfragen an das dms-Systems:
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2007  Beginn der Arbeit
0.02  27.08.2007  get_lernrestyp_*
0.03  28.08.2007  DmsEduItem
0.04  29.08.2007  DmsEduFachSachgebiet
0.05  30.08.2007  get_edu_sprache_id
0.06  04.09.2007  DmsEduSchlagwortStem
0.07  10.09.2007  is_app_available
0.08  12.09.2007  is_browseable in save_container_values
0.09  02.10.2007  get_schulart_by_id
0.10  03.10.2007  count_user_items
0.11  11.10.2007  get_all_menus_left mit mode-Schalter
0.12  23.10.2007  get_empty_folders
0.13  07.11.2007  Verbesserung von save_navigation
0.14  10.11.2007  save_min_role_id, Korrekturen bei change_container_path
0.15  14.11.2007  mkdir_fs, mk_htaccess_fs
0.16  15.11.2007  get_role_by_name
0.17  21.11.2007  get_item_container_children_by_app
0.18  10.12.2007  Korrektur exist_item
0.19  14.12.2007  Integration der Authentifizierung via LDAP
0.20  29.12.2007  mk_htaccess_fs entfernt
0.21  22.01.2008  count_users
0.22  04.02.2008  DmsUserfolderConnected
0.23  14.04.2008  DmsQuota
0.24  17.04.2008  DmsGroup
"""

import  datetime, time
import  string
import  os
import  pickle
import  StringIO
import  random
import  Stemmer

from django.db              import transaction
from django.db.models       import Q
from django.utils.encoding  import smart_unicode

from django.utils.translation import ugettext as _

from dms.settings           import BASE_SITE_URL
from dms.settings           import DOWNLOAD_PATH, DOWNLOAD_PROTECTED_PATH
from dms.settings           import LDAP_AUTH_USER
from dms.settings           import LDAP_AUTH_USER_PASSWORD
from dms.settings           import LDAP_HOST
from dms.settings           import LDAP_PORT
from dms.settings           import LDAP_DN
from dms.settings           import LDAP_MODE
from dms.settings           import HOME_PATH
from dms.settings           import HOME_QUOTA

from dms.utils_base         import ACL_USERS

from dms.auth.models        import User

from dms.models             import get_last_modified
from dms.models             import DmsAudit
from dms.models             import DmsAntiSpam
from dms.models             import DmsApp
from dms.models             import DmsAppAllowed
from dms.models             import DmsComment
from dms.models             import DmsContainer
from dms.edufolder.models   import DmsEduItem
from dms.edufolder.models   import DmsEduFachSachgebiet
from dms.edufolder.models   import DmsEduLernResTyp
from dms.edufolder.models   import DmsEduMedienformat
from dms.edufolder.models   import DmsEduOrg
from dms.edufolder.models   import DmsEduSchlagwort
from dms.edufolder.models   import DmsEduSchlagwortStem
from dms.edufolder.models   import DmsEduSprache
from dms.edufolder.models   import DmsEduSchulart
from dms.edufolder.models   import DmsEduSchulstufe
from dms.edufolder.models   import DmsEduZielgruppe
from dms.models             import DmsItem
from dms.models             import DmsItemContainer
from dms.models             import DmsFeed
from dms.models             import DmsFeedItem
from dms.models             import DmsGroup
from dms.models             import DmsLicense
from dms.models             import DmsNavMenuLeft
from dms.models             import DmsNavMenuTop
from dms.models             import DmsOrg
from dms.models             import DmsOrgGroup
from dms.models             import DmsQuota
from dms.models             import DmsRoles
from dms.models             import DmsSearchEngine
from dms.models             import DmsSite
from dms.models             import DmsUserGroup
from dms.models             import DmsUserOrg
from dms.models             import DmsUserUrlRole
#from dms.models             import DmsUserfolderConnected

from dms.mediasurvey.models import DmsMediaSurvey
from dms.mediasurvey.models import DmsMediaSurvey_gruppe_form
from dms.mediasurvey.models import DmsMediaSurvey_items
from dms.mediasurvey.models import DmsMediaSurvey_option

from dms.fortbildung.models import Fort_Fach
from dms.fortbildung.models import Fort_Schulart

from dms.encode_decode      import decode_html
from dms.encode_decode      import decode_html_dir
from dms.mail               import send_control_email
from dms.mail               import send_control_member_active

# -----------------------------------------------------
# Log-System
# -----------------------------------------------------

# -----------------------------------------------------
def append_audit(obj, operation):
  """ fuegt operation 'e' oder 'd' bezueglich obj inerhalb von parent ein """
  # wenn item geloescht wurde, kann item_container nicht mehr auf item zugreifen
  if obj.item.id != None:
    audit_obj = DmsAudit()
    audit_obj.app = obj.item.app
    audit_obj.path = obj.container.path
    audit_obj.name = obj.item.name
    audit_obj.operation = operation
    audit_obj.title = obj.item.title
    audit_obj.owner = obj.owner
    audit_obj.modified  = get_last_modified()
    audit_obj.save()

# -----------------------------------------------------
# Filesystem
# -----------------------------------------------------

# -----------------------------------------------------
def mkdir_fs(item_container):
  """ .. erzeugt passendes Verzeichnis im Dateisystem """
  file_path = DOWNLOAD_PATH + item_container.container.path
  try:
    os.makedirs(file_path)
  except:
    pass
  os.chmod(file_path, 0750)
  file_path = DOWNLOAD_PROTECTED_PATH + item_container.container.path
  try:
    os.makedirs(file_path)
  except:
    pass
  os.chmod(file_path, 0750)
  #os.chown(file_path, 30, 8)

# -----------------------------------------------------
def rmdir_fs(item_container):
  """ .. loescht Verzeichnis im Dateisystem """
  file_path = DOWNLOAD_PATH + item_container.container.path
  try:
    os.rmdir(file_path)
  except:
    pass
  file_path = DOWNLOAD_PROTECTED_PATH + item_container.container.path
  try:
    os.rmdir(file_path)
  except:
    pass

# -----------------------------------------------------
"""
def mk_htaccess_fs(item_container, overwrite=False):
  " .. erzeugt - gegebenenfalls abhaengig von overwrite - die passende .htaccess in Dateisystem "
  pos = item_container.container.path.rfind('acl_users')
  if pos > 0:
    ldap_path = item_container.container.path[:pos]
  else:
    ldap_path = item_container.container.path
  file_path = DOWNLOAD_PATH + ldap_path
  htaccess_path = file_path + '.htaccess'
  htaccess = "AuthName 'Dateien'
AuthType Basic
AuthBasicProvider ldap
AuthLDAPBindDN "cn=%s,%s"
AuthLDAPBindPassword %s
AuthLDAPURL "ldap://%s:%s/ou=community,%s?uid?sub?(objectClass=*)"
AuthLDAPGroupAttributeIsDN Off
AuthLDAPGroupAttribute memberUid
require ldap-group cn=%s,ou=groups,%s
" % (LDAP_AUTH_USER, LDAP_DN, LDAP_AUTH_USER_PASSWORD, LDAP_HOST, LDAP_PORT, LDAP_DN, ldap_path, LDAP_DN)
  if not overwrite:
    try:
      s = os.stat(htaccess_path)
    except:
      overwrite = True
  if overwrite:
    f = open(htaccess_path, 'w')
    f.write(htaccess)
    f.close()
    os.chmod(htaccess_path, 0600)
    os.chown(htaccess_path, 30, 8)
"""

# -----------------------------------------------------
def do_protect_folder(item_container, acl_item_container, do_protect=False):
  """ item_container schuetzen bzw. wieder freigeben """
  if do_protect or item_container.container.is_protected():
    acl_item_container.item.integer_1 = True
    acl_item_container.item.save()
    """
    if LDAP_MODE:
      from dms.auth.auth_ldap import ldap_user_class
      from dms.settings import LDAP_HOST
      from dms.settings import LDAP_PORT
      from dms.settings import LDAP_DN
      from dms.settings import LDAP_AUTH_USER
      from dms.settings import LDAP_AUTH_USER_PASSWORD
      my_ldap = ldap_user_class(LDAP_HOST, LDAP_PORT, LDAP_DN, LDAP_AUTH_USER, LDAP_AUTH_USER_PASSWORD)
      my_ldap.add_group(item_container.container.path)
      mk_htaccess_fs(acl_item_container, True)
    """

# -----------------------------------------------------
# Auth
# -----------------------------------------------------

def get_user(username):
  """ diese Funktion liefert das User-Objekt, das zu <username> gehoert """
  if username == '':
    return None
  return User.objects.get(username=username)

def get_user_by_id(id):
  return User.objects.get(id=id)

def get_user_not_active():
  return User.objects.filter(is_active=False).order_by('-date_joined')

def get_all_users():
  """ liefert alle freigeschalteten User """
  return DmsUserOrg.objects.filter(user__is_active=True)

def count_users(user_folder):
  """ liefert die Anzahl der User des betreffende Userfolders """
  return DmsUserUrlRole.objects.filter(container=user_folder.container).count()

def count_users_with_email(user_folder):
  """ liefert die Anzahl der User des betreffende Userfolders """
  return DmsUserUrlRole.objects.filter(container=user_folder.container).\
                                filter(user__email__gt='').filter(user__is_active=True).count()

@transaction.commit_manually
def set_user_active(id, send_email=True):
  user = User.objects.get(id=id)
  user.is_active = True
  user.save()
  # auf der obersten Ebene ohne Rechte eintragen
  user_url_role = DmsUserUrlRole()
  user_url_role.user = user
  user_url_role.container = get_container_by_id(1)
  user_url_role.role = get_role_by_name('no_rights')
  user_url_role.save()
  transaction.commit()
  if send_email:
    send_control_member_active(user)
  return user

def get_older_user_not_active(days):
  time_new = time.mktime(time.localtime()) - days*24*60*60
  old = time.strftime('%Y-%m-%d', time.localtime(time_new))
  return User.objects.filter(is_active=False).filter(date_joined__lt=old).order_by('-date_joined')

@transaction.commit_manually
def delete_user(id):
  """ loescht den betreffenden User """
  user = User.objects.get(id=id)
  try:
    user_url_role = DmsUserUrlRole.objects.filter(user=user)
    user_url_role.delete()
  except:
    pass
  try:
    user_org = DmsUserOrg.objects.get(user=user)
    user_org.delete()
  except:
    pass
  try:
    user_group = DmsUserGroup.objects.get(user=user)
    user_group.delete()
  except:
    pass
  user.delete()
  transaction.commit()  # transaction.rollback()

def delete_user_by_username(username):
  """ bestimmt das zu <username> passende User-Objekt und loescht es anschliessend """
  try:
    user = User.objects.get(username=username)
    delete_user(user.id)
  except:
    pass

def delete_user_by_email(email):
  """ bestimmt das zu <email> passende User-Objekt und loescht es anschliessend """
  try:
    users = User.objects.filter(email=email)
    for user in users:
      delete_user(user.id)
  except:
    pass

def get_distinct_info_mangers(item_container):
  """ liefert die Liste der (aktiven) Patinnen und Paten """
  path = item_container.container.path
  res = DmsItemContainer.objects.filter(container__path__istartswith=path).\
                         select_related().values('owner').distinct()
  # Durch die Brust ins Auge !!!!!
  user_ids = []
  for r in res:
    user_ids.append(r['owner'])
  query = 'id in (' + str(user_ids)[1:-1].replace('L', '') +')'
  return User.objects.extra(where=[query]).order_by('last_name', 'first_name')

def get_org_path(user):
  """ liefert Pfad fuer Home-Verzeichnis von user """
  org = get_org_by_username(user)
  if org.org_id >= 0 :
    org_id_name = 'schule_' + str(org.org_id)
  else:
    org_id_name = 'org_' + str(org.org_id)[1:]
  path = '%s%s/' % (HOME_PATH, org_id_name)
  return path, org_id_name, org

def get_home_path(user):
  """ liefert Pfad fuer Home-Verzeichnis von user """
  path, org_id_name, org = get_org_path(user)
  path = '%s%s/' % (path, user.username)
  return path

def get_home_url(user):
  """ liefert die URL des Home-Verzeichnisses """
  path = get_home_path(user)
  return get_item_container_by_path(path).get_absolute_url()

def has_home(user):
  """ falls Home-Verzeichnis vorhanden ist, wird True zurueckgegeben """
  home_path = get_home_path(user)
  containers = DmsContainer.objects.select_related().filter(path=home_path)
  return (len(containers)>0)

def create_home(user):
  """ falls noch nicht vorhanden, wird Home-Verzeichnis fuer user angelegt """
  # --- ist Org-Ordner vorhanden?
  org_path, org_name, org = get_org_path(user)
  containers = DmsContainer.objects.select_related().filter(path=org_path)
  if len(containers) == 0:
    item_container = get_item_container_by_path(HOME_PATH)
    # --- falls nicht vorhanden, wird das Home-Verzeichnis angelegt
    if item_container == None:
      new = {}
      new['name'] = HOME_PATH[1:-1]  # / am Anfang und Ende entfernen
      new['title'] = _(u'Home-Verzeichnisse')
      new['nav_title'] = _(u'Home')
      new['is_browseable'] = False
      new['integer_1'] = 0
      item_container = get_item_container_by_path('/')
      item_container = save_container_values(user, 'dmsFolder', new['name'], new, item_container)
    # --- Org-Verzeichnis angelegen
    new = {}
    new['name'] = org_name
    new['title'] = org.organisation
    new['nav_title'] = org.organisation
    new['is_browseable'] = True
    new['integer_1'] = 0
    this_item_container = save_container_values(user, 'dmsFolder', org_name, new, item_container)
  else:
    this_item_container = get_item_container_by_path(containers[0].path)
  from dms.home import utils
  utils.create_home(user.username, this_item_container)

# -----------------------------------------------------
# User
# -----------------------------------------------------

def get_user_by_email(email):
  users = User.objects.filter(email__iexact=email)
  if len(users) > 0:
    return users[0]
  else:
    return None

def get_user_by_username(username):
  users = User.objects.filter(username__exact=username)
  if len(users) > 0:
    return users[0]
  else:
    return None

# -----------------------------------------------------
# DmsOrg
# -----------------------------------------------------

def get_org_by_name(org_name, school_only=False):
  if school_only:
    return DmsOrg.objects.filter(org_id__gt=0).filter(organisation__istartswith=org_name).\
                  order_by('organisation', 'town')
  else:
    return DmsOrg.objects.filter(organisation__istartswith=org_name).\
                  order_by('organisation', 'town')

def get_org_by_name_no_school(org_name):
  return DmsOrg.objects.filter(org_id__lt=0).filter(organisation__istartswith=org_name).\
                order_by('organisation', 'town')

def get_org_by_number(org_number):
  return DmsOrg.objects.filter(org_id=org_number)

def get_org_by_town(town_name, school_only=False):
  if school_only:
    return DmsOrg.objects.filter(org_id__gt=0).filter(town__istartswith=town_name).\
                  order_by('organisation', 'town')
  else:
    return DmsOrg.objects.filter(town__istartswith=town_name).\
                  order_by('organisation', 'town')

def get_org_by_town_no_school(town_name):
  return DmsOrg.objects.filter(org_id__lt=0).filter(town__istartswith=town_name).\
                  order_by('organisation', 'town')

def get_org_by_org_id(org_id):
   orgs = DmsOrg.objects.filter(org_id=org_id)
   if len(orgs) > 0:
     return orgs[0]
   else:
     return None

def get_orgs():
  """ Liste aller Organisationen """
  return DmsOrg.objects.order_by('organisation')

def get_userfolder_org_id(item_container):
  """ untersucht, ob es sich um einen Userfolder einer Organisation handelt """
  path = item_container.container.path
  while item_container.parent_item_id!=-1 and \
        (item_container.item.app.name!='dmsFolder' or \
         (item_container.item.app.name=='dmsFolder' and item_container.item.integer_1==0)\
        ):
    item_container = item_container.get_parent()
    path = item_container.container.path
  return item_container.item.integer_1

def get_org_by_group(group):
  return DmsOrg.objects.filter(organisation__icontains=group).order_by('organisation')

# -----------------------------------------------------
# DmsOrgGroup
# -----------------------------------------------------

def get_org_groups():
  return DmsOrgGroup.objects.order_by('name')

# -----------------------------------------------------
# DmsAntiSpam
# -----------------------------------------------------

def get_random_question_answer():
  """ liefert nach Zufall eine Frage sowie die passende Antwort """
  n_max = DmsAntiSpam.objects.count()
  r = random.randint(1, n_max)
  item = DmsAntiSpam.objects.filter(id=r)[0]
  return item.question, item.answer

def get_random_question():
  """ liefert nach Zufall eine Frage """
  n_max = DmsAntiSpam.objects.count()
  r = random.randint(1, nMax)
  item = DmsAntiSpam.objects.filter(id=r)[0]
  return item.question

def check_answer(question, answer):
  """ kontrolliert, ob zu <question> die Antwort passt """
  items = DmsAntiSpam.objects.filter(question=decode_html(question))
  if len(items) == 0:
    return False
  return ( string.lower(item.answer) == string.lower(decode_html(answer)) )

# -----------------------------------------------------
# DmsApp
# -----------------------------------------------------

def get_app_list(order_by=''):
  """ .. liefert die Liste der Applikation """
  if order_by == '':
    return DmsApp.objects.all().order_by('name')
  else:
    return DmsApp.objects.all().order_by(order_by)

def get_app(app_name):
  """ .. liefert die Eigenschaften der Applikation <app_name> """
  return DmsApp.objects.get(name=app_name)

def is_app_available(app_name):
  """ .. liefert die Eigenschaften der Applikation <app_name> """
  return DmsApp.objects.get(name=app_name).is_available

def get_app_by_id(id):
  """ .. liefert die Eigenschaften der Applikation <id> """
  return DmsApp.objects.get(id=id)

# -----------------------------------------------------
# DmsAppAllowed
# -----------------------------------------------------

def app_is_allowed(parent_item_container, item_container):
  if DmsAppAllowed.objects.\
        filter(parent_app=parent_item_container.item.app).count() == 0:
    return True
  return DmsAppAllowed.objects.\
            filter(parent_app=parent_item_container.item.app.id).\
            filter(child_app=item_container.item.app.id).count() != 0

# -----------------------------------------------------
# DmsComment
# -----------------------------------------------------

def get_all_comments(item_container):
  return DmsComment.objects.filter(parent_item=item_container.item).select_related().\
                    order_by('-last_modified')

def get_visible_comments(item_container):
  return DmsComment.objects.filter(parent_item=item_container.item).filter(is_browseable=True).\
                    order_by('last_modified')

def get_visible_comment_count_by_item_containers(item_containers):
  """ liefert die jeweilige Anzahl von Kommemtaren Eintraegen in item_containers """
  ret = {}
  for i in item_containers:
    n = DmsComment.objects.filter(parent_item=i.item).filter(is_browseable=True).count()
    ret[i.item.id] = n
  return ret

# -----------------------------------------------------
# DmsContainer
# -----------------------------------------------------

def get_parent_path(path):
  return path[:1+path[:-1].rfind('/')]

def get_parent_container(container):
  """ liefert parent_container """
  if container.path == '/':
    return container
  path = container.path
  parent_path = get_parent_path(path)
  return DmsContainer.objects.get(path=parent_path)

def is_file_by_item_container(item_container):
  """ handelt es sich um ein Datei-Objekt (im Download-Bereich)? - siehe views_clipboard is_file_type """
  app_name = item_container.item.app.name
  return ( app_name in ['dmsFile', 'dmsExerciseFile',
                        'dmsImage', 'dmsImagethumb',
                        'dmsEduFileItem', 'dmsEduScormItem',
                        'dmsFreemind'] )

def get_container_by_id(id):
  return DmsContainer.objects.get(id=id)

def get_containers_by_path(path, select_related=False):
  if select_related:
    return DmsContainer.objects.select_related().filter(path=path)
  else:
    return DmsContainer.objects.filter(path=path)

def get_new_container(name, my_folder):
  """ initialisiert einen neuen Datensatz """
  new_path = my_folder.container.path + name + '/'
  containers = get_containers_by_path(path=new_path)
  if len(containers) > 0:
    self = containers[0]
  else:
    self = DmsContainer()
  self.this_item_id    = 0
  self.site_id         = my_folder.container.site_id
  self.path            = new_path
  self.is_top_folder   = False
  # --- Folder-Objekte "erben" die min_role_id-Eigenschaft in Arbeitsgruppen
  parent_container = get_parent_container(self)
  self.min_role_id    = parent_container.min_role_id
  self.nav_title       = ''
  self.menu_top_id     = my_folder.container.menu_top_id
  self.menu_left_id    = my_folder.container.menu_left_id
  self.nav_name_top    = my_folder.container.nav_name_top
  self.nav_name_left   = my_folder.container.nav_name_left
  self.sections        = ''
  self.show_next       = False
  return self

def get_new_container_with_data(name, item_container, old_container):
  """ initialiSiert einen neuen Datensatz """
  new_path = item_container.container.path + name + '/'
  containers = get_containers_by_path(path=new_path)
  if len(containers) > 0:
    self = containers[0]
  else:
    self = DmsContainer()
  self.this_item_id    = 0
  self.site_id         = item_container.container.site_id
  self.path            = new_path
  self.is_top_folder   = False
  self.min_role_id    = old_container.min_role_id
  self.nav_title       = old_container.nav_title
  self.menu_top_id     = item_container.container.menu_top_id
  self.menu_left_id    = item_container.container.menu_left_id
  self.nav_name_top    = item_container.container.nav_name_top
  self.nav_name_left   = item_container.container.nav_name_left
  self.sections        = old_container.sections
  self.show_next       = old_container.show_next
  return self

def change_container_path(old_path, new_path):
  """ Namen des Containers aendern; gegebenenfalls Ordnernamen im Dateisystem anpassen """
  file_old_path = DOWNLOAD_PATH + old_path
  file_new_path = DOWNLOAD_PATH + new_path
  try:
    os.rename(file_old_path, file_new_path)
  except:
    pass
  file_old_path = DOWNLOAD_PROTECTED_PATH + old_path
  file_new_path = DOWNLOAD_PROTECTED_PATH + new_path
  try:
    os.rename(file_old_path, file_new_path)
  except:
    pass
  containers = DmsContainer.objects.filter(path__startswith=old_path)
  for container in containers:
    container.path = container.path.replace(old_path,new_path)
    container.save()

def get_container_sitemap(item_container, start, length, include_userfolder=True):
  """ liefert <item_container> untergeordnete Container-Objekte """
  path = item_container.container.path
  if include_userfolder:
    count = DmsContainer.objects.filter(path__startswith=path).count()
    if start + length < count:
      max = start + length
    else:
      max = count
    containers = DmsContainer.objects.filter(path__startswith=path).\
                              order_by('path')[start:max]
  else:
    count = DmsContainer.objects.filter(path__startswith=path).\
                         exclude(path__contains='acl_users').count()
    if start + length < count:
      max = start + length
    else:
      max = count
    containers = DmsContainer.objects.filter(path__startswith=path).\
                              exclude(path__contains='acl_users').\
                              order_by('path')[start:max]
  return containers, count

@transaction.commit_manually
def save_min_role_id(item_container, old, new):
  """ speichert <min_role_id> bei untergeordneten Containern """
  key = 'min_role_id'
  containers = DmsContainer.objects.select_related().\
                        filter(path__startswith=item_container.container.path)
  for c in containers:
    if c.min_role_id != new[key]:
      c.min_role_id = new[key]
      c.save()
  transaction.commit()

#def is_protected(item_container):
#  """ prueft, ob <item_container> zugriffsgeschuetzt ist """
#  return (item_container.container.min_role_id < 2000)

def is_protected_app(item_container):
  """ prueft, ob <item_container> zugriffsgeschuetzt ist """
  return (item_container.item.app.name in ['dmsProjectgroup', 'dmsFolderProtected'])

# -----------------------------------------------------
# DmsEduItem
# -----------------------------------------------------

def get_new_edu_items(item_container, days, start, length):
  """ liefert aktuelle Edu-Objekte, die vor hoechstes <days> Tagen geaendert wurden """
  path = item_container.container.path
  my_date = datetime.datetime.fromtimestamp(time.time()-days*24*60*60).\
            strftime('%Y-%m-%d')
  count = DmsItemContainer.objects.filter(container__path__startswith=path).\
                    filter(last_modified__gt=my_date).count()
  if start + length < count:
    max = start + length
  else:
    max = count
  item_containers = DmsItemContainer.objects.select_related().\
                    filter(container__path__startswith=path).\
                    filter(last_modified__gt=my_date).\
                    order_by('-last_modified')[start:max]
  return item_containers, count

def get_eduitem(item):
  """ liefert die Details des entsprechenden Edu-Objektes """
  try:
    return DmsEduItem.objects.get(item=item)
  except:
    return None

def delete_stemmed_keyword(edu_item, schlagwort):
  try:
    obj = edu_item.schlagwort.get(name=schlagwort)
    obj.delete()
  except:
    pass

def insert_stemmed_keyword(edu_item, schlagwort, schlagwort_org):
  try:
    stem = DmsEduSchlagwort.objects.get(name=schlagwort)
  except:
    res = DmsEduSchlagwortStem.objects.filter(stem=schlagwort)
    if len(res) < 1:
      obj = DmsEduSchlagwortStem()
      obj.name = schlagwort_org
      obj.stem = schlagwort
      obj.save()
    obj = DmsEduSchlagwort()
    obj.name = schlagwort
    obj.save()
    return insert_stemmed_keyword(edu_item, schlagwort, schlagwort_org)
  edu_item.schlagwort.add(stem)

# -----------------------------------------------------
# DmsEduFachSachgebiet
# -----------------------------------------------------

def get_edu_faecher():
  """ liefert alle Faecher - geordnet nach Namen """
  return DmsEduFachSachgebiet.objects.all().order_by('order_by', 'name')

def get_edu_fach_id_by_name(name):
  """ liefert die id fuer das Fach 'name'
      falls das Fach nicht existiert, wird -1 zurueckgegeben
  """
  res = DmsEduFachSachgebiet.objects.filter(name=name)
  if len(res) == 0:
    return -1
  else:
    return res[0].id

def get_edu_fach_by_id(id):
  """ liefert den Fachnamen fuer id """
  return DmsEduFachSachgebiet.objects.get(id=id)

def get_edu_link_by_url(link):
  """  
  Falls bereits Web-Adressen mit der url <link> in den Lernarchiven existieren,
  werden diese zurueckgegeben.
  """
  app = DmsApp.objects.get(name='dmsEduLinkItem')
  return DmsItemContainer.objects.filter(item__url_more=link).filter(item__app=app)

# -----------------------------------------------------
# DmsEduLernResTyp
# -----------------------------------------------------

def get_lernrestyp_all():
  return DmsEduLernResTyp.objects.order_by('order', 'name')

def get_lernrestyp_by_id(id):
  return DmsEduLernResTyp.objects.get(id=id)

def get_lernrestyp_by_name(name):
  """ liefert den <lernrestyp> zu <name> oder -1 """
  item_containers = DmsEduLernResTyp.objects.filter(name=name)
  if len(item_containers) == 0:
    return -1
  else:
    return item_containers[0]

# -----------------------------------------------------
# DmsEduMedienformat
# -----------------------------------------------------

def get_medienformat_all():
  return DmsEduMedienformat.objects.order_by('name')

def get_medienformat_by_id(id):
  """ liefert das entsprechende Medienformat """
  return DmsEduMedienformat.objects.get(id=id)

def get_medienformat_by_name(name):
  """ liefert zum Namen passende Medienformat """
  return DmsEduMedienformat.objects.get(name=name)

# -----------------------------------------------------
# DmsEduOrg
# -----------------------------------------------------

def get_edu_org_beschreibung(key):
  """ liefert die Beschreibung der entsprechenden Organisation """
  res = DmsEduOrg.objects.get(schluessel=key)
  if res == None:
    return _('Unbekannte Organisation')
  else:
    return res.beschreibung

# -----------------------------------------------------
# DmsEduSchlagwortStem
# -----------------------------------------------------

def get_schlagworte(schlagwort):
  """ liefert die Liste der Schlagworte, die mit <schlagwort> beginnen """
  return DmsEduSchlagwortStem.objects.filter(name__istartswith=schlagwort)

def get_stemmed(word, insert=False):
  """
  .. liefert die gestemmte Version von <word>
  Falls nicht vorhanden, wird None zurueckgeliefert, bzw. bei <insert>=True
  in die Tabelle eingefuegt
  """
  word = str(word).strip()
  if word == '':
    return ''
  try:
    res = DmsEduSchlagwortStem.objects.get(name=word.lower())
    return res.stem
  except:
    if not insert:
      return None
    stemmer = Stemmer.Stemmer('german')
    stemmed = stemmer.stemWord(word.lower())
    s = DmsEduSchlagwortStem()
    s.name = word
    s.stem = stemmed
    s.save()
    # ---auch in der gestemmten Liste eintragen
    try:
      s = DmsEduSchlagwort()
      s.name = stemmed
      s.save()
    except:
      pass
    return stemmed

def get_schlagwort_by_stem(stem):
  """ .. liefert das zu <stem> gehoerende Orginalschlagwort """
  try:
    res = DmsEduSchlagwortStem.objects.get(stem=stem)
    return res.name
  except:
    return _('Unbekannt')

# -----------------------------------------------------
# DmsEduSprache
# -----------------------------------------------------

def get_edu_sprachen():
  """ liefert alle Sprachen - geordnet nach Namen """
  return DmsEduSprache.objects.all().order_by('name')

def get_edu_sprache_id(key):
  """ liefert die ID der betreffenden Sprache wie z.B. 'de' bzw. 'Deutsch' """
  res = DmsEduSprache.objects.filter(key=key)
  if len(res) == 0:
    res = DmsEduSprache.objects.filter(name=key)
    if len(res) == 0:
      return -1
    else:
      return res[0].id
  else:
    return res[0].id

# -----------------------------------------------------
# DmsEduSchulart
# -----------------------------------------------------

def get_schulart_all():
  return DmsEduSchulart.objects.order_by('order', 'name')

def get_schulart_id_by_name(name):
  """ liefert die zu der Schulart <name> passende id oder -1 """
  res = DmsEduSchulart.objects.filter(name__icontains=name)
  if len(res) == 0:
    return -1
  else:
    return res[0].id

# -----------------------------------------------------
# DmsEduSchulstufe
# -----------------------------------------------------

def get_schulstufe_all():
  return DmsEduSchulstufe.objects.order_by('order', 'name')

def get_schulstufe_id_by_name(name):
  """ liefert die zu der Schulstufe <name> passende id oder -1 """
  res = DmsEduSchulstufe.objects.filter(name=name)
  if len(res) == 0:
    return -1
  else:
    return res[0].id

# -----------------------------------------------------
# DmsEduZielgruppe
# -----------------------------------------------------

def get_zielgruppe_all():
  return DmsEduZielgruppe.objects.order_by('order', 'name')

def get_zielgruppe_id_by_name(name):
  """ liefert die zu der Zielgruppe <name> passende id oder -1 """
  res = DmsEduZielgruppe.objects.filter(name=name)
  if len(res) == 0:
    return -1
  else:
    return res[0].id

# -----------------------------------------------------
# DmsItem
# -----------------------------------------------------

def get_item_by_id(id):
  return DmsItem.objects.select_related().get(id=id)

def get_top_item():
  return DmsItemContainer.objects.select_related().get(id=1)

def get_all_items(order_by):
  return DmsItem.objects.order_by(order_by)

def set_extra_data(**kwargs):
  if kwargs == {}:
    pickled_text = ''
  else:
    output = StringIO.StringIO()
    pickle.dump(kwargs, output, 2)
    pickled_text = output.getvalue()
    output.close()
  return unicode(pickled_text, 'iso-8859-1')

def get_extra_data(item_container):
  pickled_text = item_container.item.extra.encode('iso-8859-1')
  if pickled_text == '':
    return None
  input = StringIO.StringIO(pickled_text)
  try:
    obj = pickle.load(input)
    input.close()
    return obj
  except:
    extra = {}
    extra['schlagwort_org'] = _(u'Fehlerhafte Kodierung\nBitte neu eingeben !!')
    return extra
    #return _(u'Fehler: ') + pickled_text

def get_extra_var(data, key, default):
  if data == None:
    return default
  elif data.has_key(key):
    return data[key]
  else:
    return default

def get_image_items(path):
  """ liefert die bilder des betreffenden Verzeichnisses """
  return DmsItemContainer.objects.select_related().\
                          filter(container__path=path).\
                          filter(item__app__id=14)

def get_item_by_url_more(url):
  """ ... liefert den zu <url> passenden Datensaetze, sonst None """
  items = DmsItem.objects.select_related().filter(url_more=url)
  if len(items) > 0:
    return items
  else:
    return None

# -----------------------------------------------------
# DmsItemContainer
# -----------------------------------------------------

def get_top_item_container():
  return DmsItemContainer.objects.select_related().get(id=1)

def get_item_container_by_id(id, select_related=False):
  if select_related:
    item_containers = DmsItemContainer.objects.select_related().filter(id=id)
  else:
    item_containers = DmsItemContainer.objects.filter(id=id)
  if len(item_containers) == 0:
    return None
  else:
    return item_containers[0]

def get_item_container_by_url(url):
  protocol = 'http://'
  if url.find(protocol) != 0:
    return None
  l = len(protocol)
  n_pos = l + url[l:].find('/')
  base_url = url[:n_pos]
  site = DmsSite.objects.get(url=base_url)
  path_url = site.base_folder + url[n_pos:].replace('index.html', '')
  return get_item_container_by_path_and_name(path_url, '')

def get_item_containers_by_item_container_id(item_container_id, select_related=False):
  if select_related:
    return DmsItemContainer.objects.select_related().filter(id=item_container_id)
  else:
    return DmsItemContainer.objects.filter(id=item_container_id)

def get_item_containers_by_item_id(item_id, select_related=False):
  if select_related:
    return DmsItemContainer.objects.select_related().filter(item__id=item_id)
  else:
    return DmsItemContainer.objects.filter(item__id=item_id)

def get_item_container_by_path_and_name(path, name):
  if name != '':
    item_containers = DmsItemContainer.objects.select_related().\
                                       filter(container__path=path).\
                                       filter(item__name=name)
  else:
    item_containers = DmsItemContainer.objects.select_related().\
                                       filter(container__path=path)
  if len(item_containers) == 0:
    return None
  else:
    return item_containers[0]

def get_item_container_by_parent_item_id(parent_item_id):
  return DmsItemContainer.objects.select_related().filter(parent_item_id=parent_item_id)

def get_item_containers_by_container(container, select_related=False):
  if select_related:
    return DmsItemContainer.objects.select_related().filter(container=container)
  else:
    return DmsItemContainer.objects.filter(container=container)

def get_item_container_children(item_container, select_related=False):
  """ liefert alle Kind-Objekte zu item_container """
  if select_related:
    return DmsItemContainer.objects.select_related().\
              filter(container__path__startswith=item_container.container.path)
  else:
    return DmsItemContainer.objects.\
              filter(container__path__startswith=item_container.container.path)

def get_item_container_child_by_name(item_container, name):
  """ liefert, falls vorhanden, den zu name passenden Eintrag """
  return get_item_container_by_path_and_name(item_container.container.path, name)

def count_item_container_children_by_app(item_container, app):
  """ liefert die Anzahl aller Kinder von <item_container> vom Typ <app> """
  return DmsItemContainer.objects.\
            filter(container__path__startswith=item_container.container.path).\
            filter(item__app=app).\
            count()

def get_item_container_children_by_app(item_container, app, start, length):
  """ liefert alle Kinder von <item_container> vom Typ <app> """
  count = count_item_container_children_by_app(item_container, app)
  if start + length < count:
    max = start + length
  else:
    max = count
  return DmsItemContainer.objects.select_related().\
            filter(container__path__startswith=item_container.container.path).\
            filter(item__app=app).\
            order_by('container__path')[start:max]
  #order_by('dms_dmscontainer.path')[start:max]

def count_item_container_children_by_app_or_name(item_container, app_id, name):
  """ liefert die Anzahl aller Kinder von <item_container> vom Typ <app> mit dem Namen name """
  if app_id < 0:
    return DmsItemContainer.objects.\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__name=name).count()
  elif name == '':
    return DmsItemContainer.objects.\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__app=app_id).count()
  else:
    return DmsItemContainer.objects.\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__app=app_id).\
              filter(item__name=name).count()

def get_item_container_children_by_app_or_name(item_container, app_id, name, start, length):
  """ liefert alle Kinder von <item_container> vom Typ <app> mit dem Namen name """
  count = count_item_container_children_by_app_or_name(item_container, app_id, name)
  if start + length < count:
    max = start + length
  else:
    max = count
  if app_id < 0:
    return DmsItemContainer.objects.select_related().\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__name=name).\
              order_by('container__path')[start:max]
    #order_by('dms_dmscontainer.path')[start:max]
  elif name == '':
    return DmsItemContainer.objects.select_related().\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__app=app_id).\
              order_by('container__path')[start:max]
    #order_by('dms_dmscontainer.path')[start:max]
  else:
    return DmsItemContainer.objects.select_related().\
              filter(container__path__startswith=item_container.container.path).\
              filter(item__app=app_id).\
              filter(item__name=name).\
              order_by('container__path')[start:max]
    #order_by('dms_dmscontainer.path')[start:max]

def get_item_containers_by_url_more(url):
  """ liefert den zu <url_more> item_container; sonst None """
  if url.strip() == '':
    return None
  item_containers = DmsItemContainer.objects.select_related().filter(item__url_more=url.strip())
  if len(item_containers) == 0:
    return None
  else:
    return item_containers[0]

def get_item_container_data_object_by_id(item_id):
  """ liefert das Datenobjekt zu item_id """
  return DmsItemContainer.objects.select_related().filter(item=item_id).filter(is_data_object=True)

def get_empty_folders(item_container):
  """ liefert eine Liste leerer Ordner unterhalb von item_container """
  total = 0
  path = item_container.container.path
  containers = DmsContainer.objects.filter(path__startswith=path)
  item_containers = []
  for c in containers:
    ics = DmsItemContainer.objects.filter(parent_item_id=c.this_item_id)
    if len(ics) == 0:
      try:
        ics = DmsItemContainer.objects.get(container=c)
        item_containers.append(ics)
      except:
        pass
    total += 1
  return item_containers, total

# -----------------------------------------------------
@transaction.commit_manually
def save_this_item_values(item, owner, my_folder, is_browseable, section):
  """ item wird gespeichert, Verbindung zu Container in DmsItemContainer """
  item.save()
  item_container = DmsItemContainer.save_values(
                      DmsItemContainer(), my_folder.container, item,
                      owner, is_browseable, section)
  transaction.commit()

# -----------------------------------------------------
#@transaction.commit_manually
def save_item_values(user, app_name, name, new, my_folder, is_browseable,
                     send_email=True,
                     visible_start=None, visible_end=None, is_data_object=True):
  """ Daten werden in DmsItem gespeichert, Container-Bezuege in DmsItemContainer """
  if not new.has_key('license'):
    new['license'] = 1
  if app_name != 'dmsText':
    new = decode_html_dir(new)
  app = get_app(app_name)
  users = User.objects.filter(username=user)
  if len(users) > 0:
    owner = users[0]
  else:
    owner = User.objects.filter(username='anonymous')[0]
  item = DmsItem.get_new_item(DmsItem(), name, new, my_folder, app, owner)
  item.license = DmsLicense.objects.filter(id=new['license'])[0]
  item.save()
  if new.has_key('section'):
    sec = new['section']
  else:
    sec = ''
  item_container = DmsItemContainer.save_values(
                      DmsItemContainer(), my_folder.container, item, owner,
                      is_browseable, sec,
                      visible_start=visible_start, visible_end=visible_end,
                      is_data_object=is_data_object,
                      parent_item_container=my_folder)
  #transaction.commit()
  if send_email:
    send_control_email(item_container)
  return item_container

# -----------------------------------------------------
@transaction.commit_manually
def save_container_values(user, app_name, name, new, my_folder):
  """ Daten werden in DmsItem gespeichert, Container-Bezuege in DmsItemContainer """
  if not new.has_key('license'):
    new['license'] = 1
  app = get_app(app_name)
  users = User.objects.filter(username=smart_unicode(user))
  if len(users) > 0:
    owner = users[0]
  else:
    owner = User.objects.filter(username='anonymous')[0]
  container = get_new_container(name, my_folder)
  if new['nav_title'] != '' :
    container.nav_title = new['nav_title']
  else :
    container.nav_title = new['title']
  if new.has_key('sections'):
    container.sections = new['sections']
  else:
    container.sections = ''
  container.min_role_id = container.min_role_id
  if new.has_key('min_role_id'):
    container.min_role_id = int(new['min_role_id'])
  if new.has_key('menu_top_id'):
    container.menu_top_id = int(new['menu_top_id'])
  if new.has_key('menu_left_id'):
    container.menu_left_id = int(new['menu_left_id'])
  if new.has_key('nav_name_top'):
    container.nav_name_top = new['nav_name_top']
  if new.has_key('nav_name_left'):
    container.nav_name_left = new['nav_name_left']
  container.save()
  # --- Eigenschaften des Ordners festlegen
  item = DmsItem.get_new_item(DmsItem(), name, new, my_folder, app, owner)
  item.license = DmsLicense.objects.filter(id=new['license'])[0]
  item.save ()
  # --- Rueckverweis eintragen
  container.this_item_id = item.id
  container.save()
  try:
    section = new['section']
  except:
    section = ''
  if new.has_key('is_browseable'):
    is_browseable = new['is_browseable']
  else:
    is_browseable = True
  if new.has_key('is_changeable'):
    is_changeable = new['is_changeable']
  else:
    is_changeable = True
  item_container = DmsItemContainer.save_values( 
                       DmsItemContainer(), container, item, owner, is_browseable, 
                       section, my_folder.item.id, 
                       parent_item_container=my_folder)
  # fuer Vortraege
  if new.has_key('show_next'):
    item_container.container.show_next = True
    item_container.container.save()
  transaction.commit()
  if app.name != 'dmsUserFolder':
    mkdir_fs(item_container)
  return item_container

# -----------------------------------------------------
def move_containers(paste_item_container, item_container):
  """ Container werden rekursiv verschoben """
  paste_path = paste_item_container.container.path
  dest_path = item_container.container.path
  n_pos = 1 + paste_path[:-1].rfind('/')
  containers = DmsContainer.objects.filter(path__startswith=paste_path)
  ret_path = dest_path + paste_item_container.container.path[n_pos:]
  for container in containers:
    container.path = dest_path + container.path[n_pos:]
    container.site = item_container.container.site
    container.is_top_folder  = False
    container.min_role_id   = item_container.container.min_role_id
    container.menu_top_id    = item_container.container.menu_top_id
    container.menu_left_id   = item_container.container.menu_left_id
    container.nav_name_top   = item_container.container.nav_name_top
    container.nav_name_left  = item_container.container.nav_name_left
    container.save()
  return DmsContainer.objects.get(path=ret_path)

# -----------------------------------------------------
# DmsItemContainer
# -----------------------------------------------------

def get_prev_parent_item_containers(item_container):
  return DmsItemContainer.objects.select_related().\
                   filter(parent_item_id=item_container.parent_item_id). \
                   filter(order_by__lt=item_container.order_by). \
                   order_by('order_by')

def get_next_parent_item_containers(item_container):
  return DmsItemContainer.objects.select_related().\
                          filter(parent_item_id=item_container.parent_item_id). \
                          filter(order_by__gt=item_container.order_by). \
                          order_by('order_by')

def get_item_container_by_item_id(id):
  """ liefert zu einem Objekt das Eltern-Objekt """
  try:
    return DmsItemContainer.objects.select_related().get(item__id=id)
  except:
    return None

# -----------------------------------------------------
def get_new_item_container(new, my_item_container, owner):
  """ initialisiert einen neuen Datensatz """
  
  def get_value(key, new, default, do_check_paragraph=False):
    """ """
    if new.has_key(key):
      if do_check_paragraph:
        item_container.__dict__[key] = check_paragraph(new[key])
      else:
        item_container.__dict__[key] = new[key]
    else:
      item_container.__dict__[key] = default

  def get_datetime(key):
    try:
      return datetime.datetime.strptime(new[key], '%Y-%m-%d %H:%M')
    except:
      if new[key].find(' ') >= 0:
        return datetime.datetime.strptime(new[key][:new[key].find(' ')], '%Y-%m-%d')
      else:
        return datetime.datetime.strptime(new[key], '%Y-%m-%d')

  item_container = DmsItemContainer()
  item_container.container = my_item_container.container
  item_container.item      = my_item_container.item
  item_container.owner     = owner
  get_value('section', new, '')
  get_value('is_deleted', new, False)
  get_value('parent_item_id', new, -1)
  get_value('order_by', new, 100)
  get_value('is_browseable', new, True)
  if new.has_key('visible_start'):
    item_container.visible_start = get_datetime('visible_start')
  else:
    get_value('visible_start', new, datetime.date.today())
  if new.has_key('visible_end'):
    item_container.visible_end = get_datetime('visible_end')
  else:
    this_year = int(datetime.datetime.now().strftime ( '%Y' ))
    get_value('visible_end', new, datetime.date(int(this_year)+10,12,31))
  if new.has_key('last_modified'):
    item_container.last_modified = get_datetime('last_modified')
  else:
    get_value('last_modified', new, get_last_modified())
  return item_container

def get_data_item_container(item_container):
  """ liefert den eigentlichen Daten-Item-Container """
  item = item_container.item
  return DmsItemContainer.objects.filter(item=item).filter(is_data_object=True)[0]

def get_linked_item_containers(item_container):
  """ liefert die Item-Container der Einblendungen """
  item = item_container.item
  ics = DmsItemContainer.objects.filter(item=item).filter(is_data_object=False)
  if len(ics) > 0:
    return ics
  else:
    return []

# -----------------------------------------------------
def count_user_items(item_container, user):
  """ liefert die Anzahl der Ressourcen von <user> """
  path = item_container.container.path
  return DmsItemContainer.objects.filter(owner=user).\
                          filter(container__path__startswith=path).count()

def get_user_item_containers(item_container, user, start, length):
  """ liefert die item_container von <user> """
  path = item_container.container.path
  count = count_user_items(item_container, user)
  if start + length < count:
    max = start + length
  else:
    max = count
  return DmsItemContainer.objects.filter(owner=user).\
                          filter(container__path__startswith=path).\
                          order_by('-last_modified')[start:max]

# -----------------------------------------------------
# DmsGroup
# -----------------------------------------------------

def get_group_by_id(id):
  """ liefert die zu id passende Gruppe """
  return DmsGroup.objects.get(id=id)

def get_groups_by_org_id(org_id, order_by='description'):
  """ liefert die Gruppen der Institution org_id """
  return DmsGroup.objects.filter(org_id=org_id).order_by(order_by)

def add_group(org_id, description, is_primary=False):
  """ ergaenzt eine neue Gruppe fuer org_id """
  group = DmsGroup()
  group.org_id = org_id
  group.description = description
  group.is_primary = is_primary
  group.save()

def delete_group_by_id(id):
  """ loescht die Gruppe id """
  DmsGroup.objects.filter(id=id).delete()

def delete_groups_by_org_id(org_id):
  """ loescht die Gruppen von org_id """
  DmsGroup.objects.filter(org_id=org_id).delete()

# -----------------------------------------------------
# DmsLicense
# -----------------------------------------------------

def get_licenses():
  return DmsLicense.objects.order_by('name')

def get_license_by_id(id):
  return DmsLicense.objects.get(id=id)

def get_null_license():
  return get_license_by_id(1)

# -----------------------------------------------------
# DmsMediaSurvey_gruppe_form
# -----------------------------------------------------

def get_mediasurvey_by_org_id(org_id):
  return DmsMediaSurvey.objects.filter(org_id=org_id)

def get_mediasurvey_items_by_org_id(org_id):
  return DmsMediaSurvey_items.objects.filter(org_id=org_id)

def get_mediasurvey_gruppe_form(group):
  return DmsMediaSurvey_gruppe_form.objects.filter(gruppe__gruppe=group).order_by('form')

def get_mediasurvey_option(group):
  return DmsMediaSurvey_option.objects.filter(gruppe__gruppe=group).order_by('option')

def get_mediasurvey_gruppe_form_count(group):
  return DmsMediaSurvey_gruppe_form.objects.filter(gruppe__gruppe=group).count()

def get_mediasurvey_gruppe_form_item(name):
  return DmsMediaSurvey_gruppe_form.objects.filter(form=name)[0]

def get_mediasurvey_option_item(name):
  return DmsMediaSurvey_option.objects.filter(option=name)[0]

# -----------------------------------------------------
# DmsNavMenuLeft
# -----------------------------------------------------

def delete_menuitem_navmenu_left(menu_id):
  DmsNavMenuLeft.objects.filter(menu_id=menu_id).delete()

def get_menuitems_by_menu_id_left(menu_id):
  return DmsNavMenuLeft.objects.filter(menu_id=-1*menu_id)

def get_menuitems_navmenu_left(menu_id, name):
  return DmsNavMenuLeft.objects.filter(menu_id=menu_id, name=name)

def get_new_navmenu_left():
  return DmsNavMenuLeft()

def get_all_menus_left(mode=0):
  """ liefert linke Navigation; 0=alle, 1=is_menu_menu, 2=not is_main_menu """
  if mode == 0:
    return DmsNavMenuLeft.objects.select_related().filter(menu_id__lt=0).order_by('-menu_id')
  elif mode == 1:
    return DmsNavMenuLeft.objects.select_related().filter(menu_id__lt=0).\
              filter(is_main_menu=True).order_by('-menu_id')
  else:
    return DmsNavMenuLeft.objects.select_related().filter(menu_id__lt=0).\
              filter(is_main_menu=False).order_by('-menu_id')

def get_menu_by_name_left(name):
  return DmsNavMenuLeft.objects.get(name=name)

def get_next_menu_left_id():
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute('SELECT MAX(menu_id) FROM dms_dmsnavmenuleft')
  row = cursor.fetchone()
  return 1+row[0]

def get_min_max_menu_left():
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute('SELECT MIN(menu_id), MAX(menu_id) FROM dms_dmsnavmenuleft')
  row = cursor.fetchone()
  return row[0], row[1]

# -----------------------------------------------------
# DmsNavMenuTop
# -----------------------------------------------------

def delete_menuitem_navmenu_top(menu_id):
  DmsNavMenuTop.objects.filter(menu_id=menu_id).delete()

def get_menuitems_by_id_navmenu_top(id):
  return DmsNavMenuTop.objects.select_related().filter(id=id)

def get_menuitems_navmenu_top(menu_id, name):
  return DmsNavMenuTop.objects.filter(menu_id=menu_id, name=name)

def get_new_navmenu_top():
  return DmsNavMenuTop()

# -----------------------------------------------------
# DmsQuota
# -----------------------------------------------------

def has_quota(username):
  """ falls Quota fuer user bereits existiert wird true zurueckgegeben """
  quota = DmsQuota.objects.filter(username=username)
  return (len(quota) > 0)

def create_quota(username, max=HOME_QUOTA):
  """ erzeugt Quota fuer user """
  quota = DmsQuota()
  quota.username = username
  quota.max = max
  quota.value = 0
  quota.save()

def get_quota(username):
  """ liefert Quota von user """
  return DmsQuota.objects.get(username=username)

def set_quota(username, value):
  """ setzt Quota von user """
  quota = get_quota(username)
  quota.value = value
  quota.save()

# -----------------------------------------------------
# DmsRoles
# -----------------------------------------------------

def get_all_roles(my_role=0):
  """ liefert die moeglichen Rollen """
  return DmsRoles.objects.filter(id__gte=my_role).order_by('id')

def get_role_by_user_path(user, path):
  """ SOLLTE ELEGANTER PROGRAMMIERT WERDEN """
  if user.id == None:
    return 0
  # --- finde einen userfolder
  p = path
  acl_users = ACL_USERS + '/'
  items = get_containers_by_path(p + acl_users)
  while len(items) == 0 and p > '/':
    # --- Pfad des uebergeordneten Containers
    p = get_parent_path(p)
    items = get_containers_by_path(p + acl_users)
  if len(items) != 0:
    # --- acl_users wieder entfernen
    items = get_containers_by_path(p)
    user_role_obj = get_user_url_role_by_container_id(user, items[0].id)
    if user_role_obj == None:
      return get_role_by_user_path(user, get_parent_path(p))
    else:
      role = user_role_obj.role.id
  else:
    role = 0
  return role

def get_role_by_name(name):
  """ liefert, falls vorhanden, die zu <name> passende Rolle """
  roles = DmsRoles.objects.filter(name=name)
  if len(roles) == 0:
    return None
  else:
    return roles[0]

def get_role_by_id(id):
  """ liefert die zu <id> passende Rolle """
  return DmsRoles.objects.get(id=id)

# -----------------------------------------------------
# DmsRssFeed
# -----------------------------------------------------

def get_feed(id):
  """ liefert RSS-Feed """
  return DmsFeed.objects.get(id=id)
  #        f = DmsFeed.objects.filter(id=int(r))[0]

def delete_feed_by_name(name):
  """ loescht den RSS-Feed <name> durch setzen von is_deleted=True """
  feed = DmsFeed.objects.get(name=name)
  feed.is_deleted = True
  feed.save()

def delete_total_feed_by_name(name):
  """ loescht den RSS-Feed <name> durch setzen von is_deleted=True """
  feed = DmsFeed.objects.get(name=name)
  feed.delete()

def undo_feed_by_name(name):
  """ loescht den RSS-Feed <name> durch setzen von is_deleted=True """
  feed = DmsFeed.objects.get(name=name)
  feed.is_deleted = False
  feed.save()

def save_feed(user, name, new):
  """ speichert den RSS-Feed ab """
  feed = DmsFeed()
  feed.name          = name
  feed.title         = new['title']
  feed.description   = new['text']
  feed.link          = new['url_more']
  feed.general_mode  = new['section']
  feed.owner         = User.objects.get(username=user)
  feed.is_deleted    = False
  feed.last_modified = get_last_modified()
  feed.save()

def get_feed_name(request, op):
  """ liefert den Namen und den Return-Pfad bei RSS-Feeds """
  path = request.path[:-len(op)-2]
  n_pos = path.rfind('/')
  name = path[n_pos+1:]
  path = path[:n_pos+1]
  item_container = get_item_container_by_path_and_name(path, '')
  if item_container != None:
    ret_path = get_site_url(item_container, 'index.html/manage/')
    return name, ret_path
  else:
    return name, path

# -----------------------------------------------------
# DmsRssFeedItem
# -----------------------------------------------------

def get_all_feed_items(order=''):
  if order == 'feed':
    return DmsFeedItem.objects.select_related().order_by('feed__title')
    #return DmsFeedItem.objects.select_related().order_by('dms_dmsfeed.title')
  elif order == 'title':
    return DmsFeedItem.objects.select_related().order_by('item__title')
    #return DmsFeedItem.objects.select_related().order_by('dms_dmsitem.title')
  elif order == 'date':
    return DmsFeedItem.objects.select_related().order_by('-last_modified')
  else:
    return DmsFeedItem.objects.select_related().order_by('is_browseable')

def exist_feed_item(feed, item_container):
  return DmsFeedItem.objects.filter(feed=feed).filter(item_container=item_container).count() > 0

def get_feed_items(item_container):
  return DmsFeedItem.objects.filter(item_container=item_container)

# -----------------------------------------------------
# DmsUserGroup
# -----------------------------------------------------

def delete_users_in_group(group_id):
  """ loescht die User der Gruppe group_id """
  DmsUserGroup.objects.filter(group__id=group_id).delete()

def delete_group_by_user_id(user_id):
  """ loescht die Gruppeneintraege von user_id """
  user_group = DmsUserGroup.objects.filter(user__id=user_id).filter(group__is_primary=False)
  user_group.delete()

def delete_primary_group_by_user(user):
  """ loescht die Primaergruppe von user """
  user_group = DmsUserGroup.objects.filter(user=user).filter(group__is_primary=True)
  user_group.delete()

def get_users_by_org_id(org_id):
  """ liefert die zu org_id passenden User """
  return DmsUserOrg.objects.filter(org_id=org_id).select_related().\
          order_by('user__last_name', 'user__first_name')

def get_users_by_group_id(group_id):
  """ liefert die zu group_id passenden User """
  return DmsUserGroup.objects.filter(group__id=group_id).select_related().\
          order_by('user__last_name', 'user__first_name')

def get_primary_group_by_user(user):
  """ liefert die Primaergruppe von user """
  user_groups = DmsUserGroup.objects.filter(user=user).filter(group__is_primary=True)
  if len(user_groups) > 0:
    return user_groups[0]
  else:
    return None

def set_user_group(user, group):
  """ ordnet user einer group zu """
  user_group = DmsUserGroup.objects.filter(user=user).filter(group=group)
  if len(user_group) > 0:
    return
  user_group = DmsUserGroup()
  user_group.user = user
  user_group.group = group
  user_group.save()

# -----------------------------------------------------
# DmsUserOrg
# -----------------------------------------------------

def get_org_id(user):
  """ falls user existiert, wird die org_id zurueckgegeben; sonst 0 """
  items = DmsUserOrg.objects.filter(user__username=user)
  if len(items) > 0:
    return items[0].org_id
  else:
    return 0

def get_org_by_username(user):
  """ falls user existiert, wird die Organisation zurueckgegeben; sonst None """
  items = DmsUserOrg.objects.filter(user__username=user)
  if len(items) > 0:
    return get_org_by_org_id(items[0].org_id)
  else:
    return None

def get_users_by_org_id(org_id):
  """ liefert alle Community-Mitglieder der Einrichtung org_id """
  return DmsUserOrg.objects.filter(org_id=org_id).select_related().\
         order_by('user__last_name', 'user__first_name')

def get_users_with_email_by_org_id(org_id):
  """ liefert alle Community-Mitglieder mit E-Mail-Adressen der Einrichtung org_id """
  return DmsUserOrg.objects.filter(org_id=org_id).filter(user__email__gt='')

def set_user_org(org_id, user):
  """ ordnet user org_id zu """
  user_org = DmsUserOrg()
  user_org.user = user
  user_org.org_id = org_id
  user_org.save()

# -----------------------------------------------------
# DmsUserRole
# -----------------------------------------------------

def get_user_url_role_by_container_id(user, container_id):
  items = DmsUserUrlRole.objects.filter(user=user).filter(container=container_id)
  if len(items) == 0:
    return None
  else:
    return items[0]

def get_my_homes(user):
  """ liefert die Verzeichnisse, zu denen user Zugang hat """
  return DmsUserUrlRole.objects.filter(user=user)

def create_user_url_role(user, container, role):
  """ erzeugt den entsprechenden Eintrag in DmsUserUrl """
  DmsUserUrlRole.save_user_url_role(DmsUserUrlRole(), user.id, container.id, role.id)

def get_user_url_role(user, container):
  """ liefert, falls vorhanden, den zu user und container passenden Eintrag """
  return DmsUserUrlRole.objects.filter(user=user.id).filter(container=container.id)

# -----------------------------------------------------
# DmsSearchEngine
# -----------------------------------------------------

def get_search_engines():
  return DmsSearchEngine.objects.order_by('name')

# -----------------------------------------------------
# DmsSite
# -----------------------------------------------------

def get_site_by_id(id):
  return DmsSite.objects.get(id=id)

def get_site_by_org_id(org_id):
  return DmsSite.objects.get(org_id=org_id)

def get_sites(order_by):
  return DmsSite.objects.select_related().order_by(order_by)

# -----------------------------------------------------
# Fort_Fach
# -----------------------------------------------------

def get_faecher():
  """ liefert alle Faecher - geordnet nach Namen """
  return Fort_Fach.objects.all().order_by('name')

def get_fach_id_by_name(name):
  """ liefert die id von name bzw. None """
  faecher = Fort_Fach.objects.filter(name__iexact=name)
  if len(faecher) > 0:
    return faecher[0]
  else:
    return None

def get_fach_by_id(id):
  """ liefert den Fachnamen zu <id> """
  return Fort_Fach.objects.get(id=id)

# -----------------------------------------------------
# Fort_Schultyp
# -----------------------------------------------------

def get_schularten():
  """ liefert die Liste der vorhandenen Schularten """
  return Fort_Schulart.objects.all().order_by('name')

def get_schulart_by_id(id):
  """ liefert den Fachnamen zu <id> """
  return Fort_Schulart.objects.get(id=id)

# -----------------------------------------------------
# Allgemeine Anfragen
# -----------------------------------------------------

def exist_item(item_container, name):
  if item_container == None or name == '':
    return False
  return (DmsItemContainer.objects.filter(parent_item_id=item_container.container.this_item_id).\
                                   filter(item__name=name).count() != 0)
  #return (DmsItemContainer.objects.filter(container=item_container.container).\
  #                                 filter(item__name=name).count() != 0)

def get_folder_filtered_items(item_container, alpha_mode=False, app_types=[], data_mode=False):
  """ liefert die Liste der entsprechenden item_container zurueck """
  today = datetime.datetime.today()
  if alpha_mode:
    order = 'item__title'
    #order = 'dms_dmsitem.title'
  elif data_mode:
    #hr order = '-visible_start'
    order = 'visible_start'
  else:
    order = 'order_by'
    #order = 'dms_dmsitemcontainer.order_by'
  if app_types == []:
    items = DmsItemContainer.objects.select_related().\
                              filter(parent_item_id=item_container.item.id). \
                              filter(is_browseable=True). \
                              filter(is_deleted=False). \
                              exclude(item__app__name='dmsUserFolder'). \
                              filter(visible_start__lte=today).\
                              filter(visible_end__gte=today). \
                              order_by(order)
  else:
    myQ = None
    for app_name in app_types:
      if myQ == None:
        myQ = Q(item__app__name=app_name)
      else:
        myQ = myQ | Q(item__app__name=app_name)
    items = DmsItemContainer.objects.select_related().\
                              filter(parent_item_id=item_container.item.id). \
                              filter(is_browseable=True). \
                              filter(is_deleted=False). \
                              exclude(item__app__name='dmsUserFolder'). \
                              filter(visible_start__lte=today).\
                              filter(visible_end__gte=today). \
                              filter(myQ). \
                              order_by(order)
  return items

def get_folder_filtered_items_date_ordered(item_container):
  today = datetime.datetime.today()
  items = DmsItemContainer.objects.select_related().\
                            filter(parent_item_id=item_container.item.id). \
                            filter(is_browseable=True). \
                            filter(is_deleted=False). \
                            exclude(item__app__name='dmsUserFolder'). \
                            filter(visible_start__lte=today).\
                            filter(visible_end__gte=today). \
                            order_by('-last_modified')
  #order_by('-dms_dmsitemcontainer.last_modified')
  return items

# -----------------------------------------------------
def get_folder_items(item_container, order, app=None):
  """ liefert in dem Ordner enthaltenen Objekte """
  reverse = (order != '' and order[0] == '-')
  if reverse:
    order = order[1:]
  if order == '' or order == 'name':
    order_by = 'item__name'
    #order_by = 'dms_dmsitem.name'
  elif order == 'title':
    order_by = 'item__title'
    #order_by = 'dms_dmsitem.title'
  elif order == 'date' :
    order_by = 'last_modified'
  else :
    order_by = 'item__app_id'
    #order_by = 'dms_dmsitem.app_id'
  if reverse:
    order_by = '-' + order_by
  if app == None:
    return DmsItemContainer.objects.select_related().\
                            filter(parent_item_id=item_container.item.id).\
                            order_by(order_by)
  else:
    return DmsItemContainer.objects.select_related().\
                            filter(parent_item_id=item_container.item.id).\
                            filter(item__app=app).order_by(order_by)

# -----------------------------------------------------
def get_folder_own_items(item, order, user_id) :
  """ liefert in dem Ordner enthaltenen Objekte """
  if order == '':
    order = 'name'
  return DmsItem.objects.select_related().filter(parent_item_id=item.folder_id). \
                                          filter(owner_id=user_id). \
                                          order_by(order)
# -----------------------------------------------------
def get_item_container(rPath, rAction=''):
  """ liefert die Eigenschaften des Objektes """

  def get_name_and_path ( rPath, rAction='' ) :
    """ liefert Pfad und Namen des Objektes """
    import string
    if string.find ( rPath, 'index.html' ) > 0 :
      cIndex = 'index.html' + rAction
      my_path = rPath[:-1*len(cIndex)]
      nPos = string.rfind ( my_path[:-1], '/' )
      my_name = my_path[nPos+1:-1]
    else :
      if rAction == '' :
        path = rPath
      else :
        path = rPath[:-1*len(rAction)]
      nPos = string.rfind ( path, '/' )
      my_name = path[nPos+1:]
      my_path = path[:nPos+1]
    return my_name, my_path

  my_name, my_path = get_name_and_path(rPath, rAction)
  return get_item_container_by_path_and_name(my_path, my_name)

# -----------------------------------------------------
def get_item_container_by_path(path):
  """ liefert die Eigenschaften des Objektes """
  item_containers = DmsItemContainer.objects.select_related().filter(container__path=path)
  if len(item_containers) == 0:
    return None
  else:
    return item_containers[0]

# -----------------------------------------------------
def get_top_url(item_container):
  """ findet uebergeordnetes Objekt """
  if item_container.parent_item_id == -1 :
    return ''
  else :
    parent = item_container.get_parent()
    site = parent.container.site
    path = parent.container.path
    length=len(site.base_folder)
    t = site.url+path[length:]
    if length < len(path):
      return site.url+path[length:]
    else :
      return site.url + '/'

# -----------------------------------------------------
def get_parent_app(item_container):
  """ liefert die Art des Eltern-Objektes """
  parent_item_container = item_container.get_parent()
  return parent_item_container.item.app.name

# -----------------------------------------------------
def get_site_url(item_container, name):
  """ liefert die absolute URL """
  site = item_container.container.site
  path = item_container.container.path + name
  length = len(site.base_folder)
  if length < len(path):
    return site.url+path[length:]
  else:
    return site.url + '/'

# -----------------------------------------------------
def get_base_site_url():
  """ liefert die URL der obersten Startseite """
  return BASE_SITE_URL
 
# -----------------------------------------------------
@transaction.commit_manually
def save_navigation(item_container, old, new):
  """ die Navigation wird fuer <item_container> und Unter-Container geaendert """
  # --- eigene Navigation = eigenes Menue !!
  item_containers = DmsItemContainer.objects.filter(item__app__has_own_breadcrumb=True)
  paths = []
  for ic in item_containers:
    paths.append(ic.container.path)
  key = 'navigation_left'
  containers = DmsContainer.objects.select_related().\
                        filter(path__startswith=item_container.container.path)
  for c in containers:
    if c.nav_name_left != new[key]:
      is_projectgroup = False
      for path in paths:
        if c.path.find(path) == 0:
          is_projectgroup = True
          break
      if not is_projectgroup:
        c.nav_name_left = new[key]
        c.save()
  transaction.commit()

# -----------------------------------------------------
def save_manage_browseable_values(request, items):
  """ Sichtbarkeit in den Objekten speichern """
  checked = request.POST.copy()
  for i in items:
    delete_key  = 'delete_' + smart_unicode(i.item.id)
    if i.is_deleted and not checked.has_key(delete_key):
      i.is_deleted = False
      i.save()
    elif not i.is_deleted and checked.has_key(delete_key):
      i.is_deleted = True
      i.save()
    else:
      visible_key = 'visible_' + smart_unicode(i.item.id)
      if i.is_browseable and not checked.has_key(visible_key):
        i.is_browseable = False
        i.save()
      elif not i.is_browseable and checked.has_key(visible_key):
        i.is_browseable = True
        i.save()

# -----------------------------------------------------
@ transaction.commit_manually
def save_item(item_container, old, new, send_email=False, func=None, new_user=None):
  """ speichert die Daten """
  if item_container.item.app.name != 'dmsText':
    new = decode_html_dir(new)
  if func != None:
    func(item_container, old, new)
  changed = item_container.item.save_values(old, new)
  item_container.save_modified_values(old, new, changed)
  if new_user != None:
    item_container.owner = new_user
    item_container.save()
  transaction.commit()
  if send_email:
    send_control_email(item_container)

# -----------------------------------------------------
@transaction.commit_manually
def save_item_container(item_container, old, new, send_email=False):
  """ speichert ausschliesslich die Daten von item_container """
  item_container.save_modified_values(old, new)
  transaction.commit()
  if send_email:
    send_control_email(item_container)

# -----------------------------------------------------
#def get_connections_with_userfolders(item_container):
#  """ liefert, falls vorhanden, die mit diesem Userfolder verbundenen Userfolder """
#  ufs = DmsUserfolderConnected.objects.filter(uf_master=item_container.id)
#  return ufs

