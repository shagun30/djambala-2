# -*- coding: utf-8 -*-
"""
/dms/freemind/views_show_detail.py

.. zeigt die Beschreibung einer Datei an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  27.02.2007  Beginn der Arbeit
0.02  05.03.2007  item_comment
0.03  09.05.2007  get_item_vars_show
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_PATH, DOWNLOAD_PROTECTED_PATH
from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show

from dms.freemind.utils   import get_file_size
from dms.freemind.utils   import get_file_modification_date
from dms.file.utils       import get_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def freemind_show(request,item_container):
  """ zeigt die Beschreibung der Datei an """
  app_name = 'freemind'
  vars = get_item_vars_show(request, item_container, app_name)
  p = item_container.container.is_protected()
  vars['size'] = get_file_size(item_container, p)
  vars['mtime'] = get_file_modification_date(item_container, _('german'), p)
  vars['link'] = show_link(get_file_url(item_container, p), _(u'Download/Anzeigen'), True)
  return render_to_response ( 'app/freemind/base_details.html', vars )
