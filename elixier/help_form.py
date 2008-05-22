# -*- coding: utf-8 -*-
"""
/dms/elixier/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Elixier-Verwaltungsprogramm
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  16.01.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres Elixier-Verwaltungprogramms ein. Dieser Kurzname wird beim Aufrufen
des Elixier-Verwaltungprogramms in der Web-Adresse verwendet. Der Kurzname sollte den Inhalt
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
Tragen Sie hier die Überschrift Ihres Elixier-Verwaltungprogramms ein. Unter dieser
Überschrift wird  Ihre Seite angezeigt. Dieser Titel erscheint ebenfalls in der
Übersicht des Ordners, der Ihre Seite enthält.
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
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Geben Sie hier bitte einen einführenden Text für Ihr Elixier-Verwaltungprogramm ein.
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Erweiterungstext'),
     'help'       : _(u"""<p>
Hier können Sie bei Bedarf zusätzliche Informationen eintragen.
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
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Elixier-Verwaltungprogramm im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['bildungsebene'] = {
     'title'      : _(u'Bildungsebene'),
     'help'       : _(u"""<p>
Wählen Sie bitte das passende Bildungsebene aus.
</p>""") }

# ----------------------------------------------------------------
help_form['fach_sachgebiet'] = {
     'title'      : _(u'Fach/Sachgebiet'),
     'help'       : _(u"""<p>
Wählen Sie bitte das passende Fach/Sachgebiet aus.
</p>""") }

# ----------------------------------------------------------------
help_form['medienformat'] = {
     'title'      : _(u'Medienformat'),
     'help'       : _(u"""<p>
Wählen Sie bitte das passende Medienformat aus.
</p>""") }

# ----------------------------------------------------------------
help_form['quelle'] = {
     'title'      : _(u'Quelle'),
     'help'       : _(u"""<p>
Wählen Sie bitte die passende Quelle aus.
</p>""") }

# ----------------------------------------------------------------
help_form['schlagwort'] = {
     'title'      : _(u'Schlagwort'),
     'help'       : _(u"""<p>
Geben Sie bitte das passende Schlagwort ein.
</p>""") }

# ----------------------------------------------------------------
help_form['status'] = {
     'title'      : _(u'Status'),
     'help'       : _(u"""<p>
Sie können einen Beitrag annehmen, unbearbeitet lassen oder ablehnen.
</p>""") }

# ----------------------------------------------------------------
help_form['dest_folder'] = {
     'title'      : _(u'Zielordner'),
     'help'       : _(u"""<p>
In diesem Feld legen Sie den Zielordner für den Elixier-Import fest.
Bitte verwenden Sie unbedingt den obigen Verweis "Zielordner festlegen".
Gegebenenfalls müssen Sie das <i>Cooky</i> "elixier_dest_folder" löschen.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften des
Elixier-Verwaltungprogramms fest.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihr Elixier-Verwaltungprogramm mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>""") }

help_form['tab_bildungsebene'] = {
     'title'      : _(u'Bildungsebene'),
     'info'       : _(u"""<p>
Hier legen Sie die Bildungsebene fest.
</p>""") }

help_form['tab_fach_sachgebiet'] = {
     'title'      : _(u'Fach/Sachgebiet'),
     'info'       : _(u"""<p>
Hier legen Sie das Fach/Sachgebiet fest.
</p>""") }

help_form['tab_medienformat'] = {
     'title'      : _(u'Medienformat'),
     'info'       : _(u"""<p>
Hier können Sie das Medienformat festlegen.
</p>""") }

help_form['tab_quelle'] = {
     'title'      : _(u'Quelle'),
     'info'       : _(u"""<p>
Hier können Sie die Quelle der Beiträge festlegen.
</p>""") }

help_form['tab_schlagwort'] = {
     'title'      : _(u'Schlagwort'),
     'info'       : _(u"""<p>
Hier können Sie einen Suchbegriff festlegen.
</p>""") }

help_form['tab_status'] = {
     'title'      : _(u'Status des Beitrags'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie den Status des Beitrags fest.
</p>""") }
