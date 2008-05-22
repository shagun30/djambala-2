# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_sitemap.py

.. zeigt die Sitemap des aktuellen Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.09.2007  Beginn der Arbeit
0.02  26.09.2007  acl_users werden ausgeschlossen
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_container_sitemap

from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link
#from dms.roles          import *

from dms.edufolder.utils  import get_user_support
from dms.edufolder.utils  import get_folder_content
from dms.newsboard.utils  import get_folder_content as get_newsboard_content

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edufolder_sitemap(request, item_container):
  """ zeigt die Sitemap des Lernarchivs """

  def get_sitemap(item_container, start, length=200):
    """ liefert eine Liste der untergeordneten Lernarchive """
    tSitemap = get_template('app/edufolder/sitemap.html')
    path_length = len(item_container.container.path)
    containers, count = get_container_sitemap(item_container, start, length,
                                              False)
    ret = ''
    s = get_site_url(item_container, '')
    #assert False
    for container in containers:
      p = container.path[path_length:]
      if p != '':
        n = p.count('/')
        space = n * '|&nbsp;&nbsp;&nbsp;' + ' '
        ret += '%s<a href="%s%sindex.html">%s</a><br />\n' % (space, s, p, p)

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

  app_name = u'edufolder'
  if request.GET.has_key('start'):
    start = int(request.GET['start'])
  else:
    start = 0
  vars = get_folderish_vars_show(request, item_container, app_name, 
             get_sitemap(item_container, start),
             get_user_support(item_container, request.user))
  vars['text'] = ''
  vars['title'] = _(u'Sitemap <i>dieses</i> Lernarchivs')
  vars['image_url'] = ''
  vars['slot_right_info'] = ''
  return render_to_response ( 'app/base_folderish.html', vars )
