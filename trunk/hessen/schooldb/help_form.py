# -*- coding: utf-8 -*-
"""
/dms/hessen/schooldb/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die Anzeige der Schul-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.02.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Suchformulars für die Schuldatenbank ein. 
Dieser Kurzname wird beim Aufrufen in der Web-Adresse verwendet.
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
Tragen Sie hier die Überschrift Ihres Suchformulars ein. Unter dieser Überschrift wird 
Ihre Seite angezeigt. Dieser Titel erscheint ebenfalls in der Übersicht des Ordners, der
Ihre Seite enthält.
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

help_form['text'] = {
     'title'      : _(u'Intro'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie den Text fest, der unterhalb
der Überschrift im Sinne einer Einführung angezeigt wird. Sie sollten dieses
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
     'title'      : _(u'Schmuckbild'),
     'help'       : _(u"""<p>
Bei Bedarf können Sie rechts neben Ihrem Text ein Bild anzeigen lassen.
Da Sie hier die Web-Adresse (http://..) des Bildes angeben, muss sich diesen Bild bereits 
auf dem Server befinden.
</p>""") }

# ----------------------------------------------------------------
help_form['image_url_url'] = {
     'title'      : _(u'URL zum Bild'),
     'help'       : _(u"""<p>
Falls Sie ein Bild angegeben haben, können Sie das Bild
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
Falls Sie Bilder einbinden wollen, sollten diese nicht breiter als
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
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Suchformular im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Filterung'),
     'help'       : _(u"""<p>
Hier legen Sie gegebenenfalls die Grundfilterung für Abfragen in Bildungsregionen
fest. Die Filter werden in Form von Python-Dictionaries beschrieben. Folgende Optionen
können gesetzt werden:
</p>
<ul>
<li>region</li>
<li>schul_amt</li>
<li>schul_beseinr</li>
<li>schul_name</li>
<li>schul_ort</li>
<li>schul_plz</li>
<li>schul_rechtsstellung</li>
<li>schul_sformangebot</li>
<li>schul_sprfolge</li>
<li>schul_traeger</li>
<li>schul_typ</li>
<li>schul_voraussetzung</li>
</ul>""") }

# ----------------------------------------------------------------
help_form['schul_name'] = {
     'title'      : _(u'Schulname'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den gewünschten Schulnamen ein. In der Regel
reicht es, wenn Sie nur den Anfang des Schulnamens eintragen.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_ort'] = {
     'title'      : _(u'Gemeinde'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Namen der Stadt bzw. Gemeinde ein. Auch hier
genügt der Anfang des Gemeindenamens.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_plz'] = {
     'title'      : _(u'Postleitzahl'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Postleitzahl der der Stadt bzw. Gemeinde ein.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_nr'] = {
     'title'      : _(u'Dienststellennummer'),
     'help'       : _(u"""<p>
Falls bekannt, können Sie hier die Dienststellennummer der Schule eintragen.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_beseinr'] = {
     'title'      : _(u'Besondere Einrichtungen'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld legen Sie fest, über welche besonderen Einrichtungen
die gewünschten Schulen verfügen sollen.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_rechtsstellung'] = {
     'title'      : _(u'Rechtsstellung'),
     'help'       : _(u"""<p>
Hier legen Sie fest, welche Rechtsstellung die gewünschten Schulen
besitzen sollen.
</p>""") }

# ----------------------------------------------------------------
help_form['schul_amt'] = {
     'title'      : _(u'Schulamt'),
     'help'       : _(u"""<p>
Zu welchem Schulamt gehören die gesuchten Schulen?
</p>""") }

# ----------------------------------------------------------------
help_form['schul_traeger'] = {
     'title'      : _(u'Schulträger'),
     'help'       : _(u"""<p>
Zu welchem Schulträger gehören die gesuchten Schulen?
</p>""") }

# ----------------------------------------------------------------
help_form['schul_typ'] = {
     'title'      : _(u'Schultyp'),
     'help'       : _(u"""<p>
Zu welchem Schultyp gehören die gesuchten Schulen?
</p>""") }

# ----------------------------------------------------------------
help_form['schul_sformangebot'] = {
     'title'      : _(u'Schulformangebote'),
     'help'       : _(u"""<p>
Welche Schulformangebote bieten die gesuchten Schulen?
</p>""") }

# ----------------------------------------------------------------
help_form['schul_sprache'] = {
     'title'      : _(u'Sprachenfolge'),
     'help'       : _(u"""<p>
Welche Sprachenfolge bieten die gesuchten Schulen?
</p>""") }

# ----------------------------------------------------------------
help_form['schul_voraussetzung'] = {
     'title'      : _(u'Koedukation'),
     'help'       : _(u"""<p>
Wie ist die Koedukation der gesuchten Schulen geregelt?
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieses
Suchformular fest.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihr Suchformular mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>""") }

help_form['tab_standard'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Füllen Sie bitte die entsprechenden Felder aus.
</p>""") }

help_form['tab_beseinr'] = {
     'title'      : _(u'Bes. Einrichtung'),
     'info'       : _(u"""<p>
Mit diesen Eingabefelder legen Sie besondere Eigenschaften der gewünschten Schulen fest.
</p>""") }

help_form['tab_rechtsstellung'] = {
     'title'      : _(u'Rechtsstellung'),
     'info'       : _(u"""<p>
Hier legen Sie die gewünschte Rechtsstellung der gesuchten Schulen fest.
</p>""") }

help_form['tab_org'] = {
     'title'      : _(u'Schulamt/träger'),
     'info'       : _(u"""<p>
Hier legen Sie die gewünschte Einrichtungen fest, denen die gesuchten Schulen
zugeordnet sind.
</p>""") }

help_form['tab_typ'] = {
     'title'      : _(u'Schultyp/Angebote'),
     'info'       : _(u"""<p>
Hier legen Sie die gewünschten Schultypen bzw. Schulformangebote fest.
</p>""") }

help_form['tab_sprache'] = {
     'title'      : _(u'Sprachenfolge'),
     'info'       : _(u"""<p>
Mit diesen Eingabefelder legen Sie u.a. die gewünschte Sprachenfolge fest.
</p>""") }

help_form['tab_justice'] = {
     'title'      : _(u'Recht'),
     'info'       : _(u"""<p>
Rechtliche Aspekte können Sie hier eintragen.
</p>""") }

