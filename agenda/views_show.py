# -*- coding: utf-8 -*-
"""
/dms/agenda/views_show.py

.. zeigt den Inhalt eines Terminplaners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2008  Uebernahme von Folder
"""

from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect
from django.views.decorators.vary import vary_on_headers

from django.utils.translation import ugettext as _

from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_folderish_vars_show

from dms.folder.utils   import get_folder_content
from dms.projectgroup.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@vary_on_headers('Accept-Language')
def agenda_show(request, item_container):
  """ zeigt den Inhalt eines Terminplaners """

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

  # --- Soll an eine andere Adresse weitergeleitet werden?
  if item_container.item.string_1 != '':
    return HttpResponseRedirect(item_container.item.string_1)

  app_name = 'agenda'
  items, sections, d_sections = get_folder_content(item_container)
  if item_container.container.is_protected():
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_section_view(items, sections),
                                   get_user_support(item_container))
  else:
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_section_view(items, sections))
  return render_to_response ( 'app/base_folderish.html', vars )
