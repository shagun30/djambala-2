# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/utils.py

.. enthaelt Hilfefunktionen fuer Userverwaltung der Institutionen
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
0.02  30.04.2008  Primärgruppen
"""

import string
import datetime
import random

from django.db          import transaction
from django.utils.translation import ugettext as _

from dms.auth.models    import User

from dms.queries        import get_groups_by_org_id
from dms.queries        import get_user_by_email
from dms.queries        import set_user_group
from dms.queries        import get_group_by_id

from dms.utils          import show_link

from dms.userregistration.utils       import get_username

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_main_options(item_container, manage_options=False):
  """ die verschiedenen Programmoptionen """
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/folder/section.html')
  content = ''
  links = []
  base_url = item_container.get_absolute_url()
  if manage_options:
    my_title = _(u'Gruppen verwalten')
    links = []
    links.append(show_link(base_url + '?op=member_insert_group', _(u'Gruppenmitglieder aufnehmen')))
    links.append(show_link(base_url + '?op=member_change_group', _(u'Gruppenzugehörigkeit ändern')))
    links.append(show_link(base_url + '?op=member_delete_user_by_group', _(u'Gruppenmitglieder löschen')))
    links.append(show_link(base_url + '?op=member_change_primary_group', _(u'Primärgruppen ändern')))
    cSection = Context( { 'section': my_title, 'links': links } )
    content += tSection.render(cSection)
    my_title = _(u'Einzelpersonen verwalten')
    links = []
    links.append(show_link(base_url + '?op=password_reset', _(u'Kennwort zurücksetzen')))
    links.append(show_link(base_url + '?op=member_add_username', _(u'Mitglied aufnehmen')))
    links.append(show_link(base_url + '?op=member_delete_username', _(u'Mitglied löschen')))
    cSection = Context( { 'section': my_title, 'links': links } )
    content += tSection.render(cSection)
    my_title = _(u'Gruppennamen verwalten')
    links = []
    links.append(show_link(base_url + '?op=group_name_add', _(u'Gruppennamen ergänzen')))
    links.append(show_link(base_url + '?op=group_name_delete', _(u'Gruppennamen löschen')))
    cSection = Context( { 'section': my_title, 'links': links } )
    content += tSection.render(cSection)
  return content

# -----------------------------------------------------
def get_groups(org_id, primary_only=False):
  """ liefert die vorhandenen Gruppen der Organisation org_id """
  groups = get_groups_by_org_id(org_id)
  ret = []
  for group in groups:
    if not primary_only or group.is_primary:
      ret.append( { 'id': group.id, 'description': group.description, 'is_primary': group.is_primary} )
  return ret

# -----------------------------------------------------
def generate_passwd(length=6):
  """ erzeugt ein Kennwort aus Zufallszeichen """
  ret = ''
  if length < 6 :
    length = 6
  elif length > 10 :
    length = 10
  for x in xrange(length) :
    if x == 3 :
      ret += '-'
    ret += chr(random.randrange(ord('a'),ord('z'),1))
  return ret

# -----------------------------------------------------
def get_pupil_password(birthday):
  """ erzeugt Kennwort fuer Schueler/in """
  try :
    d,m,y = string.splitfields ( birthday, '.' )
  except :
    return ''
  ret = ''
  if len(d) == 0 :
    ret += '0'
  ret += str(d)
  if len(m) == 0 :
    ret += '0'
  ret += str(m)
  ret += str(y)
  return ret

# -----------------------------------------------------
@transaction.commit_manually
def create_member(org_id, group_id, target_group_ids, sex, first_name, last_name, title_name, email):
  """ legt einen User fuer org_id an und ordnet sie der group_id zu """
  user = get_user_by_email(email)
  # --- falls e-mail schon existiert wird nichts unternommen
  if user != None:
    if org_id > 0: # nur bei Schulen wird die Schulnummer vorangestellt
      prefix = '%i_' % org_id
    else:
      prefix = ''
    user = User()
    username = get_username(prefix, first_name, last_name)
    user.username = username
    user.sex = sex
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.title = title_name
    user.is_staff = False
    user.is_active = True
    user.is_superuser = False
    user.date_joined = datetime.datetime.now()
    password = generate_passwd()
    user.set_password(password)
    user.save()
    set_user_org(org_id, user)
    send_password(email, username, password)
  set_user_group(user, get_group_by_id(group_id))
  for group in target_group_ids:
    set_user_group(user, get_group_by_id(group))
  transaction.commit()
