# -*- coding: utf-8 -*-
"""
/dms/wiki/queries.py

.. enthaelt Anfragen fuer Hilfstabellen der Wikis
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.03.2008  Beginn der Arbeit
"""

import string

from django.utils.translation import ugettext as _

from dms.models             import get_last_modified

from dms.wiki.models        import DmsWikiLinks
from dms.wiki.models        import DmsWikiVersion

# -----------------------------------------------------
def get_next_version(item_container):
  """ liefert die Anzahl der gespeicherten Versionen """
  from django.db import connection
  cursor = connection.cursor()
  query = 'SELECT MAX(version) FROM dms_wiki_version WHERE wiki_page_id=%i' % item_container.item.id
  cursor.execute(query)
  try:
    row = cursor.fetchone()
    return 1 + row[0]
  except:
    return 1

# -----------------------------------------------------
def save_version(request, item_container):
  """ sichert die aktuelle Version """
  version_obj = DmsWikiVersion()
  version_obj.owner = request.user
  version_obj.wiki_page = item_container.item
  version_obj.version = get_next_version(item_container)
  version_obj.title = item_container.item.title
  version_obj.text = item_container.item.text
  version_obj.modified = item_container.last_modified
  version_obj.save()

# -----------------------------------------------------
def get_page_versions(item_container):
  """ liefert die Liste der verfuegbaren Versionen der Wiki-Seite item_container """
  return DmsWikiVersion.objects.filter(wiki_page=item_container.item).order_by('-version')

# -----------------------------------------------------
def delete_page_versions(item_container):
  """ loescht die verfuegbaren Versionen der Wiki-Seite item_container """
  item_containers = DmsWikiVersion.objects.filter(wiki_page=item_container.item)
  item_containers.delete()

# -----------------------------------------------------
def delete_page_links(item_container):
  """ loescht die auf item_container zeigenden Verweise """
  item_containers = DmsWikiLinks.objects.filter(wiki_page=item_container.item)
  item_containers.delete()

