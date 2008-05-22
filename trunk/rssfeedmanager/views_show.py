# -*- coding: utf-8 -*-
"""
/dms/rssfeedmanager/views_show.py

.. zeigt die vorhandenen RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.03.2007  Beginn der Arbeit
0.02  04.07.2007  Umstellung auf Folder
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_folderish_vars_show
from dms.folder.utils   import get_folder_content
from dms.feeds          import get_feeds

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def rssfeedmanager_show(request, item_container):
  """ zeigt die enthaltenen RSS-Feeds an """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der vorhandenen RSS-Feeds """
    from django.template.loader import get_template
    from django.template import Context
    section = get_template('app/rssfeed/feed_section.html')
    feeds = get_feeds(2)
    c = Context ( { 'section': _(u'Allgemeine RSS-Feeds'),
                    'feeds'  : feeds,
                  } )
    info = section.render(c)
    feeds = get_feeds(1)
    c = Context ( { 'section': _(u'Spezielle RSS-Feeds'),
                    'feeds'  : feeds,
                  } )
    info += section.render(c)
    return info

  app_name = 'rssfeedmanager'
  items, sections, d_sections = get_folder_content(item_container)
  vars = get_folderish_vars_show(request, item_container, app_name, get_section_view(items, sections))
  return render_to_response ( 'app/base_folderish.html', vars )
