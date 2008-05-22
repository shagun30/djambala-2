# -*- coding: utf-8 -*-
"""
/dms/photo/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Photos
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.10.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Dateiname'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte das Photo bzw. die Grafik aus, die Sie auf den Server
übertragen möchten.
</p>

<p>
Der Dateiname Ihres Photos ist zugleich der Kurzname auf dem Server. Falls also bereits
ein Objekt gleichen Namens in der Galerie auf dem Server existieren sollte,
kann auf dem Server keine Datei angelegt werden!
</p>

<p>
Aus dem übertragenen Bild werden gegebenenfalls zwei kleinere Bilddateien erzeugt.
</p>""") }

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Photograph/in'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte den Namen der Photografin bzw. des Photographen ein.
</p>""") }

# ----------------------------------------------------------------
help_form['string_2'] = {
     'title'      : _(u'E-Mail-Adresse Photograph/in'),
     'help'       : _(u"""<p>
Geben Sie bitte für Rückfragen oder direkte Reaktionen die
E-Mail-Adresse an.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Titel'),
     'help'       : _(u"""<p>
Tragen Sie hier den Titel Ihres Beitrags ein.
</p>

<p>
Hinweis: Bei einem kürzen Betreff können Sie eher davon ausgehen,
dass Ihr Beitrag angeschaut wird.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Beschreibung'),
     'help'       : _(u"""<p>
Geben Sie hier bitte eine Beschreibung zu Ihrem Photo, Ihrer Grafik ein. Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Erweiterte Beschreibung'),
     'help'       : _(u"""<p>
Hier k&oouml;nnen Sie die Beschreibung Ihres Photo, Ihrer Grafik erweitern. Ihnen stehen dabei die wichtigsten
Möglichkeiten eines Editors zur Verfügung. Wenn Sie die Maus 
längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

help_form['moderated_text'] = {
      'title': _(u'Moderierte Galerie'),
      'info' : _(u"""<p>
<b>Diese Galerie ist moderiert. Ihr neuer Beitrag wird erst
angezeigt, nachdem ihn die zuständige Person freigegeben hat.</b>
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Ausstellungsraum'),
     'help'       : _(u"""<p>
Hier legen Sie fest, in welchem Raum Ihr Beitrag ausgestellt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie Eigenschaften Ihren Photos fest.
</p>""") }

