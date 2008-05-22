# -*- coding: utf-8 -*-
"""
/dms/lecture/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer einen Vortrag
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  04.02.2007  has_user_support, is_moderated
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Vortrags ein. Dieser Kurzname wird beim Aufrufen 
des Vortrags in der Web-Adresse verwendet. Der Kurzname sollte den Inhalt Ihres
Vortrags möglichst präzise beschreiben und gleichzeitig möglichst kurz
sein.
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
Tragen Sie hier die Überschrift des Vortrags ein. Unter dieser Überschrift wird 
der Vortrag angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
Ordner.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Unterüberschrift'), 
     'help'       : _(u"""<p>
Falls erforderlich tragen Sie hier die Unterüberschrift Ihres Vortrags ein.
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['nav_title'] = {
     'title'      : _(u'Navigationszeile'),
     'help'       : _(u"""<p>
Ihr Text wird in der "Navigationszeile" oberhalb des Titels angezeigt.
Falls Sie das Eingabefeld leer lassen, wird die eingegebene Überschrift
automatisch als Navigationszeile verwendet. Bei kurzen Titeln ist dies
in Ordnung; bei langen Texten sollten Sie unbedingt einen kürzeren Text verwenden,
da es sonst zu störenden Zeilenümbrüchen kommen kann.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Intro'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie den Text fest, der unterhalb
des Überschrift im Sinne einer Einführung angezeigt wird. Sie sollten dieses
Feld beispielsweise aber auch dann nutzen, wenn Sie auf besondere Punkte
hinzuweisen.
</p>

<p>
In der Regel werden Sie dieses Feld aber leer lassen.
</p>""") }

# ----------------------------------------------------------------

help_form['text_more'] = {
     'title'      : _(u'Intro - "Mehr ..."'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld können Sie einen ausführlicheren Introtext
anbieten, der automatisch mit "Mehr ..." auf der erreichbar ist.
</p>""") }

# ----------------------------------------------------------------

help_form['image_url'] = {
     'title'      : _(u'Bild zum Intro'),
     'help'       : _(u"""<p>
Bei Bedarf können Sie links neben Ihrem Intro-Text ein Bild anzeigen lassen.
Da Sie hier die Web-Adresse (http://..) des Bildes angeben, muss sich diesen Bild bereits 
auf dem Server befinden.
</p>""") }

# ----------------------------------------------------------------

help_form['image_url_url'] = {
     'title'      : _(u'URL zum Bild des Intros'),
     'help'       : _(u"""<p>
Falls Sie ein Bild zum Intro angegeben haben, können Sie das Bild
mit einer Web-Adresse (http://..) verknüpfen.
</p>""") }

# ----------------------------------------------------------------

help_form['image_extern'] = {
     'title'      : _(u'Verweis im eigenen Fenster'),
     'help'       : _(u"""<p>
Falls die mit dem Bild verknüpfte Seite in einem eigenen Fenster angezeigt werden soll,
müssen Sie dieses Feld aktivieren.
</p>""") }

# ----------------------------------------------------------------

help_form['is_wide'] = {
     'title'      : _(u'Intro mit voller Breite'),
     'help'       : _(u"""<p>
Mit diesem Feld werden die Intro-Information in voller Breite angezeigt.
</p>""") }

# ----------------------------------------------------------------

help_form['is_important'] = {
     'title'      : _(u'Intro mit Hervorhebung'),
     'help'       : _(u"""<p>
Dieses Feld hinterlegt die Intro-Information mit einem farbigen Block.
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
     'title'      : _(u'Zuordnung beim <i>übergeordneten</i> Ordner'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Vortrag im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihren Vortrag weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------

help_form['sections'] = {
     'title'      : _(u'Zwischentitel für <i>diesen</i> Vortrag'),
     'help'       : _(u"""<p>
Mit diesem Texteingabefeld legen Sie die möglichen Zwischentitel 
für <b>diesen</b> Vortrag fest.
</p>
<p>
Wichtig: Jeder Zwischentitel muss in einer eigenen Zeile stehen. Zwischentitel
werden nur dann angezeigt, wenn mindestens ein Objekt zugeordnet wurde.
</p>""") }

# ----------------------------------------------------------------

help_form['visible_end'] = {
     'title'      : _(u'Sichtbar bis'),
     'help':_(u"""<p>
Dieses Feld legt fest, bis zu welchem Zeitpunkt dieser Vortrag sichtbar ist.
</p>""") }

# ----------------------------------------------------------------

help_form['visible_start'] = {
     'title'      : _(u'Sichtbar von'),
     'help'       : _(u"""<p>
Dieses Feld legt den Zeitpunkt fest, ab dem dieser Vortrag sichtbar ist.
</p>""") }

# ----------------------------------------------------------------
help_form['is_browseable'] = {
     'title'      : _(u'Wird automatisch angezeigt'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob <i>dieser</i> Vortrag
automatisch im übergeordneten Ordner angezeigt wird oder nicht.
</p>
<p>
<b>Wichtiger Hinweis:</b> Falls der Name bekannt ist, kann die Seite
durch die direkte Angabe der Web-Adresse trotzdem angezeigt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['has_user_support'] = {
     'title'      : _(u'Ergänzungen von außen'),
     'help'       : _(u"""<p>
Falls diese Option eingeschaltet wird, können Ergänzungen
von außen vorgenommen werden.
</p>""") }

# ----------------------------------------------------------------
help_form['has_comments'] = {
     'title'      : _(u'Kann kommentiert werden'),
     'help'       : _(u"""<p>
Dieser Schalter legt fest, ob dieser Vortrag bzw. die Folien dieses Vortrags
kommentiert werden können bzw. dürfen.
In der Regel bleibt diese Option ausgeschaltet.
</p>""") }

# ----------------------------------------------------------------
help_form['is_moderated'] = {
     'title'      : _(u'Moderation'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, Eingaben von auß sofort
sichtbar werden oder explizit freigeschaltet werden müssen.
</p>
<p>
Wenn Eingaben von außen zugelassen werden, sollten Sie diese
OPtion grundsätzlich einschalten.
</p>""") }

# ----------------------------------------------------------------
help_form['show_next'] = {
     'title'      : _(u'Verweise auf Geschwister-Dokumente'),
     'help'       : _(u"""<p>
Mit dieser Option werdeb bei den Folien am unteren Ende eine entsprechende
Navigationsoptionen angeboten.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften
des Vortrags fest.
</p>""") }

help_form['tab_intro'] = {
     'title'      : _(u'Intro'),
     'info'       : _(u"""<p>
Sofern vorhanden, werden die Intro-Information zwischen der
Überschrift und dem eigentlichen Inhalt des Vortrags
angezeigt.</p>

<p>
Falls Sie bei "Intro mehr ..." Informationen eingeben, wird beim 
Intro-Text automatisch ein "Mehr"-Verweis angefügt.
</p>""") }

help_form['tab_user_support'] = {
     'title'      : _(u'Ergänzungen'),
     'info'       : _(u"""<p>
Hier legen Sie fest, ob bzw. wer von außen Folien etc. ergänzen darf.
</p>""") }

help_form['tab_visibility'] = {
     'title'      : _(u'Sichtbarkeit'),
     'info'       : _(u"""<p>
Sie können die Sichtbarkeit des Vortrags auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_sections'] = {
     'title'      : _(u'Zwischentitel'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte die gewünschten Zwischentitel ein.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

