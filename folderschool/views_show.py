# -*- coding: utf-8 -*-
"""
/dms/folderschool/views_show.py

.. zeigt den Inhalt eines Basisordners fuer Schulen an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.roles                import UserEditPerms
from dms.queries              import get_site_url
from dms.queries              import is_file_by_item_container
from dms.utils                import get_link_by_item_container
from dms.utils_form           import get_folderish_vars_show

from dms.encode_decode  import encode_html
from dms.folder.utils   import get_folder_content
from dms.folderschool.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def folderschool_show ( request, item_container ):
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
    folder_is_protected = item_container.container.is_protected()
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
      if is_file_by_item_container(i):
        user_perms = UserEditPerms(request.user.username, request.path)
        if user_perms.perm_read:
          links.append(get_link_by_item_container(i, folder_is_protected=folder_is_protected))
        else:
          links.append(i.item.title)
      else:
        links.append(get_link_by_item_container(i, folder_is_protected=folder_is_protected))
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content, last_modified

  if request.GET.has_key('section'):
    section = request.GET['section']
  else:
    section = ''
  app_name = 'folderschool'
  items, sections, d_sections = get_folder_content(item_container, this_section=section)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified=last_modified)
  vars['ajax_url'] = get_site_url(item_container, 'index.html/ajax/')
  vars['title'] = vars['sub_title'] = ''
  return render_to_response ( 'app/folderschool/base_folderish.html', vars )

