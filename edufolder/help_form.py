# -*- coding: utf-8 -*-
"""
/dms/edufolder/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer ein Lernarchiv
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
0.02  07.06.2007  Wiki
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Lernarchivs ein. Dieser Kurzname wird beim Aufrufen 
des Lernarchivs in der Web-Adresse verwendet. Der Kurzname sollte den Inhalt Ihres
Onlie-Lernarchivs möglichst präzise beschreiben und gleichzeitig möglichst kurz
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
Tragen Sie hier die Überschrift des Lernarchivs ein. Unter dieser Überschrift wird 
das Lernarchiv angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
Lernarchiv.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Unterüberschrift'), 
     'help'       : _(u"""<p>
Falls erforderlich tragen Sie hier die Unterüberschrift Ihres Lernarchivs ein.
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
anbieten, der automatisch mit "Mehr ..." aufrufbar ist.
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
Hier legen Sie fest, bei welchem Zwischentitel Ihr Lernarchiv im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihren Ordner weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['sections'] = {
     'title'      : _(u'Zwischentitel für <i>dieses</i> Lernarchiv'),
     'help'       : _(u"""<p>
Mit diesem Texteingabefeld legen Sie die möglichen Zwischentitel 
für <b>dieses</b> Lernarchiv fest.
</p>
<p>
Wichtig: Jeder Zwischentitel muss in einer eigenen Zeile stehen. Zwischentitel
werden nur dann angezeigt, wenn mindestens ein Objekt zugeordnet wurde.
</p>""") }

# ----------------------------------------------------------------
help_form['has_user_support'] = {
     'title'      : _(u'Beiträge von außen'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob Beiträge von außen
eingestellt werden können.
</p>""") }

# ----------------------------------------------------------------
help_form['is_moderated'] = {
     'title'      : _(u'Moderation'),
     'help'       : _(u"""<p>
Dieser bewirkt, dass Dateien entweder sofort sichtbar werden
oder im eingeschalteten Zustand ausdrücklich freigegeben werden
müssen.
</p>
<p>
Außerhalb geschlossener Arbeitsgruppen sollte dieser Schalter
aus Sicherheitsgründen <b>immer</b> eingeschaltet sein.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Wikipedia'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte, falls vorhanden, eine Webadresse ein,
die auf einen grundlegenden Artikel (in Wikipedia) verweist.
</p>""") }

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Permanente Weiterleitung'),
     'help'       : _(u"""<p>
Hier können Sie gegebenenfalls eine permanente Weiterleitung einrichten, um z.B.
bei der Einstiegsseite direkt das entsprechende Nachrichtenbrett
angezeigt wird. Geben Sie hier bitte eine vollständige Web-Adresse
(inklusive http://..) ein.
</p>""") }

# ----------------------------------------------------------------
help_form['string_2'] = {
     'title'      : _(u'Name des Webangebots'),
     'help'       : _(u"""<p>
Dieser Eintrag wird nur wirksam, wenn Sie im obigen Eingabefeld
eine Adresse eingetragen haben.
</p>""") }

# ----------------------------------------------------------------
help_form['fach'] = {
     'title'      : _(u'Fach'),
     'help'       : _(u"""<p>
Wählen Sie bitte das passende Fach bzw. Berufsfeld aus.
</p>""") }

# ----------------------------------------------------------------
help_form['schulart'] = {
     'title'      : _(u'Schulart/Schulformen'),
     'help'       : _(u"""<p>
Hier können die passende Schulart auswählen.
</p>""") }

# ----------------------------------------------------------------
help_form['freie_suche'] = {
     'title'      : _(u'Volltextsuche'),
     'help'       : _(u"""<p>
Tragen Sie bitte die passenden Suchbegriffe ein. Die Suchbegriffe werden
mit einem Leerzeichen voneinander getrennt.
</p>""") }

# ----------------------------------------------------------------
help_form['is_exchangeable'] = {
     'title'      : _(u'Elixier-Austausch'),
     'help'       : _(u"""<p>
Soll die Lernressource in das Elixier-Austauschprogramm einbezogen werden?
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieses
Lernarchivs fest.
</p>""") }

help_form['tab_intro'] = {
     'title'      : _(u'Intro'),
     'info'       : _(u"""<p>
Die Intro-Information wird unterhalb der Überschrift angezeigt.
Falls Sie bei "Intro - Mehr" Informationen eingeben, wird die Anzeige
automatisch über einen entsprechenden Verweis zugänglich.
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

help_form['tab_visibility'] = {
     'title'      : _(u'Sichtbarkeit'),
     'info'       : _(u"""<p>
Sie können die Sichtbarkeit des Lernarchivs auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_user_support'] = {
     'title'      : _(u'Ergänzungen'),
     'info'       : _(u"""<p>
Hier legen Sie fest, ob von außen Dateien eingestellt werden dürfen.
</p>""") }

help_form['tab_events'] = {
     'title'      : _(u'Fortbildung'),
     'info'       : _(u"""<p>
Beschreiben Sie hier, die passenden Muster der Fortbildungsveranstaltungen.
</p>""") }

help_form['tab_wiki'] = {
     'title'      : _(u'Wikipedia'),
     'info'       : _(u"""<p>
Tragen Sie hier, falls vorhanden, die passende Adresse von Wikipedia
oder einer anderen grundlegenden Webadresse ein.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

help_form['tab_formal'] = {
     'title'      : _(u'Formales'),
     'info'       : _(u"""<p>
Bei Bedarf tragen Sie hier formale Angaben ein.
</p>""") }

help_form['tab_sections'] = {
     'title'      : _(u'Zwischentitel'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte die gewünschten Zwischentitel ein.
</p>""") }

help_form['tab_ressources'] = {
     'title'      : _(u'Materialtypen'),
     'info'       : _(u"""<p>
Hier sortieren Sie die Lernressoucen.
</p>""") }

