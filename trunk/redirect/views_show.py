# -*- coding: utf-8 -*-
"""
/dms/redirect/views_show.py

.. zeigt den Inhalt einer Weiterleitung an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.01.2007  Beginn der Arbeit
"""

import string

from django.http import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def redirect_show(request, item_container):
  """ zeigt den Inhalt der Weiterleitung """
  if string.find(item_container.item.url_more, 'http://') < 0:
    site = item_container.container.site
    path = item_container.container.path + item_container.item.url_more
    length=len(site.base_folder)
    if length < len(path):
      url = site.url + path[length:]
    else :
      url = site.url + '/'
  else:
    url  = item_container.item.url_more
  return HttpResponseRedirect(url)
