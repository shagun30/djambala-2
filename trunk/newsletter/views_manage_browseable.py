# -*- coding: utf-8 -*-
"""
/dms/newsletter/views_manage.py

.. enthaelt den View fuer die Freigabe-Ansicht
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.roles  import *
from dms.folder.views_manage_browseable import do_manage_browseable

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def newsletter_manage_browseable(request, item_container):
  """ Freigabemodus des Newsletters """
  return do_manage_browseable(request, item_container, 'newsletter', 
                              _(u'Einträge freischalten/löschen'),
                              ['dmsNewsletterItem'], '-name' )
