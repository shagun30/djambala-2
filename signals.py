#-*-coding: utf-8 -*-
"""
signals.py

.. beschreibt Routinen, die auf Signale reagieren
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.12.2007  Beginn der Arbeit
0.02  20.12.2007  gegebenenfalls Eintraege in DmsUserUrlRole loeschen
0.03  19.03.2008  signal_post_save
"""

from dms.settings       import LDAP_MODE

# -----------------------------------------------------
def signal_pre_delete(sender, instance, signal, *args, **kargs):
  """ wird vor dem Loeschen aufgerufen """
  name = instance.item.app.name
  ldap_mode = LDAP_MODE
  if instance.item.app.name == 'dmsUserFolder':
    from dms.models import DmsUserUrlRole
    name = instance.item.name
    path = instance.container.path[:instance.container.path.rfind(name)]
    # User aus Userfolder loeschen
    user_url_roles = DmsUserUrlRole.objects.filter(container__path=path)
    for user_url_role in user_url_roles:
      user_url_role.delete()
    # Userfolder in Arbeitsgruppe oder geschutztem Bereich?
    if ldap_mode and (instance.item.integer_1 == 1):
      from dms.auth.auth_ldap import ldap_user_class
      from dms.settings import LDAP_HOST
      from dms.settings import LDAP_PORT
      from dms.settings import LDAP_DN
      from dms.settings import LDAP_AUTH_USER
      from dms.settings import LDAP_AUTH_USER_PASSWORD
      from dms.models   import DmsItemContainer
      my_ldap = ldap_user_class(LDAP_HOST, LDAP_PORT, LDAP_DN, LDAP_AUTH_USER, LDAP_AUTH_USER_PASSWORD)
      # der oberste Userfolder ist tabu
      if instance.parent_item_id >= 0:
        my_ldap.del_group(path)
  elif instance.item.app.name == 'dmsSurvey':
    from dms.survey.queries   import delete_complete
    delete_complete(instance)
  elif instance.item.app.name == 'dmsEduScormItem':
    from dms.eduscormitem.utils   import delete_package
    delete_package(instance)
  elif instance.item.app.name == 'dmsFreemind':
    from dms.freemind.utils   import delete_package
    delete_package(instance)
  elif instance.item.app.name == 'dmsWikiItem':
    from dms.wiki.utils   import delete_page
    delete_page(instance)
  from dms.queries   import append_audit
  append_audit(instance, u'd')

# -----------------------------------------------------
def signal_post_delete(sender, instance, signal, *args, **kargs):
  """ wird nach dem Loeschen aufgerufen """
  from dms.settings import HOME_PATH
  from dms.queries import is_file_by_item_container
  if is_file_by_item_container(instance) and instance.container.path.find(HOME_PATH)>=0:
    from dms.folderfs.utils import calculate_quota
    owner = instance.item.owner
    calculate_quota(owner)

# -----------------------------------------------------
def signal_post_save(sender, instance, signal, *args, **kargs):
  """ wird nach dem Speichern aufgerufen """
  from dms.settings import HOME_PATH
  from dms.queries import is_file_by_item_container
  if is_file_by_item_container(instance) and instance.container.path.find(HOME_PATH)>=0:
    from dms.folderfs.utils import calculate_quota
    owner = instance.item.owner
    calculate_quota(owner)
  from dms.queries   import append_audit
  append_audit(instance, u'e')
