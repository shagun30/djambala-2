# -*- coding: utf-8 -*-
"""
/dms/pool/views_show.py

.. zeigt den Inhalt eines Materialpools an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.03.2007  Beginn der Arbeit
0.02  18.03.2008  is_file_by_item_container
"""

import string

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms.settings       import MY_DOMAINS
from dms.settings       import DOWNLOAD_URL

from dms.queries        import get_site_url
from dms.queries        import is_file_by_item_container
from dms.queries        import get_parent_container
from dms.queries        import get_role_by_name

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import get_footer_email
from dms.text_icons     import FOLDER_ICON
from dms.text_icons     import NEW_WINDOW_ICON
from dms.text_icons     import FILE_DETAIL
from dms.text_icons     import EXTERN_ICON

from dms.pool.utils     import get_user_support
from dms.folder.utils   import get_folder_content
from dms.file.utils     import get_file_size
from dms.file.utils     import get_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def pool_show(request, item_container):
  """ zeigt den Inhalt eines Materialpools """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/pool/section.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section_exist = False
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
            section_exist = True
          else :
            section = unknown
          links = []
      d = {}
      d['title'] = i.item.title
      d['text'] = i.item.text
      d['text_more'] = i.item.text_more
      if i.item.app.name == 'dmsFile':
        d['size'] = '<br />' + i.item.name + ', ' + get_footer_email(i.item) + ', ' + \
                    smart_unicode(get_file_size(i, i.container.is_protected())) + ' Bytes'
      else:
        d['size'] = ''
      if i.item.app.is_folderish :
        d['folder_icon'] = FOLDER_ICON
      else :
        d['folder_icon'] = ''
      # --- handelt es sich um ein Datei- oder Ordner-Objekt?
      if string.find(i.item.name, '.html') > 0 or is_file_by_item_container(i):
        if i.item.app.name in ['dmsRedirect', 'dmsLinkItem', 'dmsEduLinkItem']:
          d['url'] = i.item.url_more
          if string.find(i.item.url_more, 'http://') >= 0:
            is_my_domain = False
            for domain in MY_DOMAINS:
              if string.find(i.item.url_more, domain) >= 0:
                is_my_domain = True
                break
            if is_my_domain:
              if i.item.url_more_extern:
                d['extern'] = '_extern'
                d['extern_icon'] = NEW_WINDOW_ICON
            else :
              d['extern'] = '_extern'
              d['extern_icon'] = EXTERN_ICON
        elif i.item.app.name in ['dmsFile', 'dmsImage', 'dmsEduFileItem']:
          if i.item.url_more_extern:
            d['extern'] = '_extern'
            d['extern_icon'] = NEW_WINDOW_ICON
          else:
            d['extern'] = ''
            d['extern_icon'] = ''
          d['url'] = get_file_url(i, i.container.is_protected())
        else:
          d['url'] = get_site_url(i, i.item.name)
      else:
        d['url'] = get_site_url(i, 'index.html')
      #if i.item.app.name != 'dmsRedirect':
      #  d['folder_icon'] = FILE_DETAIL % get_site_url(i, i.item.name + '/show/')
      links.append ( d )
    if section != '--START--' and links != []:
      if section == unknown and not section_exist:
        section = ''
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  app_name = 'pool'
  items, sections, d_sections = get_folder_content(item_container)
  vars = get_folderish_vars_show(request, item_container, app_name,
                                 get_section_view(items, sections),
                                 get_user_support(item_container, request.user))
  parent = get_parent_container(item_container.container)
  vars['no_top_main_navigation'] = (parent.min_role_id < get_role_by_name('no_rights').id) or \
                                  item_container.container.nav_name_left.find('webquest') >= 0
  #l = item_container.container.nav_name_left
  #p = parent.nav_name_left
  #assert False
  return render_to_response ( 'app/base_folderish.html', vars )
