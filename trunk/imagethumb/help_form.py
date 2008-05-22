# -*- coding: utf-8 -*-
"""
/dms/imagethumb/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Minibilder
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Minibildname'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte das Minibild aus, das Sie auf den Server
übertragen möchten. - Achtung: PNG-Bilder werden nur im "non-interlaced"-Modus
unterstützt!
</p>

<p>
Der Dateiname Ihres Bildes ist zugleich der Kurzname auf dem Server. Falls also bereits
ein Objekt gleichen Namens in dem entsprechenden Ordner auf dem Server existieren sollte,
kann auf dem Server kein Bild angelegt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['max_width'] = {
     'title'      : _(u'Maximale Breite'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die maximale Breite Ihres Minibildes ein. Das Bild wird
proportional verkleinert, wobei der hier eingegebene Wert nicht überschritten wird.
</p>""") }

# ----------------------------------------------------------------
help_form['max_height'] = {
     'title'      : _(u'Maximale Höhe'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die maximale Höhe Ihres Minibildes ein. Das Bild wird
proportional verkleinert, wobei der hier eingegebene Wert nicht überschritten wird.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die Eigenschaften dieses Minibildes fest.
</p>""") }

help_form['tab_update'] = {
     'title'      : _(u'Upload'),
     'info'       : _(u"""<p>
Hier können Sie das auf dem Server vorhandene Minibild ersetzen.<br />
<b>Achtung:</b> Das von Ihnen ausgewählte Bild muss den gleichen Namen wie das
Minibild auf dem Server haben.
</p>""") }
