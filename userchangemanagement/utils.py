# -*- coding: utf-8 -*-
"""
/dms/userchangemanagement/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.06.2007  Beginn der Arbeit
"""

import string

from django.utils.translation import ugettext as _

from dms.queries        import get_base_site_url
from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

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

