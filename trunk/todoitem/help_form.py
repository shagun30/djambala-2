# -*- coding: utf-8 -*-
"""
/dms/todoitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Auftraege in To-Do-Liste
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.11.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Mein Name'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihren Vor- und Nachnamen ein. Anonyme Beiträge
sind nicht erwünscht.
</p>""") }

# ----------------------------------------------------------------
help_form['string_2'] = {
     'title'      : _(u'Meine E-Mail-Adresse'), 
     'help'       : _(u"""<p>
Geben Sie bitte für Rückfragen oder direkte Reaktionen Ihre
E-Mail-Adresse an.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihres Auftrags ein. Dieser Titel erscheint
in der Übersicht der To-Do-Liste.
</p>

<p>
Hinweis: Kurze Überschriften fördern die Lesbarkeit und verhindern 
störende Zeilenumbrüche.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die vollständige Web-Adresse an.
Vergessen Sie bitte nicht <tt>http://</tt>.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Hier beschreiben Sie Ihren Auftrag. Bitte geben Sie alle relevanten Informationen an.
</p>
<p>
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihr Auftrag angezeigt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften des Auftrags fest.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

