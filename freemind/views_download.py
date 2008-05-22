# -*- coding: utf-8 -*-
"""
/dms/freemind/views_download.py

.. enthaelt den View zum Aendern der Eigenschaften einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.03.2008  Beginn der Arbeit
"""

import os, mimetypes
from django.http        import HttpResponse
from django.core.servers.basehttp import FileWrapper

from django.utils.translation import ugettext as _

from dms.roles          import UserEditPerms
from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_PROTECTED_PATH
from dms.views_error    import show_error

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

class FileWrapperModified(FileWrapper):
  """ http://code.djangoproject.com/ticket/6027 """
  def __iter__(self):
    self.filelike.seek(0)
    return self

# -----------------------------------------------------
def send_file(filepath, filename, mimetype):
  """ 
  send a file through Django - the FileWrapper will turn the file object into an iterator for chunks of 8KB
  http://www.djangosnippets.org/snippets/365/
  """
  wrapper = FileWrapperModified(file(filepath))
  response = HttpResponse(wrapper, content_type=mimetype)
  response['Content-Length'] = os.path.getsize(filepath)
  response['Content-Disposition'] = 'attachment; filename=%s' % filename
  #f = open(filepath, 'rb')
  #content = f.read()
  #f.close()
  #response = HttpResponse(content, content_type=mimetype)
  #response['Content-Length'] = os.path.getsize(filepath)
  #response['Content-Disposition'] = 'attachment; filename=%s' % filename
  return response

# -----------------------------------------------------
def freemind_download(request, item_container):
  """ Vorbereitungen zum Senden einer geschuetzten Datei """
  user_perms = UserEditPerms(request.user.username, item_container.container.path)
  if user_perms.perm_read:
    filename = DOWNLOAD_PROTECTED_PATH + item_container.container.path + item_container.item.name + \
               '/this.mm'
    mimetype, encoding = mimetypes.guess_type(filename)
    return send_file(filename, item_container.item.name, mimetype)
  else:
    return show_error(request, item_container, _('Zugriffsrecht'),
                      _(u'<p>Sie sind zwar eingeloggt - Ihre Zugriffsrechte sind aber zu gering!</p>'))
