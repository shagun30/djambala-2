# -*- coding: utf-8 -*-
"""
/dms/redirect/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Weiterleitungen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.01.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------

help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihrer Weiterleitung ein. Da die eigentliche Informationen
über die Weiterleitungsadresse angezeigt werden, empfehlen wir, dies im Namen
z.B. dadurch kenntlich zu machen, dass Sie am Ende des Namens <tt>_redirect</tt>
ergänzen.
</p>

<p>
Beim Aufrufen der Seiten wird zwischen Groß- und Kleinschreibung unterschieden. Bitte
verwenden Sie beim Kurznamen ausschließlich Kleinbuchstaben. Leerzeichen werden durch
einen Unterstrich, Umlaute durch "ae", "oe" usw. ersetzt.
</p>""") }

# ----------------------------------------------------------------

help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihrer Weiterleitung ein. Dieser Titel erscheint
in der Übersicht des Ordners, der Ihre Weiterleitung enthält.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die vollständige Web-Adresse an, zu der weitergeleitet
werden soll. Vergessen Sie bitte nicht <tt>http://</tt>.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more_extern'] = {
     'title'      : _(u'Eigenes Fenster'),
     'help'       : _(u"""<p>
Mit diesem Auswahlfeld legen Sie fest, dass der Verweis in einem eigenen Fenster
angezeigt werden soll. Verweise außerhalb dieses Servers werden immer in
einem eigenen Fenster geöffnet.
</p>""") }

# ----------------------------------------------------------------

help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Hier können Sie bei Bedarf Ihre Weiterleitung beschreiben. In der Regel
werden Sie dieses Feld aber leer lassen.
</p>
<p>
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------

help_form['order_by'] = {
     'title'      : _(u'Ordnungszahl'),
     'help'       : _(u"""<p>
Mit dieser Zahl bestimmen Sie die Sortierreihenfolge. Kleine Zahlen erscheinen
weiter oben, größere Zahlen weiter unten. Haben zwei Objekte die
gleiche Ordnungszahl, so werden Sie alphabetisch nach der Überschrift sortiert.
</p>""") }

# ----------------------------------------------------------------

help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihre Weiterleitung im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------

help_form['visible_end'] = {
     'title'      : _(u'Sichtbar bis'),
     'help':_(u"""<p>
Dieses Feld legt fest, bis zu welchem Zeitpunkt diese Seite sichtbar ist.
</p>""") }

# ----------------------------------------------------------------

help_form['visible_start'] = {
     'title'      : _(u'Sichtbar von'),
     'help'       : _(u"""<p>
Dieses Feld legt den Zeitpunkt fest, ab dem diese Seite sichtbar ist.
</p>""") }

# ----------------------------------------------------------------

help_form['is_browseable'] = {
     'title'      : _(u'Wird angezeigt'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob <i>diese</i> Weiterleitung
automatisch in Ihrem Ordner angezeigt wird oder nicht.
</p>
<p>
<b>Wichtiger Hinweis:</b> Falls der Name bekannt ist, kann die Seite
durch die direkte Angabe der Web-Adresse trotzdem angezeigt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften der
Weiterleitung fest.
</p>""") }

help_form['tab_visibility'] = {
     'title'      : _(u'Sichtbarkeit'),
     'info'       : _(u"""<p>
Sie können die Sichtbarkeit Ihrer Weiterleitung auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

