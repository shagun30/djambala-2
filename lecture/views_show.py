# -*- coding: utf-8 -*-
"""
/dms/lecture/views_show.py

.. zeigt den Inhalt eines Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2007  Beginn der Arbeit
0.02  09.05.2007  get_folderish_vars_show
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

#from dms.roles          import *
from dms.folder.utils   import get_folder_content
from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_folderish_vars_show

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def lecture_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
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
      links.append(get_link_by_item_container(i))

    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  app_name = 'lecture'
  item = item_container.item
  items, sections, d_sections = get_folder_content(item_container)
  vars = get_folderish_vars_show(request, item_container, app_name, get_section_view(items, sections))
  vars['content_div_style'] = 'frame-main-manage'
  vars['this_site_title'] = item.title
  vars['no_top_main_navigation'] = True
  vars['in_edit_mode'] = True  # obere Navigation ausblenden
  return render_to_response ( 'app/lecture/base.html', vars )
