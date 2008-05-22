# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles        import require_permission
from dms.folder.views_manage_browseable import do_manage_browseable

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def edufolder_manage_browseable(request, item_container):
  """ Freigabemodus des Ordners """
  app_types = ['dmsEduFileItem', 'dmsEduLinkItem', 'dmsEduMediaItem', 'dmsEduGalleryItem',
               'dmsEduTextItem', 'dmsEduWebquestItem', 'dmsEduFolder', 'dmsEduScormItem',
               'dmsEduExerciseItem']
  return do_manage_browseable(request, item_container, 'edufolder',
                              _(u'Lernressourcen freischalten/löschen'), app_types )
