# -*- coding: utf-8 -*-
"""
/dms/todolist/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer To-Do-Listen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihrer To-Do-Liste ein. Dieser Kurzname wird beim Aufrufen 
der To-Do-Liste in der Web-Adresse verwendet.
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
Tragen Sie hier die Überschrift der To-Do-Liste ein. Unter dieser Überschrift wird 
die To-Do-Liste angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
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
Falls erforderlich tragen Sie hier die Unterüberschrift Ihrer To-Do-Liste ein.
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Intro'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie den Text fest, der unterhalb
des Überschrift im Sinne einer Einführung angezeigt wird. Sie sollten dieses
Feld beispielsweise aber auch dann nutzen, wenn Sie auf wichtiges Ereignis,
eine gravierende Änderung o.ä. hinweisen möchten.
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
help_form['info_slot_right'] = {
     'title'      : _(u'Seiteninfo'),
     'help'       : _(u"""<p>
In der rechten Spalte können Sie zusätziche Informationen anzeigen.
Diese werden in Blöcken organisiert, wobei ein Block aus einer
Überschrift sowie dem eigentlichen Text besteht. Für Zwischenüberschriften 
verwenden Sie bitte das Format "Überschrift 4", da diese automatisch umgewandelt werden.
</p>

<ul>
<li>
Falls Sie Bilder einbinden wollen, sollten dies nicht breiter als
120 Pixel sein.
</li>
<li>
Wegen der geringen Spaltenbreite sollten Ihre Texte möglichst
knapp gehalten werden. Bei sehr langen Worten stößt das
System an technische Grenzen.
</li>
</ul>""") }

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
help_form['section'] = {
     'title'      : _(u'Zuordnung beim <i>übergeordneten</i> Ordner'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihre To-Do-Liste im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihre To-Do-Liste weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['sections'] = {
     'title'      : _(u'Rubriken für diese To-Do-Liste'),
     'help'       : _(u"""<p>
Mit diesem Texteingabefeld legen Sie die möglichen Rubriken
diese To-Do-Liste fest. Rubriken dienen dem Filtern von Verweisen.
</p>
<p>
Wichtig: Jede Rubrik muss in einer eigenen Zeile stehen.
</p>""") }

# ----------------------------------------------------------------
help_form['has_user_support'] = {
     'title'      : _(u'Beiträge von außen'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob Beiträge von auß
eingestellt werden können.
</p>""") }

# ----------------------------------------------------------------
help_form['has_comments'] = {
     'title'      : _(u'Kann kommentiert werden'),
     'help'       : _(u"""<p>
Dieser Schalter legt fest, ob Beiträge dieser To-Do-Liste
kommentiert werden können bzw. dürfen.
In der Regel wird diese Option eingeschaltet.
</p>""") }

# ----------------------------------------------------------------
help_form['is_moderated'] = {
     'title'      : _(u'Moderation'),
     'help'       : _(u"""<p>
Dieser bewirkt, dass Beiträge entweder sofort sichtbar werden
oder im eingeschalteten Zustand ausdrücklich freigegeben werden
müssen.
</p>
<p>
Außerhalb geschlossener Arbeitsgruppen sollte dieser Schalter
aus Sicherheitsgründen immer eingeschaltet sein.
</p>""") }

# ----------------------------------------------------------------
help_form['owner'] = {
     'title'      : _(u'Zuständige Person/Institution'),
     'help'       : _(u"""<p>
Tragen Sie bitte die Person oder die Institution ein, die für diese
To-Do-Liste zuständig bzw. verantwortlich ist.
</p>""") }

# ----------------------------------------------------------------
help_form['owner_email'] = {
     'title'      : _(u'E-Mail-Adresse für Kontroll-E-Mails'),
     'help'       : _(u"""<p>
Jede neu eingestellte Nachricht erzeugt automatisch eine Kontroll-E-Mail.
Tragen Sie hier die entsprechende E-Mail-Adresse in.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften der
To-Do-Liste fest.
</p>""") }

help_form['tab_intro'] = {
     'title'      : _(u'Intro'),
     'info'       : _(u"""<p>
Die Intro-Information wird unterhalb der Überschrift angezeigt.
Falls Sie bei "Intro - Mehr" Informationen eingeben, wird die Anzeige
automatisch über einen entsprechenden Verweis zugänglich.
</p>""") }

help_form['tab_user_support'] = {
     'title'      : _(u'Ergänzungen'),
     'info'       : _(u"""<p>
Hier legen Sie fest, ob bzw. wer von außen Verweise einstellen darf.
</p>""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>
<p>
Für Expertinnen und Experten: Falls Sie Formulare im Seitenbereich
einfügen möchten, ergänzen Sie in der Adresse <tt>?profi=1</tt>.
</p>""") }

