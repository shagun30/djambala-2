# -*- coding: utf-8 -*-
"""
/dms/pinitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Pinnwand-Beitraege
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.07.2007  Beginn der Arbeit
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
     'title'      : _(u'Betreff'), 
     'help'       : _(u"""<p>
Tragen Sie hier den Betreff Ihres Beitrags ein.
</p>

<p>
Hinweis: Bei einem kürzen Betreff können Sie eher davon ausgehen,
dass Ihr Beitrag gelesen wird.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Beitrag'),
     'help'       : _(u"""<p>
Geben Sie hier bitte Ihren Beitrag ein. Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

help_form['moderated_text'] = {
      'title': _(u'Moderierte Pinnwand'),
      'info' : _(u"""<p>
<b>Diese Pinnwand ist moderiert. Ihr neuer Beitrag wird erst
angezeigt, nachdem ihn die zuständige Person freigegeben hat.</b>
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, welcher Rubrik Ihr Beitrag zugeordnet wird.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie Ihren Beitrag fest.
</p>""") }

