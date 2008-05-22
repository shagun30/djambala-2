# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_newitems.py

.. zeigt die Sitemap des aktuellen Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.09.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_new_edu_items

from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link
from dms.roles          import *

from dms.edufolder.utils  import get_user_support
from dms.edufolder.utils  import get_folder_content
from dms.newsboard.utils  import get_folder_content as get_newsboard_content

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edufolder_newitems(request, item_container):
  """ zeigt Eintraege des letzten Monats innerhalb dieses Lernarchivs """

  def get_new_items(item_container, days=30, start=0, length=200):
    """ liefert eine Liste der untergeordneten Lernarchive """
    tSitemap = get_template('app/edufolder/newitems.html')
    path_length = len(item_container.container.path)
    item_containers, count = get_new_edu_items(item_container, days, start, length)
    ret = ''
    s = get_site_url(item_container, '')
    for i in item_containers:
      if i.item.app.is_folderish:
        marker = '[&middot;&middot;]'
      else:
        marker = ''
      ret += '<a href="%s">%s</a> %s / %s<br />\n' % \
             (i.get_absolute_url(), i.item.title, marker, 
              i.last_modified.strftime('%d.%m.%Y'))
    # --- -2, weil ./ nicht zaehlt und von 0 an gerechnet wird
    if start + length > count:
      max = count-2
      next = ''
    else:
      max = start + length
      next = show_link('./?start='+str(start+200), _(u'weiter'),
                       url_class="navLink")
    if start > 0:
      prev = show_link('./?start='+str(start-200), _(u'zurück'),
                       url_class="navLink")
    else:
      prev = ''
    section = Context ( { 'start': start,
                          'max': max,
                          'count': count-1,
                          'prev': prev,
                          'next': next,
                          'links': ret } )
    return tSitemap.render(section)

  app_name = 'edufolder'
  if request.GET.has_key('start'):
    start = int(request.GET['start'])
  else:
    start = 0
  vars = get_folderish_vars_show(request, item_container, app_name, 
             get_new_items(item_container, 30, start, 200),
             get_user_support(item_container, request.user))
  vars['text'] = ''
  vars['title'] = _(u'Aktuelle Beiträge <i>dieses</i> Lernarchivs')
  vars['image_url'] = ''
  vars['slot_right_info'] = ''
  return render_to_response ( 'app/base_folderish.html', vars )
