# -*- coding: utf-8 -*-
"""
/dms/image/utils.py

.. enthaelt Hilfefunktionen fuer Bilder
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit
"""

import string
from PIL import Image

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_actions(request, user_perms, item_container):
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('app/file/manage_options.html')
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
                  'path'           : get_site_url(item_container,
                                         item_container.item.name), } )
  return t.render ( c)

# -----------------------------------------------------
def get_image_size(filename):
  try:
    im = Image.open(filename)
    width = im.size[0]
    height = im.size[1]
  except:
    width = height = 0
  return width, height
