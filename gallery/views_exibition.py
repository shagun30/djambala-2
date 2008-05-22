# -*- coding: utf-8 -*-
"""
/dms/gallery/views_exibition.py

.. zeigt den Inhalt einer Galerie an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.11.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _

from dms.queries        import get_folder_filtered_items
from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_site_url
from dms.queries        import get_item_container_by_path_and_name
from dms.queries        import get_visible_comment_count_by_item_containers

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import show_link

from dms.folder.utils   import get_folder_content
from dms.gallery.utils  import get_user_support
from dms.file.utils     import get_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def gallery_exibition(request, item_container):
  """ zeigt den Inhalt der Galerie als Ausstellung an """

  def get_photo_name_middle(item_container):
    """ ..liefert die Namen der verkleinerten Bilder """
    file_name = get_file_url(item_container)
    ext_pos = file_name.rfind('.')
    file_name_small = file_name[:ext_pos] + '_middle' + file_name[ext_pos:]
    return file_name_small

  def get_color(color):
    if color < 0 : color = 0
    if color > 10: color = 10
    h = 3*hex(int(25.5*color))[2:]
    return '#%s' % h

  def get_prev_next(item_containers, this_name):
    """ liefert Vorgaenger und Nachfolger """
    if len(item_containers) == 0:
      return '', '', '', ''
    else:
      first = item_containers[0].item.name
      last = item_containers[len(item_containers)-1].item.name
      n_curr = 0
      while n_curr < len(item_containers) and item_containers[n_curr].item.name != this_name:
        n_curr += 1
      if n_curr > 0:
        prev = item_containers[n_curr-1].item.name
      else:
        prev = ''
      if n_curr < len(item_containers)-1:
        next = item_containers[n_curr+1].item.name
      else:
        next = ''
      return first, prev, next, last

  app_name = 'gallery'
  item_containers = get_folder_filtered_items(item_container, False, ['dmsPhoto'])
  if request.GET.has_key('image'):
    this_name = request.GET['image']
  elif len(item_containers) > 0:
    this_name = item_containers[0].item.name
  else:
    this_name = ''
  t_image = get_template('app/photo/exibition_image.html')
  first, prev, next, last = get_prev_next(item_containers, this_name)
  if first != '':
    url_pattern = item_container.get_absolute_url() + '/exibition/?image='
    first_url = url_pattern + first
    if prev != '':
      prev_url = url_pattern + prev
    else:
      prev_url = ''
    if next != '':
      next_url = url_pattern + next
    else:
      next_url = ''
    last_url = url_pattern + last
    this_ic = get_item_container_by_path_and_name(item_container.container.path, this_name)
    comment_counts = get_visible_comment_count_by_item_containers(item_containers)
    c_image = Context ({
                        'name'          : this_name,
                        'title'         : this_ic.item.title,
                        'text'          : this_ic.item.text,
                        'text_more'     : this_ic.item.text_more,
                        'first_url'     : first_url,
                        'prev_url'      : prev_url,
                        'next_url'      : next_url,
                        'last_url'      : last_url,
                        'date'          : this_ic.get_last_modified(),
                        'image_url'     : get_photo_name_middle(this_ic),
                        'section'       : this_ic.section,
                        'last_modified' : this_ic.get_last_modified(),
                        'comments'      : comment_counts[this_ic.item.id],
                      })
    vars = get_folderish_vars_show(request, item_container, app_name, t_image.render(c_image),
                                  get_user_support(item_container))
  else:
    first_url = ''
    prev_url = ''
    next_url = ''
    last_url = ''
    this_image = Context ({
                            'name'          : '',
                            'title'         : _(u'Die Ausstellung ist noch nicht geöffnet!'),
                          })
    vars = get_folderish_vars_show(request, item_container, app_name, t_image.render(this_image),
                                  get_user_support(item_container))
  vars['no_breadcrum'] = True
  color = int(item_container.item.string_2)
  vars['bg_color'] = get_color(color)
  if color < 4:
    vars['text_color'] = get_color(10)
  else:
    vars['text_color'] = get_color(0)
  return render_to_response('app/gallery/exibition.html', vars)
