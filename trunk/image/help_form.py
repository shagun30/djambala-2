# -*- coding: utf-8 -*-
"""
/dms/image/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Bilder
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Bildname'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte das Bild aus, das Sie auf den Server
übertragen möchten.
</p>

<p>
Der Dateiname Ihres Bildes ist zugleich der Kurzname auf dem Server. Falls also bereits
ein Objekt gleichen Namens in dem entsprechenden Ordner auf dem Server existieren sollte,
kann auf dem Server kein Bild angelegt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihres Bildes ein. Mit dieser Überschrift wird
Ihr Bild in der Übersicht des Ordners angezeigt.
</p>

<p>
Falls Sie den Titel leer lassen, wird der Dateiname als Titel eingetragen.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Unterüberschrift'), 
     'help'       : _(u"""<p>
Falls erforderlich tragen Sie hier eine Unterüberschrift ein.
In der Regel bleibt dieses Feld aber leer.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die Beschreibung Ihres Bildes ein.
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------

help_form['text_more'] = {
     'title'      : _(u'Erweiterungstext'),
     'help'       : _(u"""<p>
Geben Sie hier bitte den "Rest" Ihrer Beschreibung ein. In der Regel werden
Sie dieses Textfeld aber leer lassen.
</p>
<p>
Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, beim welchem Zwischentitel Ihr Bild im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['has_comments'] = {
     'title'      : _(u'Kann kommentiert werden'),
     'help'       : _(u"""<p>
Dieser Schalter legt fest, ob dieses Bild kommentiert werden kann
bzw. darf. In der Regel wird diese Option ausgeschaltet.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieses
Bildes fest.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Erweiterungstext'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie Ihre Beschreibung erweitern.
</p>""") }

help_form['tab_update'] = {
     'title'      : _(u'Upload'),
     'info'       : _(u"""<p>
Hier können Sie das auf dem Server vorhandene Bild ersetzen.<br />
Das von Ihnen ausgewählte Bild muss den <b>gleichen Namen wie das
Bild auf dem Server</b> haben!
</p>""") }
