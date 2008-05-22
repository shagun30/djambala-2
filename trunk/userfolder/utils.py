# -*- coding: utf-8 -*-
"""
/dms/userfolder/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  22.01.2007  navigation_mode
"""

import string

from django.utils.translation import ugettext as _

from dms.auth.models    import User

from dms.models         import DmsUserUrlRole
from dms.queries        import get_base_site_url

from dms.utils_base     import ACL_USERS

# -----------------------------------------------------
def is_pupil(user_name):
  """ handelt es sich um einen Schueler? """
  return user_name.find('sch_') == 0

# -----------------------------------------------------
def get_users_count(item_container):
  """ Anzahl der User """
  n_pos = string.find(item_container.container.path, 'acl_users')
  path = item_container.container.path[:n_pos]
  return DmsUserUrlRole.objects.filter(container__path=path).count()

# -----------------------------------------------------
def get_all_users_with_email(user_folder):
  """ liefert die User des betreffende Userfolders mit E-Mail-Zugang """
  return DmsUserUrlRole.objects.filter(container=user_folder.container).\
                                filter(user__email__gt='').filter(user__is_active=True)

# -----------------------------------------------------
def get_users(item_container, order='last_name', start=0, diff=200):
  """ liefert diff User in diesem User-Folder """
  if item_container.container.path.find('acl_users') < 0:
    path = item_container.container.path
  else:
    n_pos = string.find(item_container.container.path, 'acl_users')
    path = item_container.container.path[:n_pos]
  if order == 'role':
    users = DmsUserUrlRole.objects.select_related().filter(container__path=path).\
                          order_by('auth_role.id')[start:start+diff]
  else:
    users = DmsUserUrlRole.objects.select_related().filter(container__path=path).\
                          order_by('user__'+order)[start:start+diff]
  return users

# -----------------------------------------------------
def get_all_users(item_container, order='last_name'):
  """ liefert alle User in diesem User-Folder """
  if item_container.container.path.find('acl_users') < 0:
    path = item_container.container.path
  else:
    n_pos = string.find(item_container.container.path, 'acl_users')
    path = item_container.container.path[:n_pos]
  if order == 'role':
    users = DmsUserUrlRole.objects.select_related().filter(container__path=path).\
                          order_by('auth_role.id')
  else:
    users = DmsUserUrlRole.objects.select_related().filter(container__path=path).\
                          order_by('auth_user.'+order)
  return users

# -----------------------------------------------------
def get_actions(request, user_perms, item):
  """ liefert die Verwaltungsoptionen in diesem Bereich """
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/manage_options_folderish.html')
  nPos = string.rfind(request.path, ACL_USERS)
  path = request.path[:nPos]
  if string.find ( path, 'index.html' ) < 0 :
    path += 'index.html'
  manage_mode = True
  c=Context({'authenticated'  : request.user.is_authenticated(),
            #'manage_mode'    : manage_mode,
             'no_add_mode'    : True,
             'show_mode'      : True,
             'no_image_mode'  : True,
             'path'           : path,
             'user_perms'     : user_perms,
             'user_name'      : request.user,
             'base_site_url'  : get_base_site_url(),})
  return t.render ( c)

# -----------------------------------------------------
def get_prev_next_line(item, start, diff, count):
  """ Geschwisterseiten anzeigen """
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/userfolder/prev_next.html')
  n_min = start-diff
  if n_min < 0:
    n_min = 0
    prev_url = ''
    prev_info = ''
  else:
    prev_url = './?start=%i&diff=%i' % (n_min, diff)
    prev_info = _(u'vorhergehende Mitglieder (%(start_diff)i-%(start)i)' % {'start_diff': start-diff, 'start': start-1} )
  n_start = start + diff
  if n_start >= count:
    next_url = ''
    next_info = ''
  else:
    n_end = n_start + diff
    next_url = './?start=%i&diff=%i' % (n_end, diff)
    if n_end > count:
      n_end = count
    next_info = _(u'nachfolgende Mitglieder ') + '(%i-%i)' % (n_start, n_end)
  end = start + diff - 1
  if end > count:
    end = count -start
  c = Context({'prev_url'     : prev_url,
               'prev_info'    : prev_info,
               'current_items': '&middot;&middot; %i-%i &middot;&middot;' % ( start, end ),
               'next_url'     : next_url,
               'next_info'    : next_info })
  return t.render(c)

