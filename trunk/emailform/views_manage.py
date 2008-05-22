# -*- coding: utf-8 -*-
"""
/dms/emailform/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.01.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
from dms.folder.views_manage  import do_manage

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def emailform_manage(request, item_container):
  """ Pflegemodus des E-Mail-Formulars """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/emailitem/?form_type=input'),
                   'info': _(u'Einzeiliges Antwortfeld')},
                 { 'url' : get_site_url(item_container, 'index.html/add/emailitem/?form_type=text'),
                   'info': _(u'Mehrzeiliges Antwortfeld')},
                 { 'url' : get_site_url(item_container, 'index.html/add/emailitem/?form_type=radio'),
                   'info': _(u'Einzelnes Auswahlfeld ("Radio-Button")')},
                 { 'url' : get_site_url(item_container, 'index.html/add/emailitem/?form_type=checkbox'),
                   'info': _(u'Mehrfaches Auswahlfeld ("Checkbox")')},
               ]
  add_ons[1] = []
  add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
                   'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[3] = []

  app_name = 'emailform'
  my_title = _(u'E-Mail-Formular pflegen')
  my_title_own = ''

  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, 
                   my_title_own)
