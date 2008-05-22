# -*- coding: utf-8 -*-
"""
/dms/guestbook/views_show.py

.. zeigt den Inhalt eines Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  03.01.2007  Beginn der Arbeit
0.02  09.05.2007  get_folderish_vars_show
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items

from dms.utils_form     import get_folderish_vars_show

from dms.guestbook.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def guestbook_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_items_view(items, last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/guestbook/guestbookitem.html')
    content = ''
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      cSection = Context ({
                            'title': i.item.title,
                            'text' : i.item.text,
                            'name' : i.item.string_1,
                            'email': i.item.string_2,
                            'date' : i.get_last_modified(),
                           })
      content += tSection.render ( cSection)
    return content, last_modified

  app_name = 'guestbook'
  item = item_container.item
  items = get_folder_filtered_items(item_container, data_mode=True)
  last_modified = item_container.last_modified
  content, last_modified = get_items_view(items, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified=last_modified)
  return render_to_response('app/base_folderish.html', vars)
