# -*- coding: utf-8 -*-
"""
/dms/export_dms/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die Exportseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------
help_form['content_type'] = {
     'title'      : _(u'Format der Exportdatei'),
     'help'       : _(u"""<p>
Hier wird das Export-Format festgelegt.
</p>
""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Dieses Objekt wird mit eventuell vorhandenen Unterobjekten im XML-Format exportiert. Diese
Funktion wird insbesondere zur selektiven Datensicherung sowie zum Datenaustausch
zweier Djambala-Systeme benötigt.</p>

<p>
<b>Aus technischen Gründen werden von Datei-Objekten nur die <i>Beschreibungen</i> exportiert,
nicht aber die eigentlichen Dateien!</b>
</p>""") }
