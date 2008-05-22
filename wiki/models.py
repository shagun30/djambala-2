#-*-coding: utf-8 -*-
"""
/dms/wiki/models.py

.. beschreibt die Hilfstabellen fuer Wikia
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.03.2008  Beginn der Arbeit
"""

import  datetime

from django.db              import models

from django.utils.translation import ugettext as _

from dms.auth.models        import User
from dms.models             import DmsApp
from dms.models             import DmsItem

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsWikiLinks(models.Model):
  """ Beschreibung der Wiki-Verweise innerhalb der Wiki-Seiten ... """
  wiki_page     = models.ForeignKey(DmsItem)
  name          = models.CharField(max_length=200,db_index=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_wiki_links'

class DmsWikiVersion(models.Model):
  """ die verschiedenen Versionen einer Seite ... """
  wiki_page     = models.ForeignKey(DmsItem)
  owner         = models.ForeignKey(User)
  version       = models.IntegerField()
  title         = models.CharField(max_length=200)
  text          = models.TextField()
  modified      = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
    return self.title

  class Meta:
    db_table = 'dms_wiki_version'
