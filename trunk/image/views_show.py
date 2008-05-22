# -*- coding: utf-8 -*-
"""
/dms/image/views_show_detail.py

.. zeigt die Beschreibung eines Bildes
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_PATH
from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show

from dms.file.utils     import get_file_size
from dms.image.utils    import get_image_size
from dms.file.utils     import get_file_modification_date
from dms.file.utils     import get_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def image_show(request,item_container):
  """ zeigt die Beschreibung der Datei an """
  app_name = 'image'
  vars = get_item_vars_show(request, item_container, app_name)
  file_path = DOWNLOAD_PATH + item_container.container.path
  file_name = file_path + item_container.item.name
  width, height = get_image_size(file_name)
  p = item_container.container.is_protected()
  vars['size'] = get_file_size(item_container, p)
  vars['width'] = width
  vars['height'] = height
  vars['mtime'] = get_file_modification_date(item_container, _('german'), p)
  vars['link'] = show_link(get_file_url(item_container, p), _(u'Download/Anzeigen'))
  return render_to_response ( 'app/file/base_details.html', vars )
