#-*-coding: utf-8 -*-
"""
/dms/exercisefolder/models.py

.. beschreibt die Datenbankstrukturen der Aufgabendatenbank
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2005  Beginn der Arbeit
"""

from django.utils.encoding  import smart_unicode
from django.db              import models

from django.utils.translation import ugettext as _

from dms.models             import DmsItem

from dms.encode_decode      import encode_html

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

