#-!-coding: utf-8 -!-
"""
/dms/document/utils.py

.. enthaelt Hilfefunktionen fuer Informationsseiten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2007  Beginn der Dokumentation
"""

import string

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

# -----------------------------------------------------
def get_actions(request, user_perms, item_container):
  """ verfuegbare Verwaltungsoptionen """
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/manage_options_item.html')
  nPos = max ( string.rfind ( request.path, '/add/' ),
               string.rfind ( request.path, '/edit/' ),
             )
  if nPos > -1 :
    path = request.path[:nPos]
    show_mode = True
  else :
    path = request.path
    show_mode = False
  if ( string.find(request.path, '/add/') >= 0 ) :
    edit_mode = False
  elif ( string.find(request.path, '/edit/') >= 0 ) :
    edit_mode = False
  else :
    edit_mode = request.user.is_authenticated()
  c = Context ( { 'authenticated'  : request.user.is_authenticated(),
                  'show_mode'      : show_mode,
                  'edit_mode'      : edit_mode,
                  'user_perms'     : user_perms,
                  'user_name'      : request.user,
                  'path'           : get_site_url(item, item.name), } )
  return t.render ( c)

