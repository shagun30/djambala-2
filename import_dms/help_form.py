# -*- coding: utf-8 -*-
"""
/dms/import_dms/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die Importseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.02.2007  Beginn der Arbeit
0.02  05.05.2007  xml_text
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Dateiname'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte die XML-Datei aus, die Ihre
Import-Daten enthauml;t. Die Struktur der XML-Datei ist an anderer
Stelle beschrieben.
</p>
""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie wohlgeformte und korrekte XML-Daten importieren.
Das XML-Format ist an anderer Stelle beschrieben.
</p>""") }
