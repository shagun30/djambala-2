# -*- coding: utf-8 -*-
"""
/dms/eduwebquestitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Webquests in Lernarchiven
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Webquests ein. Dieser Kurzname wird beim Aufrufen 
in der Web-Adresse verwendet. Der Kurzname sollte den Inhalt
möglichst präzise beschreiben und gleichzeitig möglichst kurz
sein.
</p>

<p>
Beim Aufrufen der Seiten wird zwischen Groß- und Kleinschreibung unterschieden. Bitte
verwenden Sie beim Kurznamen ausschließlich Kleinbuchstaben. Leerzeichen werden durch
einen Unterstrich, Umlaute durch "ae", "oe" usw. ersetzt.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die vollständige Web-Adresse an.
Vergessen Sie bitte nicht <tt>http://</tt>.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift des Webquest ein. Unter dieser Überschrift wird 
der Webquest angezeigt. Dieser Titel erscheint ebenfalls im übergeordneten
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
Falls erforderlich tragen Sie hier die Unterüberschrift Ihres Webquest ein.
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Kurzbeschreibung'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld beschreiben Sie Ihren Webquest. Dieser Kommentar
wird auf der Übersichtsseite im Lernarchiv angezeigt.
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
Bei Bedarf können Sie links neben Ihrem Text ein Bild anzeigen lassen.
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
help_form['schlagwort'] = {
     'title'      : _(u'Schlagworte'),
     'help'       : _(u"""<p>
Bitte geben Sie - jeweils in einer <b>eigenen Zeile</b> - zu Ihrer Lernressource
passende Schlagworte an. Bitte berücksigen Sie folgende Hinweise:
</p>
<ul>
<li>Die Schlagworte sollten möglichst kurz sein.</li>
<li>Schlagworte sollten in der Regel aus <b>einem</b> Wort bestehen.</li>
<li>In aller Regel sollten Sie die Einzahl des jeweiligen Begriffs verwenden.</li>
</ul>""") }

# ----------------------------------------------------------------
help_form['fach_sachgebiet'] = {
     'title'      : _(u'Fach/Sachgebiet(e)'),
     'help'       : _(u"""<p>
Bitte wählen Sie das passende Fach bzw.Sachgebiet aus. Sie können auch mehrere
Fächer bzw. Sachgebiete ankreuzen.
</p>""") }

# ----------------------------------------------------------------
help_form['lernrestyp'] = {
     'title'      : _(u'Materialtyp'),
     'help'       : _(u"""<p>
Hier legen Sie die Art des Materialtyps fest.
</p>""") }

# ----------------------------------------------------------------
help_form['medienformat'] = {
     'title'      : _(u'Medienformat'),
     'help'       : _(u"""<p>
Bitte geben Sie das Medienformat an.
</p>""") }

# ----------------------------------------------------------------
help_form['titel_lang'] = {
     'title'      : _(u'Schülertitel'),
     'help'       : _(u"""<p>
Geben Sie hier bitte einen kurzen Titel für die Schülerinnen und Schüler ein.
Gegebenenfalls können Sie dieses Feld auch freilassen.
</p>
""") }

# ----------------------------------------------------------------
help_form['beschreibung_lang'] = {
     'title'      : _(u'Beschreibung für Schüler/innen'),
     'help'       : _(u"""<p>
Beschreiben Sie hier in verständlicher Sprache die Lernressource.
</p>""") }

# ----------------------------------------------------------------
help_form['alter_min'] = {
     'title'      : _(u'Geeignet für Klasse (min)'),
     'valign'     : False,
     'help'       : _(u"""<p>
Geben Sie hier bitte die Klasse an, ab der diese Ressource geeignet ist.
(0=ohne Altersangabe, V=Vorschule/Kindergarten, E=Erwachsenbildung)
</p>
""") }

help_form['alter_max'] = {
     'title'      : _(u'Geeignet für Klasse (max)'),
     'valign'     : False,
     'help'       : _(u"""<p>
Geben Sie hier bitte die Klasse an, bis zu der diese Ressource geeignet ist.
(0=ohne Altersangabe, V=Vorschule/Kindergarten, E=Erwachsenbildung)
</p>
""") }

# ----------------------------------------------------------------
help_form['has_user_support'] = {
     'title'      : _(u'Beiträge von außen'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob Beiträge von auß
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
help_form['fach'] = {
     'title'      : _(u'Fach'),
     'help'       : _(u"""<p>
Wählen Sie bitte das passende Fach bzw. Berufsfeld aus.
</p>""") }

# ----------------------------------------------------------------
help_form['sprache'] = {
     'title'      : _(u'Sprache'),
     'help'       : _(u"""<p>
Bitte geben Sie die Sprache an, in der die Lernressource geschrieben wurde.
Falls es sich um eine mehrsprachige Ressource handelt, verwenden Sie
bitte pro Sprache eine eigene Zeile.
</p>""") }

# ----------------------------------------------------------------
help_form['lernziel'] = {
     'title'      : _(u'Lernziel(e)'),
     'help'       : _(u"""<p>
Hier beschreiben Sie Lernziele, die mit dieser Lernressource angestrebt
werden.
</p>""") }

# ----------------------------------------------------------------
help_form['lernzeit'] = {
     'title'      : _(u'Lernzeit'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die ungefähr benötigte Lernzeit an.
Dieses Feld kann aber auch leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['methodik'] = {
     'title'      : _(u'Methodik'),
     'help'       : _(u"""<p>
Hier geben Sie methodische Hinweise, wie mit dieser Lernressource umgegangen
werden kann bzw.sollte.
</p>""") }

# ----------------------------------------------------------------
help_form['lehrplan'] = {
     'title'      : _(u'Lehrplanbezug'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte Hinweise zu den passenden Lehrplänen ein. Idealerweise
geben Sie die genauen Verweise an.
</p>""") }

# ----------------------------------------------------------------
help_form['standards_kmk'] = {
     'title'      : _(u'Standards (KMK)'),
     'help'       : _(u"""<p>
Geben Sie hier bitte Hinweise zu den KMK-Standards.
</p>""") }

# ----------------------------------------------------------------
help_form['standards_weitere'] = {
     'title'      : _(u'Standards (weitere)'),
     'help'       : _(u"""<p>
Hier können Sie zu weiteren Standards Hinweise geben.
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
help_form['zielgruppe'] = {
     'title'      : _(u'Zielgruppe(n)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Zielgruppe(n) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['autor'] = {
     'title'      : _(u'Autor/in'),
     'help'       : _(u"""<p>
Falls bekannt geben Sie hier bitte die Autorin bzw. den Autor
der Lernressource an. Dieses Feld kann auch leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['herausgeber'] = {
     'title'      : _(u'Herausgeber/in'),
     'help'       : _(u"""<p>
Falls bekannt tragen Sie hier bitte die Herausgeberin bzw. den Herausgeber
der Lernressource ein. Dieses Feld kann auch leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['publikations_datum'] = {
     'title'      : _(u'Publikationsdatum'),
     'help'       : _(u"""<p>
Falls bekannt tragen Sie hier bitte das Publikationsdatum
der Lernressource ein. Dieses Feld kann auch leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['isbn'] = {
     'title'      : _(u'ISBN'),
     'help'       : _(u"""<p>
Falls vorhanden tragen Sie hier bitte die ISBN
der Lernressource ein. Dieses Feld wird in der Regel leer bleiben.
</p>""") }

# ----------------------------------------------------------------
help_form['rechte'] = {
     'title'      : _(u'Rechte/Nutzungsbedingungen'),
     'help'       : _(u"""<p>
Geben Sie hier an, unter welchen Bedingungen die Lernressource
genutzt werden kann.
</p>""") }

# ----------------------------------------------------------------
help_form['schulart'] = {
     'title'      : _(u'Schulart(en)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Schulart(en) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['schulstufe'] = {
     'title'      : _(u'Schulstufe(n)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Schulstufe(n) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['anbieter_herkunft'] = {
     'title'      : _(u'Anbieter/Herkunft'),
     'help'       : _(u"""<p>
Wer bietet die entsprechende Lernressource an?
</p>""") }

# ----------------------------------------------------------------
help_form['preis'] = {
     'title'      : _(u'Preis'),
     'help'       : _(u"""<p>
Was kostet die Lernressource?
</p>""") }

# ----------------------------------------------------------------
help_form['techn_voraus'] = {
     'title'      : _(u'Technische Voraussetzungen'),
     'help'       : _(u"""<p>
Ist die Nutzung der Lernressource an spezielle technische Voraussetzungen
gebunden?
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
Webquests fest.
</p>""") }

help_form['tab_pupil'] = {
     'title'      : _(u'Schüler/innen'),
     'info'       : _(u"""<p>
Materialien, die für Schüler/innen geeignet sind, können hier beschrieben werden.
</p>""") }

help_form['tab_description'] = {
     'title'      : _(u'Beschreibung'),
     'info'       : _(u"""<p>
Hier können Sie die Lernressource genauer beschreiben.
</p>""") }

help_form['tab_course'] = {
     'title'      : _(u'Fach'),
     'info'       : _(u"""<p>
Hier legen Sie fest, welchem Fach bzw. welchen Fächern Ihre
Lernressource zugeordnet wird.
</p>""") }

help_form['tab_details'] = {
     'title'      : _(u'Zuordnung'),
     'info'       : _(u"""<p>
Hier ordnen Sie die Lernressource verschiedenen Dimensionen zu.
</p>""") }

help_form['tab_paed'] = {
     'title'      : _(u'Didaktik'),
     'info'       : _(u"""<p>
Hiermit können Sie didaktisch-methodische Anmerkungen speichern.
</p>""") }

help_form['tab_formal'] = {
     'title'      : _(u'Formales'),
     'info'       : _(u"""<p>
Bei Bedarf tragen Sie hier formale Angaben ein.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihren Webquest mit einem kleinen Bild versehen.
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
Sie können die Sichtbarkeit des Webquest auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_user_support'] = {
     'title'      : _(u'Ergänzungen'),
     'info'       : _(u"""<p>
Hier legen Sie fest, ob von außen Dateien eingestellt werden dürfen.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

