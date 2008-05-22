# -*- coding: utf-8 -*-
"""
/dms/exercise/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Aufgaben
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.03.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Dateiname'),
     'help'       : _(u"""<p>
Falls Ihre Aufgabe auf Ihrer Festplatte gespeichert ist, können Sie diese
hier hochladen.
</p>
""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift der Aufgabe ein. Unter dieser Überschrift wird 
die Aufgabe angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
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
Falls erforderlich tragen Sie hier eine Unterüberschrift ein.
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Aufgabe'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld beschreiben Sie Ihre Aufgabe fest. - Sie können dieses
Feld leer lassen, wenn Sie Ihre Aufgabe als Datei hochspielen.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Intro - "Mehr ..."'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld können Sie Ihre Aufgabe mit zusätzlichen Informationen
anreichenr, die automatisch mit "Mehr ..." aufrufbar sind.
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
Hier legen Sie fest, bei welchem Zwischentitel Ihre Aufgabe im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihren Ordner weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['visible_end'] = {
     'title'      : _(u'Letzter Abgabetermin'),
     'help':_(u"""<p>
Dieses Feld legt fest, bis zu welchem Zeitpunkt diese Aufgabe bearbeitet werden kann.
</p>""") }

# ----------------------------------------------------------------
help_form['visible_start'] = {
     'title'      : _(u'Sichtbar von'),
     'help'       : _(u"""<p>
Dieses Feld legt den Zeitpunkt fest, ab dem diese Aufgabe sichtbar ist.
</p>""") }

# ----------------------------------------------------------------
help_form['is_browseable'] = {
     'title'      : _(u'Wird angezeigt'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob <i>diese</i> Aufgabe
automatisch im übergeordneten Ordner angezeigt wird oder nicht.
</p>
<p>
<b>Wichtiger Hinweis:</b> Falls der Name bekannt ist, kann die Seite
durch die direkte Angabe der Web-Adresse trotzdem angezeigt werden!
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
Dieser Schalter legt fest, ob Dateien
kommentiert werden können bzw. dürfen.
In der Regel wird diese Option ausgeschaltet.
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
help_form['sections'] = {
     'title'      : _(u'Zwischentitel'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie die möglichen Zwischentitel 
für <b>diesen</b> Ordner fest.
</p>
<p>
Wichtig: Jeder Zwischentitel muss in einer eigenen Zeile stehen. Zwischentitel
werden nur dann angezeigt, wenn mindestens ein Objekt zugeordnet wurde.
</p>""") }

# ----------------------------------------------------------------
help_form['integer_1'] = {
     'title'      : _(u'Punktzahl'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die maximal mögliche Punktzahl ein.
</p>
""") }

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Notenspiegel'),
     'help'       : _(u"""<p>
Geben Sie bitte für die Noten 1-5 die erforderlichen Mindestpunkzahlen jeweils in einer
eigenen Zeile ein. Beispiel: 1:18
</p>""") }

# ----------------------------------------------------------------
help_form['string_2'] = {
     'title'      : _(u'Aufgaben-Adresse im Lernarchiv'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Webadresse der entsprechenden Aufgabe aus den Online-Lernarchiven ein,
mit der an dieser Stelle gearbeitet werden soll.
</p>
<p>
Achtung: Wenn Sie dieses Eingabefeld leer lassen, <b>müssen</b> Sie Felder
Kurzname/ID, Überschrift und Kurzbeschreibung im Reiter "Aufgabe" ausfüllen.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Neue Aufgabe'),
     'info'       : _(u"""<p>
Tragen Sie hier die entsprechenden Informationen zu Ihrer Aufgabe ein. - Falls
Sie eine Aufgabe als Datei eingetragen haben, dann können Sie diese (später) über "pflegen"
ändern.
</p>""") }

help_form['tab_base_2'] = {
     'title'      : _(u'Aufgabe Online-Lernarchiv'),
     'info'       : _(u"""<p>
Mit diesem Formular erzeugen Sie eine neue Aufgabe. Falls Sie eine Aufgabe aus den
Online-Lernarchiven verwenden möchten, können Sie diese Felder
leer lassen. Andernfalls müssen Sie die Felder Kurzname/ID, Überschrift und Kurzbeschreibung
ausfüllen.
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
Sie können die Sichtbarkeit der Aufgabe auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_exercise'] = {
     'title'      : _(u'Aufgabe'),
     'info'       : _(u"""<p>
Bei Bedarf können Sie hier eine Aufgabe als Datei einstellen.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

