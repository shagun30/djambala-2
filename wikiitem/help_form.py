# -*- coding: utf-8 -*-
"""
/dms/wikiitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Nachrichten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.03.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'), 
     'help'       : _(u"""<p>
Dieser Name wird für die Wiki-Seite verwendet.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift/Titel'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihres Wiki-Seite ein.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Untertitel'), 
     'help'       : _(u"""<p>
Falls erforderlich geben Sie hier bitte Ihren Untertitel ein.
</p>
""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Hier geben Sie bitte den Inhalt Ihrer Wiki-Seite ein.
</p>
<p>
Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
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
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular geben Sie Ihre Wiki-Seite ein.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihre Wiki-Seite mit einem kleinen Bild schmücken.
</p>""") }

help_form['moderated_text'] = {
      'title': _(u'Moderiertes Wiki'),
      'info' : _(u"""<p>
<b>Dieses Wiki ist moderiert. Ihre neue Seite wird erst
angezeigt, nachdem die zuständige Person Sie freigegeben hat.</b>
</p>""") }
