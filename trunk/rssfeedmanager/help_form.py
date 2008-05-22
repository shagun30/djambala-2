# -*- coding: utf-8 -*-
"""
/dms/rssfeedmanager/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte zur Verwaltung von RSS-Feeds
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
Tragen Sie hier den Kurznamen Ihrer Verwaltungsseite der RSS-Feeds ein.
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
Tragen Sie hier die Überschrift Ihrer Verwaltungsseite der RSS-Feeds ein.
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
help_form['text'] = {
     'title'      : _(u'Intro-Text'),
     'help'       : _(u"""<p>
Geben Sie hier bitte den Intro-Text zu den RSS-Feeds ein.
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
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
Hier legen Sie fest, bei welchem Zwischentitel Ihre Seite im
Ordner angezeigt wird.
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
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieser
Informationsseite fest.
</p>""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>""") }

