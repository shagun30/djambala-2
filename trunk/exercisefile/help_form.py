# -*- coding: utf-8 -*-
"""
/dms/exercisefile/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Aufgabendateien
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Lösung'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte Ihre Lösung aus, die Sie auf den Server
übertragen möchten.
</p>
""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte gegebenenfalls zusätzliche Information zur Ihrer Lösung ein.
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Kommentar'),
     'help'       : _(u"""<p>
Hier können Sie gegebenenfalls die Lösung sprachlich bewerten.
</p>""") }

# ----------------------------------------------------------------
help_form['integer_1'] = {
     'title'      : _(u'Punktzahl'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Punktzahl ein.
</p>""") }

# ----------------------------------------------------------------
help_form['has_comments'] = {
     'title'      : _(u'Kann kommentiert werden'),
     'help'       : _(u"""<p>
Dieser Schalter legt fest, ob diese Datei kommentiert werden kann
bzw. darf. In der Regel wird diese Option ausgeschaltet.
</p>""") }

# ----------------------------------------------------------------
help_form['one_file'] = {
     'title'      : _(u'Nur eine Datei'),
     'help'       : _(u"""<p>
Pro Person kann nur eine Lösung bzw. eine Datei hochgespielt werden.
Falls schon eine Datei existiert, wird diese beim Hochladen durch die neue Version ersetzt.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Das Eingabefeld "Text" beleibt in der Regel leer.
</p>""") }

help_form['tab_check'] = {
     'title'      : _(u'Bewertung'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie die Arbeit der Schülerin bzw. des Schülers bewerten.
</p>""") }

help_form['tab_update'] = {
     'title'      : _(u'Upload'),
     'info'       : _(u"""<p>
Hier können Sie die auf dem Server vorhandene Datei ersetzen.<br />
<b>Achtung:</b> Die von Ihnen ausgewählte Datei muss den gleichen Namen wie die
Datei auf dem Server haben.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

