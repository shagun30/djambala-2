# -*- coding: utf-8 -*-
"""
/dms/projectgroupemail/views_show.py

.. zeigt den Inhalt eines Rundschreibens an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.01.2008  Beginn der Arbeit
0.02  05.02.2008  Entschlackung
"""

import StringIO

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from django.template.loader   import get_template
from django.template          import Context

from dms.queries        import get_folder_filtered_items_date_ordered
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_site_url
from dms.queries        import get_user
from dms.queries        import get_user_by_username
from dms.queries        import get_item_container_by_path_and_name

from dms.settings       import CONTROL_EMAIL

from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_base_vars

from dms.projectgroupemail.utils   import get_user_support
from dms.newsletter.utils   import remove_html

from dms.utils          import get_link_by_item_container

from dms.folder.utils   import get_folder_content

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_section_view(items, sections):
  """ erzeugt die Section-Ansicht der im Rundschreiben enthaltenen Objekte """
  # Hilfsfunktion fuer projectgroupemail_show und projectgroupemail_send
  tSection = get_template('app/folder/section.html')
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
    if comment_counts[i.item.id]:
      links.append(get_link_by_item_container(i) + ' - %s: %i' % \
                    (_(u'Kommentar(e)'), comment_counts[i.item.id]))
    else:
      links.append(get_link_by_item_container(i))
  if section != '--START--' and links != []:
    cSection = Context ( { 'section': section, 'links': links } )
    content += tSection.render ( cSection)
  return content

# -----------------------------------------------------
def projectgroupemail_show(request, item_container):
  """ zeigt die vorhandenen Rundschreiben """
  app_name = 'projectgroupemail'
  items, sections, d_sections = get_folder_content(item_container)
  if item_container.container.is_protected():
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_section_view(items, sections),
                                   get_user_support(item_container))
  else:
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_section_view(items, sections))
  if item_container.item.has_comments:
    vars['comments'] = True
  return render_to_response('app/base_folderish.html', vars)
