# -*- coding: utf-8 -*-
"""
/dms/exercisefolder/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles        import require_permission
from dms.folder.views_manage_browseable import do_manage_browseable

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def exercisefolder_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  app_types = ['dmsEduFileItem', 'dmsEduLinkItem', 'dmsEduMediaItem', 'dmsEduGalleryItem',
               'dmsEduTextItem', 'dmsEduWebquestItem', 'dmsEduFolder', 'dmsEduScormItem']
  return do_manage_browseable(request, item_container, 'edufolder',
                              _(u'Lernressourcen freischalten/löschen'), app_types )
