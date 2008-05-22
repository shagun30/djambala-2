# -*- coding: utf-8 -*-
"""
/dms/lecture/views_show_complete.py

.. zeigt den Inhalt eines Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2007  Beginn der Arbeit
"""

import string

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.utils          import get_folderish_actions
from dms.folder.utils   import get_folder_content
#from dms.roles          import *

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def lecture_show_complete(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_section_view(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    for i in items :
      if string.find ( i.item.name, '.html' ) > 0 :
        n = i.item.app.name
        #assert False
        if i.item.app.name == 'dmsSheet':
          content += '<h3 class="top-border" style="padding-top:0.2em;">' + i.item.title + '</h3>\n'
          if i.item.sub_title != '':
            content += '<h4>' + i.item.sub_title + '</h4>\n'
          content += i.item.text + '\n'
    return content

  app_name = 'lecture'
  items, sections, d_sections = get_folder_content(item_container)
  if request.GET.has_key('show_more') :
    show_more = request.GET['show_more']
  else :
    show_more = False
  try:
    user_perms = UserEditPerms(request.user.username,request.path)
  except:
    user_perms = []
  vars = { 'content_div_style'     : 'frame-main-manage',
           'this_site_title'       : item_container.item.title,
           'site'                  : item_container.container.site,
           'no_top_main_navigation': True,
           'title'                 : item_container.item.title,
           'sub_title'             : item_container.item.sub_title,
           'slot_right_info'       : item_container.item.info_slot_right,
           'action'                : get_folderish_actions(request, user_perms, item_container,
                                                      app_name, False),
           'breadcrumb'            : get_breadcrumb(item_container),
           'path'                  : item_container.container.path,
           'show_more'             : show_more,
           'text'                  : item_container.item.text,
           'text_more'             : item_container.item.text_more,
           'image_url'             : item_container.item.image_url,
           'image_url_url'         : item_container.item.image_url_url,
           'image_extern'          : item_container.item.image_extern,
           'is_wide'               : item_container.item.is_wide,
           'is_important'          : item_container.item.is_important,
           'content'               : get_section_view(items, sections),
           'footer_email'          : get_footer_email(item_container),
           'last_modified'         : item_container.get_last_modified(),
         }
  return render_to_response ( 'app/lecture/base.html', vars )
