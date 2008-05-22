# -*- coding: utf-8 -*-
"""
/dms/gallery/views_show.py

.. zeigt den Inhalt einer Galerie an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.10.2007  Beginn der Arbeit
0.02  01.11.2007  Zur Ausstellung
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_site_url

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import show_link

from dms.folder.utils   import get_folder_content
from dms.file.utils     import get_file_url
from dms.gallery.utils  import get_user_support
from dms.gallery.utils  import get_exibition_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def gallery_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_photo_name_small(item_container):
    """ ..liefert die Namen der verkleinerten Bilder """
    file_name = get_file_url(item_container)
    ext_pos = file_name.rfind('.')
    file_name_small = file_name[:ext_pos] + '_small' + file_name[ext_pos:]
    return file_name_small

  def get_section_view(items, sections,last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/gallery/section.html')
    tItem = get_template('app/gallery/photo.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    photos = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if section != i.section :
        if section != unknown :
          if section != '--START--' and photos != [] :
            cSection = Context ( { 'section': section, 'photos': photos } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          photos = []
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
                              'image_url'    : get_photo_name_small(i),
                              'image_url_url': i.item.image_url_url,
                              'image_extern' : i.item.image_extern,
                              'exbition_url' : get_exibition_url(item_container),
                              'last_modified': i.get_last_modified(),
                              'more_infos'   : more_items,
                              'comments'     : comment_counts[i.item.id]
                            })
      photos.append(tItem.render(item_section))
    if section != '--START--' and photos != []:
      cSection = Context ( { 'section': section, 'photos': photos } )
      content += tSection.render ( cSection)
    return content, last_modified

  def get_items_view(items):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/gallery/photo.html')
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

  app_name = 'gallery'
  items, sections, d_sections = get_folder_content(item_container)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified)
  link = show_link(get_exibition_url(item_container), _(u'Zur Ausstellung'), True)
  vars['text'] = vars['text'] + '\n<p">\n%s</p>\n' % link
  return render_to_response('app/base_folderish.html', vars)
