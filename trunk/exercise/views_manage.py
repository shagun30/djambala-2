#-*-coding: utf-8 -*-
"""
/dms/exercise/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def exercise_manage(request, item_container):
  """ Pflegemodus des Ordners """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/image/'),
                   'info': _(u'Bild, Foto, Grafik')},
                 { 'url' : get_site_url(item_container, 'index.html/add/file/'),
                   'info': _(u'Datei (z.B. Word-Dokument, PDF-Datei)')},
                 { 'url' : get_site_url(item_container, 'index.html/add/document/'),
                   'info': _(u'Informationsseite für kürzere Texte')},
                 { 'url' : get_site_url(item_container, 'index.html/add/redirect/'),
                   'info': _(u'Verweis auf eine andere Web-Adresse')}, ]
  add_ons[1] = []
  add_ons[2] = []
  add_ons[3] = []

  app_name = 'exercise'
  my_title = _(u'Aufgabe pflegen')
  my_title_own = _(u'Eigene Dateien, Bilder etc. pflegen')
  dont = { 'sort_mode': False, 'navigation_mode': False, 'browseable_mode': False,
           'empty_mode': False, 'search_mode': False}
  return do_manage(request, item_container, user_perms, add_ons,
                   app_name, my_title, my_title_own, dont=dont)
