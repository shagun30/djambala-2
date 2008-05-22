# -*- coding: utf-8 -*-
"""
/dms/pinboard/views_show.py

.. zeigt den Inhalt einer Pinnwand an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.07.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items
from dms.queries        import get_visible_comment_count_by_item_containers

from dms.utils_form     import get_folderish_vars_show

from dms.folder.utils   import get_folder_content
from dms.pinboard.utils import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def pinboard_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_section_view(items, sections, last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/pinboard/section.html')
    #tItem = get_template('app/pinboard/pinboarditem.html')
    tItem = get_template('app/discussboard/discussitem.html')
    content = ''
    unknown = _(u'Beiträge')
    section = '--START--'
    pinitems = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
    for i in items :
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if section != i.section :
        if section != unknown :
          if section != '--START--' and pinitems != [] :
            cSection = Context ( { 'section': section, 'pinitems': pinitems } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          pinitems = []
      if i.item.url_more != '':
        more_items = show_link(i.item.url_more, _(u'Weitere Infos ...'), i.item.url_more_extern,
                               url_class='navLink')
      else:
        more_items = ''
      item_section = Context ({
                              'name'         : i.item.name,
                              'title'        : i.item.title,
                              'text'         : i.item.text,
                              'user_name'    : i.item.string_1,
                              'email'        : i.item.string_2,
                              'date'         : i.get_last_modified(),
                              'image_url'    : i.item.image_url,
                              'image_url_url': i.item.image_url_url,
                              'image_extern' : i.item.image_extern,
                              'last_modified': i.get_last_modified(),
                              'more_infos'   : more_items,
                              'comments'     : comment_counts[i.item.id]
                            })
      pinitems.append(tItem.render(item_section))
    if section != '--START--' and pinitems != []:
      cSection = Context ( { 'section': section, 'pinitems': pinitems } )
      content += tSection.render ( cSection)
    return content, last_modified

  def get_items_view(items):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/pinboard/pinboarditem.html')
    content = ''
    for i in items :
      cSection = Context ({
                            'title': i.item.title,
                            'text' : i.item.text,
                            'name' : i.item.string_1,
                            'email': i.item.string_2,
                            'date' : i.get_last_modified(),
                           })
      content += tSection.render ( cSection)
    return content

  app_name = 'pinboard'
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified=last_modified)
  return render_to_response('app/base_folderish.html', vars)
