# -*- coding: utf-8 -*-
"""
/dms/wikiitem/views_show.py

.. zeigt den Inhalt einer Wiki-Seite an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.03.2008  Beginn der Arbeit
0.02  18.03.2008  check_wiki_urls
0.03  20.03.2008  wikiitem_diff
0.03  21.03.2008  Urheber der Aenderungen werden angezeigt
0.04  07.05.2008  diff wird jeweils gegenueber der letzten Version angezeigt
"""

import datetime

from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms.queries        import get_role_by_user_path
from dms.queries        import get_base_site_url
from dms.queries        import get_user_by_id

from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_item_vars_edit
from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link
from dms.views_comment  import item_comment
from dms.wiki.utils     import check_wiki_urls
from dms.wiki.queries   import get_page_versions
from dms.diff           import textDiff
from dms.wiki.utils     import get_user_support

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def wikiitem_diff(request,item_container):
  """ zeigt die Versionen dieser Seite """
  versions = get_page_versions(item_container)
  diff_list = []
  org_text = '<h4>%s</h4>\n' % item_container.item.title + item_container.item.text
  curr_text = last_text = ''
  for version in versions:
    v_text = '<h4>%s</h4>\n' % version.title
    v_text += version.text
    diff_list.append({ 'version': version.version, 
                       'text_diff': textDiff(v_text, curr_text),
                       'user': version.owner.get_full_name(),
                       'modified': version.modified.strftime('%d.%m.%Y %H:%M')
                     })
    if last_text.strip() == '':
      last_text = v_text
    curr_text = v_text
  app_name = 'wikiitem'
  my_title = _(u'Versionen der Wiki-Seite')
  content = diff_list
  parent = item_container.get_parent()
  name = item_container.item.name
  wiki_page = name[:name.rfind('.html')]
  dont_show = { 'no_version': True, 'no_new_items': True}
  vars = get_folderish_vars_show(request, item_container, app_name, '',
                                 get_user_support(parent, wiki_page, dont_show))
  if parent.item.has_comments:
    vars['comments'] = True
  vars['text'] = ''
  vars['image_url'] = ''
  vars['slot_right_info'] = ''
  vars['user_support_header'] = _(u'Mögliche Aktionen')
  vars['sub_title'] = '%s: <i>%s</i>' % (_(u'Versionen der Wiki-Seite'), vars['title'])
  vars['title'] = parent.item.title
  vars['site_url'] = get_base_site_url()
  vars['versions'] = diff_list
  vars['org_text'] = textDiff(org_text, last_text)
  vars['user'] = item_container.owner.get_full_name()
  vars['modified'] = item_container.last_modified.strftime('%d.%m.%Y %H:%M')
  return render_to_response ( 'app/wiki/show_version.html', vars )

# -----------------------------------------------------
def wikiitem_show(request,item_container):
  """ zeigt Wiki-Seite """
  app_name = 'wikiitem'
  parent = item_container.get_parent()
  name = item_container.item.name
  url = parent.get_absolute_url() + '?wiki_page=' + name[:name.rfind('.html')]
  return HttpResponseRedirect(url)
