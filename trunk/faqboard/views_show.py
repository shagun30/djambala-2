# -*- coding: utf-8 -*-
"""
/dms/faqboard/views_show.py

.. zeigt den Inhalt einer FAQ-Liste an
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
0.02  10.11.2007  is_protected
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items_date_ordered
from dms.queries        import get_visible_comment_count_by_item_containers

from dms.utils_form     import get_folderish_vars_show

from dms.faqboard.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def faqboard_show(request, item_container):
  """ zeigt den Inhalt einer FAQ-Liste """

  def get_section_view(items, sections, last_modified):
    """ erzeugt die Section-Ansicht der in der FAQ-Liste enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
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
          links = []
      if i.item.text_more.strip() == '':
        links.append(get_link_by_item_container(i) + ' - ' + _(u'Ohne Antwort ...'))
      elif comment_counts[i.item.id]:
        links.append(get_link_by_item_container(i) + ' - %s: %i' % \
                     (_(u'Kommentar(e)'), comment_counts[i.item.id]))
      else:
        links.append(get_link_by_item_container(i))
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content, last_modified

  app_name = 'faqboard'
  #item = item_container.item
  #items = get_folder_filtered_items_date_ordered(item_container)
  from dms.utils          import get_link_by_item_container
  from dms.folder.utils   import get_folder_content
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                  get_user_support(item_container), last_modified=last_modified)
  if item_container.item.has_comments:
    vars['comments'] = True
  return render_to_response('app/base_folderish.html', vars)
