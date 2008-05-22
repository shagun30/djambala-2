# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die Anzeige der Schul-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.02.2007  Beginn der Arbeit
0.02  20.02.2008  gueltig
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form
from django.utils.safestring  import mark_safe

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Suchformulars für die Fortbildungsdatenbank ein. 
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
help_form['training_fach'] = {
     'title'      : _(u'Fach'),
     'help'       : _(u"""<p>
Wählen Sie hier bitte das gewünschte Fach aus.
</p>""") }

# ----------------------------------------------------------------
help_form['training_text'] = {
     'title'      : _(u'Volltext-Suche'),
     'help'       : _(u"""<p>
Geben Sie bitte in das Eingabefeld den gewünschten Suchbegriff ein.
</p>""") }

# ----------------------------------------------------------------
help_form['training_gueltig'] = help_form['integer_1'] = {
     'title'      : _(u'Gültigkeitsbereich'),
     'help'       : _(u"""<p>
Hier können Sie den Gültigkeitsbereich der Suche einschränken bzw. erweitern.
</p>""") }

# ----------------------------------------------------------------
help_form['training_schulart'] = {
     'title'      : _(u'Schularten'),
     'help'       : _(u"""<p>
Wählen Sie hier bitte die gewünschten Schularten aus.
</p>""") }

# ----------------------------------------------------------------
help_form['training_zielgruppe'] = {
     'title'      : _(u'Zielgruppen'),
     'help'       : _(u"""<p>
Wählen Sie hier bitte die gewünschten Zielgruppen aus.
</p>""") }

# ----------------------------------------------------------------
help_form['training_anbieter'] = {
     'title'      : _(u'Anbieter'),
     'help'       : _(u"""<p>
Wählen Sie bitte den Anbieter aus der Liste aus.
</p>""") }

help_form['string_1'] = {
     'title'      : _(u'Anbieter'),
     'help'       : _(u"""<p>
Geben Sie hier gegebenenfalls die IQ-Zugangsnamen - NICHT das Kennwort!! - des Anbieters ein.
</p>""") }

# ----------------------------------------------------------------
help_form['training_iq_nummer'] = {
     'title'      : _(u'IQ-Nummer'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die IQ-Veranstaltungsnummer ein.
</p>""") }

# ----------------------------------------------------------------
help_form['training_intern_nummer'] = {
     'title'      : _(u'Interne Veranstaltungsnummer'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die interne Veranstaltungsnummer ein.
</p>""") }

# ----------------------------------------------------------------
help_form['training_anbieter'] = {
     'title'      : _(u'Anbieter'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Namen oder einen wesentlichen Teil des Namens des Anbieters ein.
</p>""") }

# ----------------------------------------------------------------
help_form['vorname'] = {
     'title'      : _(u'Vorname'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihren Vornamen ein.
</p>""") }

help_form['nachname'] = {
     'title'      : _(u'Nachname'),
     'help'       : _(u"""<p>
Geben Sie hier bitte Ihren Nachnamen an.
</p>""") }

help_form['personalnummer'] = {
     'title'      : _(u'Personalnummer'),
     'help'       : _(u"""<p>
Falls Sie beim Land Hessen beschäftigt sind, geben Sie hier bitte Ihre Personalnummer ein.
</p>""") }

help_form['strasse'] = {
     'title'      : _(u'Straße'),
     'help'       : _(u"""<p>
In welcher Straße wohnen Sie?
</p>""") }

help_form['plz'] = {
     'title'      : _(u'PLZ'),
     'help'       : _(u"""<p>
Wie lautet die PLZ Ihrer Wohnung?
</p>""") }

help_form['ort'] = {
     'title'      : _(u'Ort'),
     'help'       : _(u"""<p>
In welchem Ort wohnen Sie?
</p>""") }

help_form['telefon'] = {
     'title'      : _(u'Telefon'),
     'help'       : _(u"""<p>
Falls vorhanden tragen Sie hier bitte Ihre Telefonummer ein.
</p>""") }

help_form['email'] = {
     'title'      : _(u'E-Mail'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihre E-Mail-Adresse in.
</p>""") }

# ----------------------------------------------------------------
help_form['school_name'] = {
     'title'      : _(u'Dienststelle'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Namen Ihrer Schule/Dienststelle ein.
</p>""") }

help_form['school_ort'] = {
     'title'      : _(u'Dienstort'),
     'help'       : _(u"""<p>
In welchem Ort liegt Ihre Schule/Diensstelle?
</p>""") }

help_form['school_telefon'] = {
     'title'      : _(u'Telefon'),
     'help'       : _(u"""<p>
Falls bekannt, tragen Sie hier bitte die Telefonummer Ihrer Schule/Dienststelle ein.
</p>""") }

help_form['school_no'] = {
     'title'      : _(u'Dienststellennummer'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte die Dienststellennummer Ihrer Schule ein. Falls Sie an keiner
Schule beschäftigt sind, lassen Sie dieses Feld bitte frei.
</p>""") }

# ----------------------------------------------------------------
help_form['zusatz'] = {
     'title'      : _(u'Zusatzinformationen'),
     'help'       : _(u"""<p>
Tragen Sie die im Programm gegebenenfalls nachgefragten Informationen ein.
</p>""") }

help_form['uebernachtung'] = {
     'title'      : _(u'Übernachtung'),
     'help'       : _(u"""<p>
Benötigen Sie bei mehrtägigen Veranstaltungen eine Übernachtung?
</p>""") }

# ----------------------------------------------------------------
help_form['v_thema'] = {
     'title'      : _(u'Veranstaltungstitel'),
     'help'       : _(u"""<p>
Hier wird der Veranstaltungstitel angezeigt.
</p>""") }

help_form['v_iq_id'] = {
     'title'      : _(u'IQ-Veranstaltungsnummer'),
     'help'       : _(u"""<p>
Hier wird die Veranstaltungsnummer des IQ angezeigt.
</p>""") }

help_form['v_intern_id'] = {
     'title'      : _(u'Interne Veranstaltungsnummer'),
     'help'       : _(u"""<p>
Hier wird die interne Veranstaltungsnummer angezeigt.
</p>""") }

help_form['v_anbieter'] = {
     'title'      : _(u'Anbieter'),
     'help'       : _(u"""<p>
Hier wird der Anbieter dieser Veranstaltung angezeigt.
</p>""") }

help_form['v_datum'] = {
     'title'      : _(u'Datum'),
     'help'       : _(u"""<p>
Hier steht, wann die Veranstaltung stattfindet.
</p>""") }

help_form['v_punkte'] = {
     'title'      : _(u'Leistungspunkte'),
     'help'       : _(u"""<p>
Hier sehen Sie, wie viele Leistungspunkte mit dieser Veranstaltung erworben werden können.
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
Hier können Sie Eingaben vornehmen, die am häufigsten benötigt werden.
</p>""") }

help_form['tab_faecher'] = {
     'title'      : _(u'Fach/Volltextsuche'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie das Fach sowie gegebenenfalls einen passenden Suchbegriff fest.
</p>""") }

help_form['tab_gueltig'] = {
     'title'      : _(u'Region'),
     'info'       : _(u"""<p>
Legen Sie hier bitte den Gültigkeitsbereich der gewünschten Veranstaltungen fest: landesweit
bzw. Angebot für eine Bildungsregion.
</p>""") }

help_form['tab_schularten'] = {
     'title'      : _(u'Schulart'),
     'info'       : _(u"""<p>
Hier können Sie die gewünschte Schulart/Schulform auswählen. Um alle Schulformen
auszuwählen, verwenden Sie bitte "---".
</p>""") }

help_form['tab_zielgruppen'] = {
     'title'      : _(u'Zielgruppe'),
     'info'       : _(u"""<p>
Bitte wählen Sie die gewünschte Zielgruppe aus.
</p>""") }

help_form['tab_anbieter'] = {
     'title'      : _(u'Anbieter'),
     'info'       : _(u"""<p>
Hier finden Sie die Anbieter der Fortbildungsangebote.
</p>""") }

help_form['tab_anbieter2'] = {
     'title'      : _(u'Anbieter'),
     'info'       : _(u"""<p>
Hier können Sie die Auswahl der Veranstaltungen auf einen Anbieter beschränken.
</p>""") }

help_form['tab_weiteres'] = {
     'title'      : _(u'Weitere Optionen'),
     'info'       : _(u"""<p>
Hier finden Sie weitere Suchoptionen.
</p>""") }

help_form['tab_person'] = {
     'title'      : _(u'Zur Person'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte Ihre persönlichen Daten ein, die im Zusammenhang mit
Ihrer Online-Anmeldung benötigt werden.
</p>""") }

help_form['tab_school_person'] = {
     'title'      : _(u'Dienststelle/Person'),
     'info'       : _(u"""<p>
Tragen Sie hier bitte die für die Online-Anmeldung zwingend erforderlichen
Informationen zu Ihrer Dienststelle und Ihrer Person ein.
</p>
<p>
  <span class="red"><strong>··</strong></span>
  <a href="javascript:select_school_no(document.form_input.school_no)">Schule auswählen ...</a>
</p>""") }

help_form['tab_schule'] = {
     'title'      : _(u'Dienststelle'),
     'info'       : mark_safe(_(u"""<p>
Tragen Sie hier bitte die notwendigen Informationen zu Ihrer Schule/Dienststelle ein.
</p>
<p>
  <span class="red"><strong>··</strong></span>
  <a href="javascript:select_school_no(document.form_input.school_no)">Schule auswählen ...</a>
</p>
""")) }

help_form['tab_zusatz'] = {
     'title'      : _(u'Zusatzinformationen'),
     'info'       : _(u"""<p>
Tragen Sie hier gegebenenfalls nachgefragte Informationen ein.
</p>""") }

help_form['tab_veranstaltung'] = {
     'title'      : _(u'Veranstaltung'),
     'info'       : _(u"""<p>
Hier finden Sie noch einmal in kompakter Form Informationen zu Ihrer
ausgewählten Veranstaltung.
</p>""") }

help_form['tab_schule2'] = {
     'title'      : _(u'Schule'),
     'info'       : _(u"""<p>
Mit diesem Formular wählen Sie Ihre Schule aus.
</p>""") }

help_form['tab_person2'] = {
     'title'      : _(u'Zur Person'),
     'info'       : _(u"""<p>
Bitte überprüfen Sie Ihre persönlichen Daten.
</p>""") }

help_form['tab_schule2'] = {
     'title'      : _(u'Dienststelle'),
     'info'       : mark_safe(_(u"""<p>
Bitte überprüfen Sie die Angaben zu Ihrer Schule/Dienststelle.
</p>""")) }

help_form['tab_zusatz2'] = {
     'title'      : _(u'Zusatzinformationen'),
     'info'       : _(u"""<p>
Sind die eingetragenen Informationen korrekt?
</p>""") }

