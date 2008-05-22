# -*- coding: utf-8 -*-
"""
/dms/wiki/views_show.py

.. zeigt den Inhalt eines Wikis an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

integer_1 = Rolle zum Ergaenzen und Aendern der Wiki-Seiten

0.01  09.02.2008  Beginn der Arbeit
0.02  18.03.2008  Beruecksichtigung der Rolle bei der Anzeige
0.03  21.03.2008  Anzeige der Sitemap
"""

from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items_date_ordered
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_item_container_child_by_name
from dms.queries        import get_role_by_user_path
from dms.queries        import get_folder_items
from dms.queries        import get_base_site_url
from dms.queries        import get_user_by_id

from dms.utils          import get_link_by_item_container
from dms.file.utils     import get_file_url
from dms.folder.utils   import get_folder_content
from dms.utils          import get_footer_email
from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link

from dms.wiki.queries   import get_page_versions
from dms.wiki.utils     import get_user_support
from dms.wiki.utils     import check_wiki_urls
from dms.diff           import textDiff

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def show_pages(item_container):
  """ zeigt die Wiki-Seiten des Wikis """
  if not item_container.item.app.is_folderish and item_container.parent_item_id != -1:
    item_container = item_container.get_parent()
  url = item_container.get_absolute_url()
  items = get_folder_items(item_container, 'name')
  has_user_folder = False
  objs = []
  for item_container in items :
    if (not item_container.item.app.is_folderish):
      obj = {}
      obj['id'] = item_container.item.id
      obj['title'] = item_container.item.title
      obj['app_name'] = item_container.item.app.name
      obj['is_folderish'] = item_container.item.app.is_folderish
      obj['url']  = item_container.get_absolute_url()
      obj['name'] = item_container.item.name
      obj['app_description'] = item_container.item.app.description
      obj['last_modified'] = item_container.last_modified.strftime ( '%d.%m.%Y %H:%M' )
      obj['is_deleted'] = item_container.is_deleted
      objs.append ( obj )

  vars = { 'content_div_style': 'frame-util-images',
           'objs'             : objs,
           'item'             : item_container.item,
           'site'             : item_container.container.site,
           'title'            : _('Alle Seiten dieses Wikis'),
           'this_style'       : item_container.container.site.skin_style,
           'footer_email'     : get_footer_email(item_container.item),
           'last_modified'    : item_container.get_last_modified()
         }
  return render_to_response ( 'app/wiki/show_pages.html', vars )

# -----------------------------------------------------
def show_sitemap(request, item_container):
  """ zeigt die Wki-Seiten des Wikis (im Sinne einer Sitemap) """
  if not item_container.item.app.is_folderish and item_container.parent_item_id != -1:
    item_container = item_container.get_parent()
  url = item_container.get_absolute_url()
  item_containers = get_folder_items(item_container, 'name')
  has_user_folder = False
  objs = []
  for ic in item_containers :
    if (not ic.item.app.is_folderish):
      app_name = ic.item.app.name
      obj = {}
      obj['id'] = ic.item.id
      obj['is_wiki'] = app_name == 'dmsWikiItem'
      obj['title'] = ic.item.title
      obj['url'] = ic.get_absolute_url()
      obj['image_url'] = get_file_url(ic)
      obj['app_name'] = ic.item.app.name
      name = ic.item.name
      obj['name'] = name
      obj['wiki_page'] = name[:name.rfind('.html')]
      obj['last_modified'] = ic.last_modified.strftime('%m/%d/%Y %H:%M' )
      objs.append ( obj )

  app_name = 'wiki'
  dont_show = { 'no_sitemap': True, 'no_version': True, 'no_edit': True, 'no_new_items': True}
  vars = get_folderish_vars_show(request, item_container, app_name, '',
                                  get_user_support(item_container, 'start', dont_show))
  if item_container.item.has_comments:
    vars['comments'] = True
  vars['text'] = ''
  vars['image_url'] = ''
  vars['slot_right_info'] = ''
  vars['user_support_header'] = _(u'Mögliche Aktionen')
  vars['sub_title'] = _(u'Übersicht aller Wiki-Seiten')
  vars['objs'] = objs
  vars['site_url'] = get_base_site_url()
  return render_to_response ( 'app/wiki/show_sitemap.html', vars )

# -----------------------------------------------------
def wiki_show(request, item_container):
  """ zeigt den Inhalt eines Wiks """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der in der FAQ-Liste enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    content = ''
    unknown = _(u'Weitere Wikis')
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
      links.append(get_link_by_item_container(i))
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  app_name = 'wiki'
  if request.GET.has_key('show_all_pages'):
    return show_pages(item_container)
  elif request.GET.has_key('show_sitemap'):
    return show_sitemap(request, item_container)
  elif request.GET.has_key('wiki_page'):
    wiki_page = request.GET['wiki_page']
  else:
    wiki_page = 'start'
  this_page = get_item_container_child_by_name(item_container, wiki_page + '.html')
  my_role = get_role_by_user_path(request.user, item_container.container.path)
  if this_page == None:
    if my_role <= item_container.item.integer_1:
      url = item_container.get_absolute_url() + '/add/wikiitem/?wiki_page=' + wiki_page
      return HttpResponseRedirect(url)
    else:
      wiki = {}
  else:
    wiki = { 'title': this_page.item.title,
             'sub_title': this_page.item.sub_title,
             'page': check_wiki_urls(item_container, this_page.item.text, my_role),
             'image_url': this_page.item.image_url,
             'image_url_url': this_page.item.image_url_url,
             'image_extern': this_page.item.image_extern,
           }
  items, sections, d_sections = get_folder_content(item_container, app_types=['dmsWiki'])
  vars = get_folderish_vars_show(request, item_container, app_name,
                                  get_section_view(items, sections),
                                  get_user_support(item_container, wiki_page))
  if item_container.item.has_comments:
    vars['comments'] = True
  vars['wiki'] = wiki
  vars['user_support_header'] = _(u'Mögliche Aktionen')
  # Intro nur auf der Startseite
  if wiki_page != 'start':
    vars['text'] = ''
    vars['image_url'] = ''
  return render_to_response('app/wiki/show_wiki.html', vars)