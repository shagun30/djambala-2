#-*-coding: utf-8 -*-
"""
/fortbildung/models.py

.. beschreibt die Datenbankstrukturen fuer Fortbildungsveranstaltungen
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.06.2007  Beginn der Arbeit
"""

from django.db              import models

from django.utils.translation import ugettext as _

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class Fort_Fach(models.Model):
  """ Liste aller Faecher """
  name                = models.CharField(max_length=60, unique=True)

  class Meta:
    db_table = 'dms_fort_fach'

  def __unicode__(self):
    return self.name

  class Admin:
    pass

class Fort_Schulart(models.Model):
  """ Liste aller Faecher """
  name                = models.CharField(max_length=60, unique=True)

  class Meta:
    db_table = 'dms_fort_schulart'

  def __unicode__(self):
    return self.name

  class Admin:
    pass

