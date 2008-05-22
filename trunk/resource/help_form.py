# -*- coding: utf-8 -*-
"""
/dms/resource/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Ordner
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  26.03.2007  perma_link
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihrer Ressourcenverwaltung ein. Dieser Kurzname wird beim Aufruf in der Web-Adresse verwendet. Der Kurzname sollte Ihre Ressourcenverwaltung möglichst präzise beschreiben und gleichzeitig möglichst kurz sein.
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
Tragen Sie hier die Überschrift der Ressourcenverwaltung ein. Unter dieser Überschrift wird 
die Ressourcenverwaltung angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
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
Falls erforderlich tragen Sie hier die Unterüberschrift Ihres Ordners ein.
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Intro'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie den Text fest, der unterhalb
des Überschrift im Sinne einer Einführung angezeigt wird. Sie sollten dieses
Feld beispielsweise aber auch dann nutzen, wenn Sie auf ein wichtiges Ereignis,
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
anbieten, der automatisch mit "Mehr ..." auf der Startseite erreichbar ist.
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
help_form['navigation_left'] = {
     'title'      : _(u'Linkes Menü'),
     'help'       : _(u"""<p>
Mit diesem Auswahlfeld legen Sie den aktiven Menüpunkt der linken
Navigation fest. Hauptmenüpunkte werden fett angezeigt; die jeweiligen
Unterpunkte werden normal dargestellt.
</p>""") }

# ----------------------------------------------------------------
help_form['domain'] = {
     'title'      : _(u'Domaine'),
     'help'       : _(u"""<p>
Mit diesem Auswahlfeld legen Sie die Domaine dieses Ordners sowie
aller Unterordner fest.
</p>""") }

# ----------------------------------------------------------------
help_form['menu_name'] = {
     'title'      : _(u'Kurzname'),
     'help'       : _(u"""<p>
Geben Sie hier bitte einen eindeutigen Kurznamen Ihres Menüpunktes ein.
Umlaute sind nicht zulässig!
</p>""") }

# ----------------------------------------------------------------
help_form['navigation'] = {
     'title'      : _(u'Navigationsbereich'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte zeilenweise die verschiedenen Menüpunkte ein.
Für Leerzeilen geben Sie '999' ein. Vergessen Sie bitte bei
den Web-Adressen das abschließende "/" nicht!
</p>""") }

# ----------------------------------------------------------------
help_form['new_name'] = {
     'title'      : _(u'Kurzname'),
     'help'       : _(u"""<p>
Geben Sie hier bitte einen eindeutigen Kurznamen Ihres Menüpunktes ein.
Umlaute sind nicht zulässig!
</p>""") }

# ----------------------------------------------------------------
help_form['new_description'] = {
     'title'      : _(u'Beschreibung'),
     'help'       : _(u"""<p>
Beschreiben Sie hier bitte knapp den gewünschten neuen Menüpunkt.
</p>""") }

# ----------------------------------------------------------------
help_form['info_slot_right'] = {
     'title'      : _(u'Seiteninfo'),
     'help'       : _(u"""<p>
In der rechten Spalte können Sie zusätzliche Informationen anzeigen.
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
help_form['show_next'] = {
     'title'      : _(u'Verweise auf Geschwister-Dokumente'),
     'help'       : _(u"""<p>
In manchen Situationen werden größere Texteinheiten
auf mehrere Seiten verteilt. Wenn Sie diese Option einschalten,
wird bei den Informationsseiten am unteren Ende eine entsprechende
Navigationsoption angeboten.
</p>

<p>
Falls Ihre Informationsseiten inhaltlich nur lose gekoppelt sind,
sollten Sie diese Option ausschalten.
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung beim <i>übergeordneten</i> Ordner'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Ordner im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihren Ordner weiter nach oben
oder nach unten verschieben.
</p>""") }

# ----------------------------------------------------------------
help_form['my_periods'] = {
     'title'      : _(u'Zeitanzeige'),
     'help'       : _(u"""<p>
Dieser Schalter bewirkt, dass die Reservierungs-Zeiträume entweder wie in obigem Textfeld definiert werden oder als Standardwerte (Schulstunden oder Zeitstunden) angelegt werden.
</p>""") }

# ----------------------------------------------------------------
help_form['periods_as_text'] = {
     'title'      : _(u'Zeitspannen'),
     'help'       : _(u"""<p>
Bitte geben Sie jede Zeitspanne als eigene Zeile im Format &quot;Anfangszeitpunkt|Name&quot; ein.<br />Beispiel: &quot;22:00|Nachts&quot;<br />Die Zeiten müssen bei 00:00 beginnen und aufsteigend geordnet sein. Als Endzeitpunkt wird automatisch der Anfangszeitpunkt der folgenden Zeitspanne genommen, bzw. 24:00 für die letzte Zeitspanne.<br />Sind Name und Anfangszeitpunkt identisch, so wird von einem Zeitpunkt ausgegangen.</p>
<p>
Der Inhalt dieses Feldes ist nur relevant, wenn unten als Zeitanzeige &quot;Zeitspannen wie oben&quot; markiert wurde.<br />
Eine Standard-Vorbelegung erhalten Sie auch, wenn Sie dieses Feld leer lassen.
</p>""") }


# ----------------------------------------------------------------
help_form['res_type_id'] = {
     'title'      : _(u'Kategorie'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Kategorie aus.
</p>""") }


# ----------------------------------------------------------------
help_form['sections'] = {
     'title'      : _(u'Zwischentitel für <i>diesen</i> Ordner'),
     'help'       : _(u"""<p>
Mit diesem Texteingabefeld legen Sie die möglichen Zwischentitel 
für <b>diesen</b> Ordner fest.
</p>
<p>
Wichtig: Jeder Zwischentitel muss in einer eigenen Zeile stehen. Zwischentitel
werden nur dann angezeigt, wenn mindestens ein Objekt zugeordnet wurde.
</p>""") }




help_form['res_types'] = {
     'title'      : _(u'Kategorien'),
     'help'       : _(u"""<p>
Wählen Sie bitte die gewünschte(n) Kategorie(n) aus.</p>""") }



help_form['res_day'] = {
     'title'      : _(u'Tag der Reservierung'),
     'help'       : _(u"""<p>
Geben Sie an, an welchem Datum Sie reservieren wollen. Format: TT.MM.JJJJ</p>""") }


help_form['res_time'] = {
     'title'      : _(u'Zeitrahmen der Reservierung'),
     'help'       : _(u"""<p>
Geben Sie die Start- und Endzeitpunkt im Format HH:MM-HH:MM ein.<br />Z.B.: &quot;09:15-14:30&quot;</p>""") }

help_form['date_start'] = {
     'title'      : _(u'Beginn der Reservierung'),
     'help'       : _(u"""<p>
Geben Sie den Anfangszeitpunkt im Format TT.MM.JJJJ an.<br /> Z.B.: &quot;05.03.2008&quot;</p>""") }

help_form['date_end'] = {
     'title'      : _(u'Ende der Reservierung'),
     'help'       : _(u"""<p>
Geben Sie den Endzeitpunkt im Format TT.MM.JJJJ an.<br /> Z.B.: &quot;07.03.2008&quot;</p>""") }

help_form['type_description'] = {
     'title'      : _(u'Name der Kategorie'),
     'help'       : _(u"""<p>
Geben Sie eine neue Kategorie ein.</p>""") }

help_form['existing_types'] = {
     'title'      : _(u'vorhandene Kategorien'),
     'help'       : _(u"""<p>Hier bekommen Sie die bereits bekannten Kategorien gezeigt.<br /><b><i>(Kein Eingabefeld!)</i></b></p>""") }

help_form['res_description'] = {
     'title'      : _(u'Bezeichnung'),
     'help'       : _(u"""<p>
Geben Sie eine möglichst kurze Bezeichnung (Schlagwort) der neuen Ressource ein.</p>""") }

help_form['res_descr_more'] = {
     'title'      : _(u'Ausführliche Beschreibung'),
     'help'       : _(u"""<p>
Hier können Sie eine ausführliche Beschreibung der neuen Ressource eingeben (optional).</p>""") }

help_form['res_url'] = {
     'title'      : _(u'Webadresse'),
     'help'       : _(u"""<p>
Hier können Sie eine Webadresse mit weiteren Informationen über die neue Ressource eingeben (optional).</p>""") }

help_form['existing_res'] = {
     'title'      : _(u'sonst vorhandene Ressourcen'),
     'help'       : _(u"""<p>Hier bekommen Sie die sonst bereits bekannten Ressourcen gezeigt.<br /><b><i>(Kein Eingabefeld!)</i></b></p>""") }

help_form['delete_res'] = {
     'title'      : _(u'Löschen'),
     'help'       : _(u"""<p>Bitte markieren Sie, wenn die Ressource gelöscht werden soll.</b></p>""") }


# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Permanente Weiterleitung'),
     'help'       : _(u"""<p>
Hier können Sie gegebenenfalls eine permanente Weiterleitung einrichten, um z.B.
bei einer Einstiegsseite direkt zu einem passenden Nachrichtenbrett
zu springen. Geben Sie hier bitte eine vollständige Web-Adresse
(inklusive http://..) ein.
</p>""") }

# ----------------------------------------------------------------
help_form['min_role_id'] = {
     'title'      : _(u'Zugangsrolle'),
     'help'       : _(u"""<p>
Mit dieser Auswahlbox legen Sie die minimale Rolle fest, die für den Zugang
für diesen Ordner erforderlich ist.
</p>""") }

# ----------------------------------------------------------------
# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieser
Ressourcenverwaltung fest.
</p>""") }

help_form['tab_reserve'] = {
     'title'      : _(u'eintägige Reservierung'),
     'info'       : _(u"""<p>
Hier können Sie <b>eintägige</b> Reservierungen vornehmen.</p>
<p>
Bitte wählen Sie zunächst den Zeitrahmen (Schritt 1/2).
</p>""") }

help_form['tab_reserve_m'] = {
     'title'      : _(u'mehrtägige Reservierung'),
     'info'       : _(u"""<p>
Hier können Sie <b>mehrtägige</b> Reservierungen für ganze Tage vornehmen. Soll der erste oder letzte Tag nicht ganz reserviert werden, reservieren Sie diesen bitte einzeln.</p>
<p>
Bitte wählen Sie zunächst den Zeitrahmen (Schritt 1/2).
</p>""") }

help_form['tab_new_type'] = {
     'title'      : _(u'neue Kategorie'),
     'info'       : _(u"""<p></p>""") }

help_form['tab_new_res'] = {
     'title'      : _(u'neue Ressource'),
     'info'       : _(u"""<p></p>""") }

help_form['tab_reserve_2'] = {
     'title'      : _(u'Reservierung'),
     'info'       : _(u"""
<p>
Bitte wählen Sie zunächst die gewünschte(n) Ressource(n) aus (Schritt 2/2).
</p>""") }

help_form['tab_edit_res'] = {
     'title'      : _(u'Bearbeiten'),
     'info'       : _(u"""<p></p>""") }

help_form['tab_edit0_res'] = {
     'title'      : _(u'Bearbeiten'),
     'info'       : _(u"""<p></p>""") }

help_form['tab_del_res'] = {
     'title'      : _(u'Löschen'),
     'info'       : _(u"""<p></p>""") }

help_form['tab_intro'] = {
     'title'      : _(u'Intro'),
     'info'       : _(u"""<p>
Die Intro-Information wird unterhalb der Überschrift angezeigt.
Falls Sie bei "Intro - Mehr" Informationen eingeben, wird die Anzeige
automatisch über einen entsprechenden Verweis zugänglich.
</p>""") }

help_form['tab_navigation'] = {
     'title'      : _(u'Navigationspunkt'),
     'info'       : _(u"""<p>
Wählen Sie bitte den aktiven Menüpunkt des linken Navigationsbereichs aus.
</p>""") }

help_form['tab_navigation_left'] = {
     'title'      : _(u'Navigationsbereich'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie den linken Navigationsbereichs anpassen.
</p>
<p>
<tt>Ebene (0/1) | Kurzname | Web-Adresse (http://..) | Beschreibung | opt. Kommentar | opt. Präfix</tt>
</p>
""") }

help_form['tab_navigation_left_new'] = {
     'title'      : _(u'Neues Menü'),
     'info'       : _(u"""<p>
Mit diesem Formular erzeugen Sie ein neuen (leere) linken Menü.
</p>""") }

help_form['tab_navigation_top'] = {
     'title'      : _(u'Oberer Navigationsbereich'),
     'info'       : _(u"""<p>
Mit diesem Formular können Sie den oberen Navigationsbereichs anpassen.
</p>
<p>
<tt>Kurzname | Web-Adresse (http://..) | Beschreibung | opt. Kommentar | opt. Präfix</tt>
</p>
""") }

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
Sie können die Sichtbarkeit des Ordners auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Zeitanzeige'),
     'info'       : _(u"""<p>
Optionen zur Zeitanzeige (Zeitpunkte oder Zeiträume)
</p>""") }

help_form['tab_sections'] = {
     'title'      : _(u'Zwischentitel'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte die gewünschten Zwischentitel ein.
</p>""") }

help_form['tab_domain'] = {
     'title'      : _(u'Domaine'),
     'info'       : _(u"""<p>
Wählen Sie bitte die richtige Domaine aus.<p>

<p>
<b>Wichtiger Hinweis:</b>
Der Pfad Ihres Ordners muss zum "Basis-Folder" der Domaine passen!
</p>""") }