# -*- coding: utf-8 -*-
"""
/dms/userchangemanagement/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die User_verwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.06.2007  Beginn der Arbeit
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
Tragen Sie hier die Überschrift zur Verwaltung der eigenen User-Daten ein. Unter dieser
Überschrift wird die User-Verwaltung angezeigt. Dieser Titel erscheint ebenfalls
im übergeordneten Ordner.
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
Hier können Sie ein Intro eingeben. Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Erweiterungstext'),
     'help'       : _(u"""<p>
Falls erforderlich können Sie den Intro-Text ausführlicher gestalten.
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
help_form['section'] = {
     'title'      : _(u'Zuordnung beim <i>übergeordneten</i> Ordner'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel die User-Verwaltung im
<b>übergeordneten</b> Ordner angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihre User-Verwaltung weiter nach oben
oder nach unten verschieben.
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
help_form['email'] = {
     'title'      : _(u'E-Mail-Adresse'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihre E-Mail-Adresse ein. Wichtig: Diese
E-Mail-Adresse muss wirklich existieren, da Community-Mitglieder
mit falschen E-Mail-Adressen periodisch gelöscht werden.
</p>""") }

# ----------------------------------------------------------------
help_form['password1'] = {
     'title'      : _(u'Neues Kennwort'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihr neues Kennwort ein.
</p>
<ul>
<li>Beim Eintippen werden anstelle der Buchstaben Sternchen angezeigt.</li>
<li>Das Kennwort muss mindestens sechs Zeichen lang sein.</li>
<li>Verwenden Sie bitte niemals Ihren Vor- bzw. Nachnamen als Kennwort!</li>
<li>Auch die Vornamen Ihrer Liebsten eignen sich nicht als Kennwort!</li>
<li>Sie sollten aus Sicherheitsgründen zumindest ein Zeichen groß schreiben.</li>
<li>Wir empfehlen, mindestens eine Ziffer in das Kennwort zu integrieren.</li>
</ul>
""") }

help_form['password2'] = {
     'title'      : _(u'Neues Kennwort wiederholen'),
     'help'       : _(u"""<p>
Falls Sie Ihr Kennwort ändern möchten, müssen Sie hier
aus Sicherheitsgründen das obige Kennwort noch einmal eingeben.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften fest.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können die User-Daten-Verwaltungsseite mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_email'] = {
     'title'      : _(u'E-Mail-Adresse'),
     'info'       : _(u"""<p>
Falls erforderlich können Sie hier Ihre neue E-Mail-Adresse eintragen.
</p>""") }

help_form['tab_password'] = {
     'title'      : _(u'Kennwort'),
     'info'       : _(u"""<p>
Hier können Sie sich ein neues Kennwort geben. Falls Sie die Felder
leer lassen, gilt weiterhin Ihr bisherigen Kennwort. Um Tippfehler zu vermeiden,
müssen Sie das neue Kennwort zweimal eingeben.
</p>""") }

