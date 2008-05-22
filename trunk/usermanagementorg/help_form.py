# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die User-Verwaltung der Institutionen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  06.02.2007  Beginn der Arbeit
0.02  21.06.2007  Wiederaufnahme det Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen ein. Dieser Kurzname wird beim Aufrufen
der Web-Adresse verwendet. Der Kurzname sollte den Inhalt
möglichst präzise beschreiben und gleichzeitig möglichst kurz
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
Tragen Sie hier die Überschrift der Community-Verwaltung ein. Unter dieser Überschrift wird 
die Community-Verwaltung angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
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
Falls erforderlich tragen Sie hier die Unterüberschrift Ihrer Community-Verwaltung ein.
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
verwenden Sie bitte das Format "Überschrift 4", da dieses automatisch umgewandelt wird.
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
help_form['section'] = {
     'title'      : _(u'Zuordnung beim <i>übergeordneten</i> Ordner'),
     'help'       : _(u"""<p>
Hier legen Sie fest, beim welchem Zwischentitel Ihre Community-Verwaltung im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihre Community-Verwaltung weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['username'] = {
     'title'      : _(u'Zugangsname'),
     'help'       : _(u"""<p>
Geben Sie hier bitte den exakten Zugangsnamen ein.
</p>""") }

# ----------------------------------------------------------------
help_form['org_name'] = {
     'title'        : _(u'Name der Einrichtung'),
     'auto_complete': True,
     'help'         : _(u"""<p>
Geben Sie hier den Namen der neuen Einrichtung ein..
</p>""") }

# ----------------------------------------------------------------
help_form['email'] = {
     'title'      : _(u'E-Mail-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die exakte E-Mail-Adresse ein.
</p>""") }

# ----------------------------------------------------------------
help_form['groupname'] = {
     'title'      : _(u'Gruppenname'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den neuen Gruppennamen.
</p>""") }

# ----------------------------------------------------------------
help_form['group_names'] = {
     'title'      : _(u'Vorhandene Gruppen'),
     'help'       : _(u"""<p>
Wählen Sie bitte die gewünschte Gruppe aus.
</p>""") }

# ----------------------------------------------------------------
help_form['group_names_target'] = {
     'title'      : _(u'Zielgruppen'),
     'help'       : _(u"""<p>
Wählen Sie bitte die Gruppen aus, denen Sie Mitglieder der betreffenden Basisgruppe
zuordnen möchten.
</p>""") }

# ----------------------------------------------------------------
help_form['group_names_primary'] = {
     'title'      : _(u'Basisgruppen'),
     'help'       : _(u"""<p>
Hier sehen die nicht-veränderbaren Basisgruppen Ihrer Organisation.
</p>""") }

# ----------------------------------------------------------------
help_form['group_names_del'] = {
     'title'      : _(u'Vorhandene Gruppen'),
     'help'       : _(u"""<p>
Aus dieser Liste können Sie eine oder mehrere Gruppen entfernen.
</p>""") }

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'CSV-Datei'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte Ihre CSV-Datei aus.
Die entsprechende CSV-Datei, die Sie mit Excel erzeugen können, muss folgenden Aufbau haben:
</p>
<ul>
<li>Jeweils eine Zeile pro Person.</li>
<li>Die einzelnen Angaben zur Person werden mit einem Semikolon getrennt.</li>
<li>Die Spalten haben folgenden Aufbau:<br />
<br />
<tt>Anrede;Nachname;Vorname;E-Mail</tt><br />
oder<br />
<tt>Anrede;Titel;Nachname;Vorname ; E-Mail</tt>
<br />oder<br />
<tt>Nr.;Anrede;Titel;Nachname;Vorname;E-Mail</tt><br />
</li>
</ul>
<p>Beachten Sie bitte, dass E-Mail-Adressen innerhalb der Community nur einmal auftreten
dürfen.</p>
""") }

# ----------------------------------------------------------------
help_form['sex'] = {
     'title'      : _(u'Anrede'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Anrede ein.
</p>""") }

# ----------------------------------------------------------------
help_form['first_name'] = {
     'title'      : _(u'Vorname'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Vornamen sein. Sollte der Vorname Akzente
oder Buchstaben eines anderen Alphabets enthalten, wandeln Sie diese
bitte in den zugehörigen deutschen Buchstaben um. Umlaute werden
automatisch gewandelt.
</p>""") }

# ----------------------------------------------------------------
help_form['last_name'] = {
     'title'      : _(u'Nachname'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Nachnamen sein. Sollte der Nachname Akzente
oder Buchstaben eines anderen Alphabets enthalten, wandeln Sie diese
bitte in den zugehörigen deutschen Buchstaben um. Umlaute werden
automatisch gewandelt.
</p>""") }

# ----------------------------------------------------------------
help_form['title_name'] = {
     'title'      : _(u'Titel'),
     'help'       : _(u"""<p>
Falls vorhanden tragen Sie hier bitte den Titel ein. In der Regel
wird dieses Feld aber leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['email'] = {
     'title'      : _(u'E-Mail-Adresse'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die E-Mail-Adresse ein. Wichtig: Diese
E-Mail-Adresse muss wirklich existieren, da Community-Mitglieder
mit falschen E-Mail-Adressen periodisch gelöscht werden.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften der
Community-Verwaltung einer Institution fest.
</p>""") }

help_form['tab_intro'] = {
     'title'      : _(u'Intro'),
     'info'       : _(u"""<p>
Sofern vorhanden, werden die Intro-Information zwischen der
Überschrift und dem eigentlichen Inhalt der Community-Verwaltung
angezeigt.</p>

<p>
Falls Sie bei "Intro mehr ..." Informationen eingeben, wird beim 
Intro-Text automatisch ein "Mehr"-Verweis angefügt.
</p>""") }

help_form['tab_navigation'] = {
     'title'      : _(u'Navigation'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte die Menüpunkte des linken Navigationsbereichs
jeweils in einer eigenen Zeile ein.
</p>
<p>
<tt>Verweis | Beschreibung | Erläterung | "ausgewählt" = 0 oder 1 | "optisches Merkmal" = 0 oder 1</tt>
</p>
""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>""") }

help_form['tab_visibility'] = {
     'title'      : _(u'Sichtbarkeit'),
     'info'       : _(u"""<p>
Sie können die Sichtbarkeit der Community-Verwaltung auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

help_form['tab_username'] = {
     'title'      : _(u'Zugangsname'),
     'info'       : _(u"""<p>
Geben Sie hier bitte den Zugangsname des entsprechenden Community-Mitglieds ein.
</p>""") }

help_form['tab_email'] = {
     'title'      : _(u'E-Mail'),
     'info'       : _(u"""<p>
Geben Sie hier bitte die E-Mail-Adresse des Community-Mitglieds ein.
</p>""") }

help_form['tab_group_name_add'] = {
     'title'      : _(u'Grupppenname'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie Gruppennamen Ihrer Institution wie z.B. "Lerngruppe xy" ergänzen.
</p>""") }

help_form['tab_group_name_delete'] = {
     'title'      : _(u'Grupppennamen'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie Gruppennamen Ihrer Institution löschen.
</p>""") }

help_form['tab_group_user_change'] = {
     'title'      : _(u'Basisgrupppe'),
     'info'       : _(u"""<p>
Mit diesem Formular wählen Sie Basisgruppe, aus deren Mitglieder Sie anderen
Gruppen zurodnen möchten.
</p>""") }

help_form['tab_member_user_insert'] = {
     'title'      : _(u'Mitglied aufnehmen'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie ein neues Community-Mitglied in Ihrer Institution aufnehmen.
""") }

help_form['tab_group_user_insert'] = {
     'title'      : _(u'Mitglieder aufnehmen'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie neue Community-Mitglieder in Ihrer Institution aufnehmen.
""") }

help_form['tab_group_user_change'] = {
     'title'      : _(u'Grupppen'),
     'info'       : _(u"""<p>
Hiermit ändern Sie die Gruppenzugehörigkeit Ihrer Community-Mitglieder. Legen Sie dazu
bitte die Basisgrupppe sowie die gewünschten Zielgruppen aus.
</p>""") }

help_form['tab_primary_group_user_change'] = {
     'title'      : _(u'Grupppen'),
     'info'       : _(u"""<p>
Hiermit ändern Sie die Primärgruppenzugehörigkeit von Community-Mitgliedern.
</p>""") }

help_form['tab_group_user_delete'] = {
     'title'      : _(u'Grupppe'),
     'info'       : _(u"""<p>
Mit diesem Formular wählen Sie Gruppe, aus der Sie Mitglieder entfernen möchten.
</p>""") }

