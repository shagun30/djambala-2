#-*-coding: utf-8 -*-
"""
/dms/edufolder/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edufolder_manage(request, item_container):
  """ Pflegemodus des Lernarchivs """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/edufolder/'),
                   'info': _(u'Online-Lernarchiv')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edulinkitem/'),
                   'info': _(u'Verweis auf Lernressource')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edufileitem/'),
                   'info': _(u'Datei')},
                 { 'url' : get_site_url(item_container, 'index.html/add/eduexerciseitem/'),
                   'info': _(u'Aufgabe')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edugalleryitem/'),
                   'info': _(u'Galerie')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edumediaitem/'),
                   'info': _(u'Medienpaket')},
                 { 'url' : get_site_url(item_container, 'index.html/add/eduscormitem/'),
                   'info': _(u'Scorm/Content-Package (CP)')},
                 { 'url' : get_site_url(item_container, 'index.html/add/redirect/'),
                   'info': _(u'"Siehe auch"-Hinweis auf anderes Lernarchiv')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edutextitem/'),
                   'info': _(u'Textdokument')},
                 { 'url' : get_site_url(item_container, 'index.html/add/eduwebquestitem/'),
                   'info': _(u'Webquest')},
               ]
  add_ons[1] = [
                 { 'url' : get_site_url(item_container,
                               'index.html/add/imagethumb/?max_width=120&max_height=80'),
                   'info': _(u'Minibild für Verweise etc.')},
                 { 'url' : get_site_url(item_container, 'index.html/add/image/'),
                   'info': _(u'Bild, Foto, Grafik')},
                 { 'url' : get_site_url(item_container, 'index.html/add/newsboard/'),
                   'info': _(u'Nachrichtenbrett')},
               ]
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = [ { 'url' : get_site_url(item_container, 'index.html/add/exercisefolder/'),
                   'info': _(u'Aufgaben-Datenbank')},
                 { 'url' : get_site_url(item_container, 'index.html/add/newsletter/'),
                   'info': _(u'Newsletter')}, ]

  app_name = u'edufolder'
  my_title = _(u'Online-Lernarchiv pflegen')
  my_title_own = _(u'Eigene Ressourcen etc. pflegen')

  return do_manage(request, item_container, user_perms, add_ons, app_name,
                   my_title, my_title_own, allow_copy=False)
