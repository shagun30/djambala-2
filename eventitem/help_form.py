# -*- coding: utf-8 -*-
"""
/dms/eventitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Termine
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.06.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['visible_start'] = {
    'title'      : _(u'Beginn des Termins'),
    'help':_(u"""<p>
Dieses Feld legt fest, wann Ihr Termin beginnt.
</p>""") }

# ----------------------------------------------------------------
help_form['visible_end'] = {
    'title'      : _(u'Ende des Termins'),
    'help'       : _(u"""<p>
Dieses Feld legt fest, wann Ihr Termin endet.
</p>""") }

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
     'title'      : _(u'Überschrift/Titel'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihres Beitrags ein.
</p>

<p>
Hinweis: Bei einem kürzen Titel können Sie eher davon ausgehen,
dass Ihr Termin gelesen wird.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Untertitel'), 
     'help'       : _(u"""<p>
Falls erforderlich geben Sie hier bitte Ihren Untertitel ein.
</p>
""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einer Rubrik'),
     'help'       : _(u"""<p>
Hier legen Sie fest, welcher Rubrik Ihr Termin zugeordnet wird.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Zusammenfassung'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die Zusammenfassung Ihres Termins ein. Dieser Text wird
in der Übersicht des Terminkalenders angezeigt.
</p>
<p>
Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Termin'),
     'help'       : _(u"""<p>
Geben Sie hier bitte den "Rest" Ihres Termins ein. Gegebenenfalls können
Sie dieses Textfeld auch leer lassen.
</p>
<p>
Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die vollständige Web-Adresse an, für weitergehende
Informationen an. Vergessen Sie bitte nicht <tt>http://</tt>.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more_extern'] = {
     'title'      : _(u'Eigenes Fenster'),
     'help'       : _(u"""<p>
Mit diesem Auswahlfeld legen Sie fest, dass der Verweis in einem eigenen Fenster
angezeigt werden soll. Verweise außerhalb dieses Servers werden immer in
einem eigenen Fenster geöffnet.
</p>""") }

# ----------------------------------------------------------------
help_form['image_url'] = {
     'title'      : _(u'Schmuckbild'),
     'help'       : _(u"""<p>
Bei Bedarf können Sie links neben Ihrem Beitrag ein Bild anzeigen lassen.
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
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular geben Sie Ihren Termin ein.
</p>""") }

help_form['tab_text'] = {
     'title'      : _(u'Termintext'),
     'info'       : _(u"""<p>
Tragen Sie hier "den Rest" Ihres Termins ein.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihre Informationsseite mit einem kleinen Bild schmücken.
</p>""") }

help_form['moderated_text'] = {
      'title': _(u'Moderierter Terminkalender'),
      'info' : _(u"""<p>
<b>Dieser Terminkalender ist moderiert. Ihr neuer Termin wird erst
angezeigt, nachdem die zuständige Person diesen freigegeben hat.</b>
</p>""") }
