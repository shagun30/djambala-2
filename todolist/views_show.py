# -*- coding: utf-8 -*-
"""
/dms/todolist/views_show.py

.. zeigt den Inhalt einer To-Do-Liste an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.11.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

#from dms.roles          import *
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.utils          import show_link
from dms.utils_form     import get_folderish_vars_show

from dms.folder.utils   import get_folder_content
from dms.todolist.utils import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def todolist_show ( request, item_container ):
  """ zeigt den Inhalt einer To-Do-Liste """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/todolist/section.html')
    t_link = get_template('app/todolist/linkitem.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
    for i in items :
      if section != i.section :
        if section != unknown :
          if section != '--START--' and links != [] :
            cSection = Context ( { 'section': section, 'links': links } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          links = []
      if i.item.url_more != '':
        title_link = show_link(i.item.url_more, i.item.title)
      else:
        title_link = i.item.title
      cSection = Context ({
                            'id'           : i.item.id,
                            'title'        :i.item.title,
                            'text'         : i.item.text,
                            'text_more'    : i.item.text_more,
                            'user_name'    : i.item.string_1,
                            'email'        : i.item.string_2,
                            'date'         : i.get_last_modified(),
                            'image_url'    : i.item.image_url,
                            'image_url_url': i.item.image_url_url,
                            'image_extern' : i.item.image_extern,
                            'last_modified': i.get_last_modified(),
                            'show_item'    : i.get_absolute_url(),
                            'comments'     : comment_counts[i.item.id]
                          })
      links.append(t_link.render(cSection))

    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  app_name = 'todolist'
  items, sections, d_sections = get_folder_content(item_container)
  vars = get_folderish_vars_show(request, item_container, app_name, get_section_view(items, sections),
                                 get_user_support(item_container))
  return render_to_response ( 'app/base_folderish.html', vars )
