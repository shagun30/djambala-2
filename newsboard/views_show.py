# -*- coding: utf-8 -*-
"""
/dms/newsboard/views_show.py

.. zeigt den Inhalt eines Nachrichtenbretts an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.03.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_visible_comment_count_by_item_containers
from dms.utils          import show_link
from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_folderish_vars_show

from dms.newsboard.utils   import get_folder_content
from dms.newsboard.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def newsboard_show ( request, item_container ):
  """ zeigt den Inhalt eines Ordners """

  def get_items_view(last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    t_section = get_template('app/newsboard/newsitem.html')
    t_section_old = get_template('app/newsboard/newsitem-old.html')
    t_archives = get_template('app/archives.html')
    content = ''
    if item_container.item.name.find('archiv') == 0:
      items = get_folder_content(item_container, 'all')
      items_old_dist = []
    else:
      items = get_folder_content(item_container, 'new')
      items_old_dist = get_folder_content(item_container, 'old')
    items_old = []
    for i in items_old_dist:
      if i.item.app.name == 'dmsNewsItem':
        items_old.append(i)
    archives = []
    comment_counts = get_visible_comment_count_by_item_containers(items)
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if i.item.url_more != '':
        more_items = show_link(i.item.url_more, _(u'Weitere Infos ...'), i.item.url_more_extern,
                               url_class='navLink')
      else:
        more_items = ''
      if i.item.app.name == 'dmsNewsboard':
        archives.append(show_link(i.get_absolute_url(), i.item.title))
      else:
        cSection = Context ({
                              'name'         : i.item.name,
                              'title'        : i.item.title,
                              'sub_title'    : i.item.sub_title,
                              'text'         : i.item.text,
                              'user_name'    : i.item.string_1,
                              'email'        : i.item.string_2,
                              'date'         : i.get_last_modified(),
                              'image_url'    : i.item.image_url,
                              'image_url_url': i.item.image_url_url,
                              'image_extern' : i.item.image_extern,
                              'last_modified': i.get_last_modified(),
                              'more_infos'   : more_items,
                              'comments'     : comment_counts[i.item.id]
                            })
        content += t_section.render(cSection)
    if items_old != [] or archives != []:
      if archives != []:
        archiv_txt = t_archives.render( Context({'title': _(u'Nachrichtenarchiv(e)'),
                                                  'archives': archives}) )
      else:
        archiv_txt = ''
      cSection = Context ({ 'items_old': items_old, 'archives': archiv_txt, })
      content += t_section_old.render(cSection)
    return content, last_modified

  app_name = 'newsboard'
  last_modified = item_container.last_modified
  content, last_modified = get_items_view(last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container), last_modified=last_modified)
  if item_container.item.has_comments:
    vars['comments'] = True
  return render_to_response ( 'app/base_folderish.html', vars )
