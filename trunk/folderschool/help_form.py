# -*- coding: utf-8 -*-
"""
/dms/folderschool/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Basisordner der Schulen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.05.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['integer_1'] = {
     'title'      : _(u'Dienststellennummer'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Dienststellennummer der Schule ein.
Die betreffende Schule muss in der zugehörigen Schuldatenbank existieren.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Name der Schule'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Schulnamen ein.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Namenszusatz'), 
     'help'       : _(u"""<p>
Geben Sie bitte bitte gegebenenfalls die Art der Schule an.
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
Hier legen Sie fest, beim welchem Zwischentitel Ihre geschlossene Arbeitsgruppe im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihre Arbeitsgruppe weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['sections'] = {
     'title'      : _(u'Hauptmenüeinträge'),
     'help'       : _(u"""<p>
Mit diesem Texteingabefeld legen Sie die mögliche Hauptmenüs
dieses Basisordners für Schulen fest.
</p>
<p>
Wichtig: Jeder Zwischentitel muss in einer eigenen Zeile stehen.
<tt>Menüpunkt | Name des Objektes</tt>
</p>""") }

# ----------------------------------------------------------------
help_form['owner'] = {
     'title'      : _(u'Zuständige Person/Institution'),
     'help'       : _(u"""<p>
Tragen Sie bitte die Person oder die Institution ein, die für diese
Arbeits- bzw. Lerngruppe zuständig bzw. verantwortlich ist.
</p>""") }

# ----------------------------------------------------------------
help_form['min_role_id'] = {
     'title'      : _(u'Zugangsrolle'),
     'help'       : _(u"""<p>
Mit dieser Auswahlbox legen Sie Rolle fest, die die meisten Mitglieder
dieser Arbeits- bzw. Lerngruppe haben sollen. Für eine Lerngruppe empfehlen sich
die Rollen "worker" oder "worker_reader". Arbeitsgruppen mit gleichberechtigten
Mitgliedern sollten die Rolle "co_manager" erhalten. - Wichtig: Natürlich
haben Personen, die über höhere Rechte verfügen, ebenfalls Zugang
zu dieser Arbeitsgruppe.
</p>""") }

# ----------------------------------------------------------------
help_form['string_2'] = {
     'title'      : _(u'Terminkalender'),
     'help'       : _(u"""<p>
Falls Sie die Termine des Terminkalenders auf der Startseite anzeigen lassen möchten,
geben Sie hier bitte den relativen Pfad an. Beispiel: <tt>/kooperations/events/</tt>
</p>""") }

# ----------------------------------------------------------------
help_form['new_menu'] = {
     'title'      : _(u'Neues Menü'),
     'help'       : _(u"""<p>
Bitte diese Schaltfläche nur dann aktivieren, wenn das Menü der Arbeitsgruppe
nicht funktioniert bzw. fehlerhaft ist!
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften der
Arbeitsgruppe fest.
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

