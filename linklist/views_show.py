# -*- coding: utf-8 -*-
"""
/dms/linklist/views_show.py

.. zeigt den Inhalt eines Linkliste an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.05.2007  Beginn der Arbeit
0.02  30.01.2008  local_menu
"""

from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

#from dms.roles          import *
from dms.text_icons     import SEPERATOR_ICON_GREY
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.utils          import show_link
from dms.utils_form     import get_folderish_vars_show

from dms.folder.utils   import get_folder_content
from dms.linklist.utils import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def linklist_show ( request, item_container ):
  """ zeigt den Inhalt eines Ordners """

  def get_local_menu(local_menu):
    """ liefert das lokale Menue fuer dieser Linkliste """
    if len(local_menu) <= 1:
      return ''
    t_local_menu = get_template('app/linklist/local_menu.html')
    menus = []
    for menu in local_menu:
      ret = ''
      if menus != []:
        ret += ' %s ' % SEPERATOR_ICON_GREY
      ret += show_link(item_container.get_absolute_url() + '#' + menu, menu, url_class='navLink')
      menus.append(ret)
    return t_local_menu.render( Context( {'menus': menus, } ) )

  def get_section_view(items, sections, last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    tSection = get_template('app/linklist/section.html')
    t_link = get_template('app/linklist/linkitem.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
    linklists = []
    local_menu = []
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if section != i.section :
        if section != unknown :
          if section != '--START--' and links != [] :
            cSection = Context ( { 'section': section, 'links': links } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          local_menu.append(section)
          links = []
      if i.item.app.name == 'dmsLinklist':
        linklists.append(show_link(i.get_absolute_url(), i.item.title))
      else:
        if i.item.url_more != '':
          title_link = show_link(i.item.url_more, i.item.title)
        else:
          title_link = i.item.title
        cSection = Context ({
                              'id'           : i.item.id,
                              'link'         : show_link(i.item.url_more, i.item.title,
                                                        url_class="headerLink"),
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
    if linklists != []:
      tSection = get_template('app/folder/section.html')
      cSection = Context ( { 'section': _(u'Weitere Link-Listen'), 'links': linklists } )
      content = tSection.render ( cSection) + content
    return get_local_menu(local_menu) + content, last_modified

  app_name = u'linklist'
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified=last_modified)
  return render_to_response ( 'app/base_folderish.html', vars )
