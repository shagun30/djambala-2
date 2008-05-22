#-*-coding: utf-8 -*-
"""
roles.py

.. beschreibt die Rollen des dms-Systems:
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.01.2007  Beginn der Arbeit
0.02  18.01.2007  Geruest von has_permission
0.03  21.01.2007  perm_manage_site, the_manager
0.04  19.02.2007  get_user_roles
0.05  02.10.2007  change_owner
0.06  13.05.2008  check
"""

import string

from django.utils.translation import ugettext as _

from dms.settings         import BASE_SITE_URL
from dms.auth.models      import User

from dms.models           import DmsRoles
from dms.models           import DmsUserUrlRole
from dms.models           import DmsContainer
from dms.perms            import *
from dms.views_error      import show_error

# -----------------------------------------------------
# Festlegung der Rollen und Rechte
# -----------------------------------------------------

def init_role(name):
  """ """
  perm = DmsRoles.objects.select_related().filter(name=name)[0]
  return { 'name':                  name,
           'description':           perm.description,
           'perm_read':             perm.perm_read,
           'perm_add':              perm.perm_add,
           'perm_add_folderish':    perm.perm_add_folderish,
           'perm_edit':             perm.perm_edit,
           'perm_edit_own':         perm.perm_edit_own,
           'perm_edit_folderish':   perm.perm_edit_folderish,
           'perm_manage':           perm.perm_manage,
           'perm_manage_own':       perm.perm_manage_own,
           'perm_manage_folderish': perm.perm_manage_folderish,
           'perm_manage_site':      perm.perm_manage_site,
           'perm_manage_user':      perm.perm_manage_user,
           'perm_manage_user_new':  perm.perm_manage_user_new
          }

the_manager     = init_role(name='the_manager')
top_manager     = init_role(name='top_manager')
manager         = init_role(name='manager')
co_manager      = init_role(name='co_manager')
worker          = init_role(name='worker')
worker_reader   = init_role(name='worker_reader')
worker_writer   = init_role(name='worker_writer')
no_rights_mini  = init_role(name='no_rights_mini')
no_rights_micro = init_role(name='no_rights_micro')
no_rights       = init_role(name='no_rights')

roles = (the_manager, top_manager, manager, co_manager, worker, worker_reader, worker_writer, 
         no_rights_mini, no_rights_micro, no_rights)

# -----------------------------------------------------
# Hilfsfunktionen
# -----------------------------------------------------

def get_user_roles(username, path):
  """ liefert die Rollen, die <user> in <path> zugewiesen wurden"""
  items = User.objects.filter(username=username)
  if len(items) == 0:
    return []
  user_id = items[0].id
  n_pos = string.rfind(path, 'acl_users')
  if n_pos > 0:
    path = path[:n_pos]
  n_pos = string.rfind(path, 'index.html')
  if n_pos > 0:
    path = path[:n_pos]
  items = DmsContainer.objects.filter(path=path)
  if len(items) == 0:
    # handelt es sich um eine Datei-Objekt?
    n_pos = max( string.rfind(path,'/edit/'),
                 string.rfind(path,'/check/'),
                 string.rfind(path,'/diff/'),
                 string.rfind(path,'/show/'),
                 string.rfind(path,'/ajax/'),
                 string.rfind(path,'/change_owner/'),
                 string.rfind(path,'/manage_comments/'),
                 string.rfind(path,'/add_rss/') )
    if n_pos > 0:
      path = path[:n_pos]
    n_pos = string.rfind(path, '/')
    if n_pos >= 0:
      path = path[:n_pos+1]
    items = DmsContainer.objects.filter(path=path)
    # --- Sonderfall: Pseudoadressen wie /css_generate/
    if len(items) == 0:
      n_pos = path[:-1].rfind('/')
      path = path[:n_pos+1]
      items = DmsContainer.objects.filter(path=path)
    #if len(items) == 0:
    #  return []
  container_id = items[0].id
  items = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)
  if len(items) == 0:
    while len(items) == 0 and path != '/':
      path = path[:-1]
      n_pos = string.rfind(path, '/')
      if n_pos >= 0:
        path = path[:n_pos+1]
        items = DmsContainer.objects.filter(path=path)
        container_id = items[0].id
      items = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)
  if len(items) > 0:
    r = items[0].role.name
    return [items[0].role.name]
  else:
    return []

# -----------------------------------------------------
# Welche Aenderungsrechte hat <user> in <path>?
# -----------------------------------------------------

class UserEditPerms:

  def __init__(self,user,path):

    def has_perm(roles, perm):
      ok = False
      for role in roles:
        ok = ok or eval(role)[perm]
        if ok: break
      return ok

    self.roles                 = get_user_roles(user, path)
    self.perm_read             = has_perm(self.roles, 'perm_read')
    self.perm_add              = has_perm(self.roles, 'perm_add')
    self.perm_add_folderish    = has_perm(self.roles, 'perm_add_folderish')
    self.perm_edit             = has_perm(self.roles, 'perm_edit')
    self.perm_edit_own         = has_perm(self.roles, 'perm_edit_own')
    self.perm_edit_folderish   = has_perm(self.roles, 'perm_edit_folderish')
    self.perm_manage           = has_perm(self.roles, 'perm_manage')
    self.perm_manage_own       = has_perm(self.roles, 'perm_manage_own')
    self.perm_manage_folderish = has_perm(self.roles, 'perm_manage_folderish')
    self.perm_manage_site      = has_perm(self.roles, 'perm_manage_site')
    self.perm_manage_user      = has_perm(self.roles, 'perm_manage_user')
    self.perm_manage_user_new  = has_perm(self.roles, 'perm_manage_user_new')

# -----------------------------------------------------
# Gibt es fuer den User/die Rolle ausreichende Rechte?
# -----------------------------------------------------

def has_permission(user, path, perm):
  """ prueft, ob <user> in <path> die Rechte <perm> besitzt """
  roles = get_user_roles(user, path)
  ok = False
  for role in roles:
    ok = eval(role)[perm]
    if ok: break
  return ok

def require_permission(perm):
  """ ueberprueft die Zugangsrechte: falls ok, wird die mit
      @require_permission dekorierte Funktion aufgerufen
      falls nein, werden entsprechende Fehlermeldungen ausgegeben
  """
  def decorator(func):
    def wrapper(*__args,**__kw):
      request=__args[0]
      if request.user.is_authenticated():
        if has_permission(request.user.username, request.path, perm):
          return func(*__args,**__kw)
        else:
          if len(__args) > 1:
            return show_error(__args[0],__args[1], _('Zugriffsrecht'),
                              _('<p>Ihre Zugriffsrechte passen hier nicht!</p>'))
          else:
            return show_error(__args[0],None, _('Zugriffsrecht'),
                              _('<p>Ihre Zugriffsrechte passen hier nicht!</p>'))
      else:
        if len(__args) >= 2:
          item_container = __args[1]
        else:
          item_container = None
        return show_error(__args[0], item_container, _('Zugriffsrecht'),
                          _('<p>Sie sind bislang nicht eingeloggt!</p>'),
                          BASE_SITE_URL + '/login/?next=' + request.path)
    return wrapper
  return decorator

