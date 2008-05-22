# -*- coding: utf-8 -*-
"""
/dms/photo/views_show.py

.. zeigt den Inhalt eines Photos an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.10.2007  Beginn der Arbeit
0.02  31.10.2007  Anzeige des Bildes
"""

from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment
from dms.file.utils     import get_file_url
from dms.gallery.utils  import get_exibition_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def photo_show(request,item_container):
  """ zeigt den Inhalt eines Photos """

  def get_photo_name_middle(item_container):
    """ ..liefert die Namen der normalen Bilder """
    file_name = get_file_url(item_container)
    ext_pos = file_name.rfind('.')
    return file_name[:ext_pos] + '_middle' + file_name[ext_pos:]

  app_name = 'photo'
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars = get_item_vars_show(request, item_container, app_name)
  vars['comments'] = comments
  vars['image_url'] = get_photo_name_middle(item_container)
  vars['image_url_big'] = show_link(get_file_url(item_container), _(u'Originalphoto'), True)
  tItem = get_template('app/photo/show_photo.html')
  vars['full_name'] = item_container.item.string_1
  vars['email'] = item_container.item.string_2
  vars['exibition_url'] = get_exibition_url(item_container)
  vars['name'] = item_container.item.name
  vars['text_more'] = tItem.render(Context(vars))
  vars['text'] = ''
  vars['image_url'] = ''
  return render_to_response ( 'base-full-width.html', vars )
