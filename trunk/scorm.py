#-*-coding: utf-8 -*-
"""
/dms/scorm.py

.. enthaelt Routinen zur Kommunikation mit Scorm-Modulen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  10.03.2007  Beginn der Arbeit
"""

from django.http              import HttpResponse
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def scorm_show_top(request, item_container):
  """ Top-Scorm-Seite anzeigen """
  url = item_container.get_absolute_url()
  vars = { 'base_site_url': url[:1+url.rfind('/')], }
  return render_to_response ( 'scorm/nav_top.html', vars )

# -----------------------------------------------------
def scorm_show_left(request, item_container):
  """ linke Scorm-Seite anzeigen """
  url = item_container.get_absolute_url()
  vars = { 'base_site_url': url[:1+url.rfind('/')], }
  return render_to_response ( 'scorm/nav_left.html', vars )

# -----------------------------------------------------
def scorm_show_main(request, item_container):
  """ Haupt-Scorm-Seite anzeigen """
  url = item_container.get_absolute_url()
  vars = { 'base_site_url': url[:1+url.rfind('/')], }
  return render_to_response ( 'scorm/start.html', vars )

# -----------------------------------------------------
def scorm_show(request, item_container):
  """ Scorm-Seite anzeigen """
  url = item_container.get_absolute_url()
  vars = { 'base_site_url': url[:1+url.rfind('/')], }
  return render_to_response ( 'scorm/index.html', vars )

# -----------------------------------------------------
def scorm_ajax_call(request, item_container):
  """ Scorm-Kommunikation """
  #user_perms, add_ons = get_add_ons(request.user.username, request.path, item_container)
  #allow_copy = get_allow_copy(item_container)
  #t_link = get_template('app/base_manage_link.html')
  #main_obj, objs, objs_linkable = get_objs(request, item_container, allow_copy)
  #res = t_link.render(Context({'objs': objs_linkable, 'main_obj': main_obj}))
  res = "angekommen"
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

