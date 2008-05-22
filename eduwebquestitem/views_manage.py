#-*-coding: utf-8 -*-
"""
/dms/eduwebquestitem/views_manage.py

.. enthaelt den View fuer die Management-Ansicht des Webquests
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def eduwebquestitem_manage(request, item_container):
  """ Pflegemodus der Webquests """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/document/'),
                   'info': _(u'Informationsseite')},
                 { 'url' : get_site_url(item_container, 'index.html/add/image/'),
                   'info': _(u'Bild, Foto, Grafik')},
               ]
  add_ons[1] = []
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')},
               ]
  
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/document/'),
                   'info': _(u'Informationsseite')},
                 { 'url' : get_site_url(item_container, 'index.html/add/image/'),
                   'info': _(u'Bild, Foto, Grafik')},
                 { 'url' : get_site_url(item_container, 
                                        'index.html/add/edufileitem/'),
                   'info': _(u'Datei')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edutextitem/'),
                   'info': _(u'Textdokument (aus den Online_lernarchiven)')},
                 { 'url' : get_site_url(item_container, 'index.html/add/edulinkitem/'),
                   'info': _(u'Verweis  (aus den Online_lernarchiven)')},
               ]
  add_ons[1] = [
                 { 'url' : get_site_url(item_container, 
                                        'index.html/add/pool/'),
                   'info': _(u'Materialpool')},
                 { 'url' : get_site_url(item_container, 
                                        'index.html/add/imagethumb/?' + \
                                                        'max_width=120&max_height=80'),
                   'info': _(u'Minibild für Verweise etc.')},
               ]
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = 'eduwebquestitem'
  my_title = _(u'Webquest pflegen')
  my_title_own = _(u'Eigene Ressourcen etc. pflegen')
  dont = { 'navigation_mode': False}

  return do_manage(request, item_container, user_perms, add_ons, app_name,
                   my_title, my_title_own, dont)
