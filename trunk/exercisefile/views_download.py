# -*- coding: utf-8 -*-
"""
/dms/exercisefile/views_download.py

.. enthaelt den View zum Aendern der Eigenschaften einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.05.2008  Beginn der Arbeit
"""

import os, mimetypes
from django.http        import HttpResponse
from django.core.servers.basehttp import FileWrapper

from django.utils.translation import ugettext as _

from dms.roles          import UserEditPerms
from dms.roles          import has_permission

from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_PROTECTED_PATH
from dms.views_error    import show_error

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

class FileWrapperModified(FileWrapper):
  """ http://code.djangoproject.com/ticket/6027 """
  def __iter__(self):
    self.filelike.seek(0)
    return self

# -----------------------------------------------------
def send_file(filepath, filename):
  """ 
  send a file through Django - the FileWrapper will turn the file object into an iterator for chunks of 8KB
  http://www.djangosnippets.org/snippets/365/
  """
  mimetype, encoding = mimetypes.guess_type(filename)
  wrapper = FileWrapperModified(file(filepath))
  response = HttpResponse(wrapper, content_type=mimetype)
  response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
  response['Content-Length'] = os.path.getsize(filepath)
  response['Content-Disposition'] = 'attachment; filename=%s' % filename
  #f = open(filepath, 'rb')
  #content = f.read()
  #f.close()
  #response = HttpResponse(content, content_type=mimetype)
  ## IE-Problem: http://forum.de.selfhtml.org/2006/11/t140933/
  #response['Cache-Control'] = 'must-revalidate, max-age=0'
  #response['Content-Length'] = os.path.getsize(filepath)
  #response['Content-Disposition'] = 'attachment; filename=%s' % filename
  return response

# -----------------------------------------------------
def exercisefile_download(request, item_container):
  """ Vorbereitungen zum Senden einer geschuetzten Datei """
  is_teacher = has_permission(request.user, item_container.container.path, 'perm_manage_folderish')
  if is_teacher or item_container.owner == request.user:
    filename = DOWNLOAD_PROTECTED_PATH + item_container.container.path + item_container.item.name
    return send_file(filename, item_container.item.name)
  else:
    return show_error(request, item_container, _('Zugriffsrecht'),
                      _(u'<p>Nur die Lehrkraft darf alle Lösungen anschauen!</p>'))
