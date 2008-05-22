# -*- coding: utf-8 -*-
"""
/dms/webquestitem/views_show.py

.. zeigt den Inhalt des Webquests an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.settings       import MY_DOMAINS
from dms.settings       import DOWNLOAD_URL

from dms.queries        import get_site_url
from dms.queries        import get_data_item_container
from dms.queries        import get_eduitem

from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_item_vars_show

from dms.text_icons     import NEW_WINDOW_ICON
from dms.text_icons     import FILE_DETAIL
from dms.text_icons     import EXTERN_ICON

from dms.webquest.utils  import get_user_support
from dms.webquest.utils  import get_view_mode
from dms.edulinkitem.views_show import get_details

from dms.folder.utils     import get_folder_content
from dms.newsboard.utils  import get_folder_content as get_newsboard_content
from dms.views_comment  import item_comment

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def webquest_show(request, item_container):
  """ 
  zeigt den Inhalt eines Webquests
  !! siehe auch check_visual_effects in utils_form !!
  """

  def get_section_view_pool(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    tSection = get_template('app/eduwebquestitem/section_pool.html')
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
      d = {}
      d['title'] = i.item.title
      d['text'] = i.item.text
      d['text_more'] = i.item.text_more
      # --- handelt es sich um ein Datei- oder Ordner-Objekt?
      if i.item.name.find('.html') > 0 or \
        (i.item.app.name == 'dmsFile') or (i.item.app.name == 'dmsImage'):
        if i.item.app.name in ['dmsRedirect', 'dmsLinkItem', 'dmsEduLinkItem']:
          d['url'] = i.item.url_more
          if i.item.url_more.find('http://') >= 0:
            is_my_domain = False
            for domain in MY_DOMAINS:
              if i.item.url_more.find(domain) >= 0:
                is_my_domain = True
                break
            if is_my_domain:
              if i.item.url_more_extern:
                d['extern'] = '_extern'
                d['extern_icon'] = NEW_WINDOW_ICON
            else :
              d['extern'] = '_extern'
              d['extern_icon'] = EXTERN_ICON
        elif i.item.app.name in ['dmsFile', 'dmsImage', 'dmsEduTextItem', 'dmsEduFileItem']:
          d['extern'] = '_extern'
          d['extern_icon'] = NEW_WINDOW_ICON
          d['folder_icon'] = FILE_DETAIL % get_site_url(i, i.item.name + '/show/')
          d['url'] = DOWNLOAD_URL + i.container.path + i.item.name
        else:
          d['url'] = get_site_url(i, i.item.name)
      else:
        d['url'] = get_site_url(i, 'index.html')
      links.append(d)
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  def get_section_view(item_containers, sections):
    """ erzeugt die Uebersichsseite des Webquest """
    tSection = get_template('app/eduwebquestitem/section.html')
    content = ''
    for i in item_containers:
      if i.item.app.name == 'dmsDocument':
        context = Context ( {'title': i.item.title,
                             'sub_title': i.item.sub_title,
                             'text': i.item.text, } )
        content += tSection.render(context)
      elif i.item.app.name == 'dmsPool':
        pool_item_containers, sec, d_sec = get_folder_content(i)
        pool_text = get_section_view_pool(pool_item_containers,
                                          i.container.sections)
        if pool_text != '':
          context = Context ( {'title': i.item.title,
                               'sub_title': i.item.sub_title,
                               'text': pool_text, } )
          content += tSection.render(context)
    return content

  def get_section_view_webquest(item_containers, sections):
    """ erzeugt die Webquest-Ansicht """
    content = ''
    return content

  app_name = 'webquestitem'
  # --- Detail-Ansicht
  if request.GET.has_key('show_details'):
    vars = get_item_vars_show(request, item_container, app_name,
                              ignore_own_breadcrumb=True)
    data = get_eduitem(item_container.item)
    vars['text_more'] += get_details(item_container, True, data)
    if item_container.item.has_comments:
      comments = item_comment(request, item_container=item_container)
    else:
      comments = ''
    vars['comments'] = comments
    return render_to_response ( 'base-full-width.html', vars )

  # --- Objekte des Webquest zeigen
  item_containers, sections, d_sections = get_folder_content(item_container)
  if request.GET.has_key('view_mode'):
    view_mode = 'complete'
    my_view = get_section_view(item_containers, sections)
  else:
    view_mode = ''
    my_view = get_section_view_webquest(item_containers, sections)
  vars = get_folderish_vars_show(request, item_container, app_name,
            my_view,
            get_user_support(item_container, request.user.is_authenticated()))
  vars['view_options'] = get_view_mode(item_container, view_mode)
  vars['no_top_main_navigation'] = True
  return render_to_response ( 'app/base_folderish.html', vars )
