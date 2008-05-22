# -*- coding: utf-8 -*-
"""
/dms/faqitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer FAQ-Beitraege
         Django content Management System

Werner Fabian
w.fabian@afl.bildung.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------

help_form['string_1'] = {
     'title'      : _(u'Mein Name'), 
     'help'       : _(u"""<p>
Falls Sie eingeloggt sind, werden Ihre bekannten Daten übernommen, ansonsten tragen Sie hier bitte Ihren Vor- und Nachnamen ein. Anonyme Beiträge sind nicht erwünscht.
</p>""") }

# ----------------------------------------------------------------

help_form['string_2'] = {
     'title'      : _(u'Meine E-Mail-Adresse'), 
     'help'       : _(u"""<p>
Falls Sie eingeloggt sind, wird Ihre bekannte Adresse übernommen, ansonsten geben Sie bitte für Rückfragen oder direkte Reaktionen Ihre E-Mail-Adresse an.
</p>""") }

# ----------------------------------------------------------------

help_form['title'] = {
     'title'      : _(u'Betreff'), 
     'help'       : _(u"""<p>
Tragen Sie hier den Betreff Ihres FAQ-Beitrags ein.
</p>

<p>
Hinweis: Bei einem kürzen Betreff können Sie eher davon ausgehen,
dass Ihr Beitrag gelesen wird.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Frage'),
     'help'       : _(u"""<p>
Geben Sie hier bitte Ihre Frage ein. Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Antwort'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die Antwort ein.
</p>
<p>
Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['moderated_text'] = {
      'title': _(u'Moderierte FAQ-Liste'),
      'info' : _(u"""<p>
<b>Diese FAQ-Liste ist moderiert. Ihr neuer Beitrag wird erst
angezeigt, nachdem ihn die zuständige Person freigegeben hat.</b>
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie Ihren Beitrag fest.
</p>""") }

# ----------------------------------------------------------------

help_form['section'] = {
     'title'      : _(u'Zuordnung in der FAQ-Liste'),
     'help'       : _(u"""<p>
Hier legen Sie fest, unter welchem Zwischentitel Ihr FAQ-Beitrag in der
<b>übergeordneten</b> FAQ-Liste angezeigt wird. Bei Bedarf können 
Sie später mit der Aktion "umordnen" Ihren FAQ-Beitrag weiter nach oben
oder nach unten verschieben.
</p>""") }

