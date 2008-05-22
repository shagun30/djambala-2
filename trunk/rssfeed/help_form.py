# -*- coding: utf-8 -*-
"""
/dms/rssfeed/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.07.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihres RSS-Feeds ein. Der Kurzname sollte den Inhalt
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
Tragen Sie hier die Überschrift Ihres RSS-Feeds ein. Unter dieser Überschrift wird 
Ihr Feed angezeigt.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Kurzbeschreibung'),
     'help'       : _(u"""<p>
Beschreiben Sie hier bitte kurz Ihren RSS-Feed. Diese Information
wird potentiellen Abonnenten als Beschreibung angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Verweis'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die Web-Adresse an, auf die sich dieser RSS-Feed
bezieht. Diese Adresse muss vollständig sein: <tt>http://...</tt>
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Art des Feeds'),
     'help'       : _(u"""<p>
Hier legen Sie fest, ob es sich um einen globalen oder
speziellen RSS-Feed handelt.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften Ihres RSS-Feeds fest.
</p>""") }

