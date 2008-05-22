# -*- coding: utf-8 -*-
"""
/dms/folder/views_error.py

.. enthaelt Muster fuer Fehlerseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.01.2007  Beginn der Arbeit
0.02  04.02.2007  show_error_object_exist
0.03  21.05.2008  show_error_community_members_only
"""

from django.shortcuts  import render_to_response

from django.utils.translation import ugettext as _

from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.views          import get_my_item_container

# -----------------------------------------------------
def show_error(request, item_container, header, info, login_url='', is_hint=False):
  """ Fehlerseite anzeigen """
  if item_container != None:
    my_item_container = item_container
  else:
    my_item_container = get_my_item_container(request, 'login')
  if is_hint:
    title = header
  else:
    title = _('Fehler: ') + header
  if my_item_container != None:
    vars = {'content_div_style': 'frame-main-manage',
            'site'             : my_item_container.container.site,
            'title'            : title,
            'breadcrumb'       : get_breadcrumb(my_item_container),
            'content'          : info,
            'footer_email'     : get_footer_email(my_item_container),
            'last_modified'    : my_item_container.\
                                last_modified.strftime('%d.%m.%Y %H:%M'),
            'no_top_main_navigation': True,
            'login_url'        : login_url
          }
  else:
    vars = {'content_div_style': 'frame-main-manage',
            'title'            : title,
            'content'          : info,
            'no_top_main_navigation': True,
            'login_url'        : login_url
          }
  return render_to_response('error.html', vars)

# -----------------------------------------------------
def show_error_object_exist(request, item_container, name):
  """ ein Objekt mit dem Namen <name> existiert schon """
  return show_error(request, item_container, _('Objekt gleichens Namens'),
         _('<p>Ein Objekt mit dem Namen <i>') + name + _('</i> existiert schon!</p>') )

# -----------------------------------------------------
def show_error_spam(request, item_container):
  """ ein Objekt mit dem Namen <name> existiert schon """
  return show_error(request, item_container, _('Fehlerhafte Antwort'),
                    _('<p>Bitte beantworten Sie die Anti-Spam-Frage korrekt!</p>') )

# -----------------------------------------------------
def show_error_community_members_only(request, item_container):
  """ der freie Zugang ist gesperrt """
  return show_error(request, item_container, _(u'Nur für Community-Mitglieder'),
         _(u'<p>Nur (eingeloggte) Community-Mitglieder dürfen Ergänzungen vornehmen!</p>') )

