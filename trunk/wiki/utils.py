# -*- coding: utf-8 -*-
"""
/dms/wiki/utils.py

.. enthaelt Hilfefunktionen fuer Wikis
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2008  Beginn der Arbeit
0.02  17.03.2008  check_wiki_urls
0.03  21.03.2008  delete_page
0.04  28.03.2008  externe Wiki-Seiten
"""

import re
import string

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import get_item_container_children
from dms.queries        import get_item_container_child_by_name
from dms.queries        import get_item_container_by_path_and_name

from dms.wiki.queries   import delete_page_versions
from dms.wiki.queries   import delete_page_links

from dms.utils          import check_name
from dms.utils          import show_link

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_dont():
  """ Verwaltungsoptionen ausschliessen """
  return { 'sort_mode': 0, 'navigation_mode': 0}

# -----------------------------------------------------
def get_user_support(item_container, wiki_page, dont_show={}):
  """ Beitraege von aussen zulassen """
  if not item_container.item.has_user_support:
    return ''
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/wiki/user_support.html')
  vars = dont_show
  vars['path'] = get_site_url(item_container, '')
  vars['wiki_page'] = wiki_page
  cSection = Context(vars)
  content = tSection.render(cSection)
  return content

# -----------------------------------------------------
def check_wiki_urls(item_container, text, my_role):
  """ ersetzt Wiki-Adressen durch Verweise """

  def get_pages(item_container):
    """ liefert die enthaltenen Wiki-Seiten """
    wiki_item_containers = get_item_container_children(item_container)
    pages = {}
    for page in wiki_item_containers:
      if page.item.app.name == 'dmsWikiItem':
        if page.is_browseable:
          page_name = page.item.name[:page.item.name.find('.html')]
          pages[page_name] = page
    return pages

  def replace_url(item_container, wiki_name, name, pages, text):
    """ ersetzt die Wiki-Notation durch die entsprechende URL """
    url = item_container.get_absolute_url()
    this_url = '%s?wiki_page=%s' % (url, wiki_name)
    this_link = show_link(this_url, name)
    if wiki_name in pages:
      text = '%s%s%s' % (text[:obj.start()], this_link, text[obj.end():])
    else:
      if item_container.item.integer_1 < my_role:
        text = '%s<i>[%s]</i>%s' % (text[:obj.start()], name, text[obj.end():])
      else:
        text = '%s<i>[%s]</i>%s' % (text[:obj.start()], this_link, text[obj.end():])
    return text

  pages = get_pages(item_container)
  prog = re.compile('\[\[.*?\]\]')
  obj = prog.search(text)
  while obj != None:
    name = text[obj.start()+2:obj.end()-2].strip()
    pos = name.find('|')
    if pos > 0:
      wiki_url = name[:pos].strip()
      name = name[pos+1:].strip()
    else:
      wiki_url = name
    wiki_name = check_name(wiki_url.lower(), True)
    # externe Verweise ?
    if wiki_url.find('/') >= 0:
      item_container_curr = item_container
      f_str = string.splitfields(wiki_url, '/')[:-1]
      for f in f_str:
        if f == '..':
          item_container_curr = item_container_curr.get_parent()
          # nur Wiki duerfen adressiert werden
          if item_container_curr.item.app.name != 'dmsWiki':
            item_container_curr = item_container
        else:
          path = '%s%s/' % (item_container_curr.container.path, f)
          item_container_curr = get_item_container_by_path_and_name(path, '')
          # nur Wikis duerfen adressiert werden
          if item_container_curr == None or item_container_curr.item.app.name != 'dmsWiki':
            item_container_curr = item_container
      pages_curr = get_pages(item_container_curr)
      text = replace_url(item_container_curr, wiki_name, name, pages_curr, text)
    else:
      text = replace_url(item_container, wiki_name, name, pages, text)
    obj = prog.search(text)
  return text

# -----------------------------------------------------
def delete_page(item_container):
  """ Wiki-Seite loeschen """
  delete_page_versions(item_container)
  delete_page_links(item_container)
