# -*- coding: utf-8 -*-
"""
/dms/edufileitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Dateien in Lernarchiven
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Dateiname'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte die Datei aus, die Sie auf den Server
übertragen möchten.
</p>

<p>
Falls also bereits ein Objekt gleichen Namens in dem entsprechenden Ordner auf dem
Server existieren sollte, kann auf dem Server keine Datei angelegt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihrer Datei ein. Dieser Titel erscheint
in der Übersicht des Lernarchivs.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Zusammenfassung'),
     'help'       : _(u"""<p>
Der hier eingegebene Text erscheint in der Übersicht des Lernarchivs.
Er sollte deshalb die Inhalte Ihrer Datei knapp und präzise beschreiben.
</p>
<p>
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier gegebenenfalls die vollständige Web-Adresse
für weiterführende Informationen an.
Vergessen Sie bitte nicht <tt>http://</tt>.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more_extern'] = {
     'title'      : _(u'Eigenes Fenster'),
     'help'       : _(u"""<p>
Mit diesem Auswahlfeld legen Sie fest, dass die Datei in einem eigenen Fenster
angezeigt werden soll.
</p>""") }

# ----------------------------------------------------------------
help_form['image_url'] = {
     'title'      : _(u'Schmuckbild'),
     'help'       : _(u"""<p>
Bei Bedarf können Sie links neben Ihrem Text ein Bild anzeigen lassen.
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
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Text angezeigt wird.
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
help_form['fach_sachgebiet'] = {
     'title'      : _(u'Fach/Sachgebiet(e)'),
     'help'       : _(u"""<p>
Bitte wählen Sie das passende Fach bzw.Sachgebiet aus. Sie können auch mehrere
Fächer bzw. Sachgebiete ankreuzen.
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
Mit diesem Formular legen Sie die wichtigsten Eigenschaften des Textdokuments fest.
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
Sie können Ihren Verweis mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_update'] = {
     'title'      : _(u'Upload'),
     'info'       : _(u"""<p>
Hier können Sie die auf dem Server vorhandene Datei ersetzen.<br />
<b>Achtung:</b> Die von Ihnen ausgewählte Datei muss den gleichen Namen wie die
Datei auf dem Server haben.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

