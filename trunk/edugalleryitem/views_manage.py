#-*-coding: utf-8 -*-
"""
/dms/edugalleryitem/views_manage.py

.. enthaelt den View fuer die Management-Ansicht der Edu-Galerie
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edugalleryitem_manage(request, item_container):
  """ Pflegemodus des Medienpakets """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/photo/'),
                   'info': _(u'Photo/Grafik')}, ]
  add_ons[1] = []
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = u'edugallery'
  my_title = _(u'Galerie pflegen')
  my_title_own = ''
  dont = { 'navigation_left_mode': False, }

  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, 
                   my_title_own, dont)
