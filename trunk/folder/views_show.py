# -*- coding: utf-8 -*-
"""
/dms/folder/views_show.py

.. zeigt den Inhalt eines Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  09.05.2007  get_folderish_vars_show
0.03  10.11.2007  is_protected
"""

from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect
from django.views.decorators.vary import vary_on_headers

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_container
from dms.queries        import get_role_by_name

from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_folderish_vars_show

from dms.folder.utils   import get_folder_content
from dms.projectgroup.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@vary_on_headers('Accept-Language')
def folder_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_section_view(items, sections, last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    has_sections = False
    folder_is_protected = item_container.container.is_protected()
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if section != i.section:
        if section != unknown:
          if section != '--START--' and links != [] :
            cSection = Context ( { 'section': section, 'links': links } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
            has_sections = True
          else :
            section = unknown
          links = []
      links.append(get_link_by_item_container(i, folder_is_protected=folder_is_protected))
    if section != '--START--' and links != []:
      if not has_sections:
        section = ''
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content, last_modified

  # --- Soll an eine andere Adresse weitergeleitet werden?
  if item_container.item.string_1 != '':
    return HttpResponseRedirect(item_container.item.string_1)

  app_name = 'folder'
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  if item_container.container.is_protected():
    vars = get_folderish_vars_show(request, item_container, app_name, content,
                                   get_user_support(item_container), last_modified=last_modified)
  else:
    vars = get_folderish_vars_show(request, item_container, app_name, content, last_modified=last_modified)
  parent = get_parent_container(item_container.container)
  vars['no_top_main_navigation'] = (parent.min_role_id < get_role_by_name('no_rights').id) or \
                                  item_container.container.nav_name_left.find('webquest') >= 0
  return render_to_response ( 'app/base_folderish.html', vars )
