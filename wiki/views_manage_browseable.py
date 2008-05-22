# -*- coding: utf-8 -*-
"""
/dms/wiki/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles  import *
from dms.folder.views_manage_browseable import do_manage_browseable

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def wiki_manage_browseable(request, item_container):
  """ Freigabemodus des wikis """
  return do_manage_browseable(request, item_container, u'wiki', 
                              _(u'Wiki-Seiten freischalten/löschen'),
                              ['dmsWikiItem'], '-name' )
