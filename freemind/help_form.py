# -*- coding: utf-8 -*-
"""
/dms/freemind/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Informationsseiten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.03.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['fname'] = {
     'title'      : _(u'Freemind-Datei'),
     'help'       : _(u"""<p>
Wählen Sie bitte auf Ihrer Festplatte die Freemind-Datei aus, die Sie auf den Server
übertragen möchten.
</p>

<p>
Der Dateiname Ihrer Freemind-Datei (ohne .mm) ist zugleich der Kurzname auf dem Server. Falls also bereits
ein Objekt gleichen Namens in dem entsprechenden Ordner auf dem Server existieren sollte,
kann auf dem Server keine Datei angelegt werden!
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihrer Freemind-Datei ein. Mit dieser Überschrift wird
Ihre Maindmap in der Übersicht des Ordners angezeigt.
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
In der Regel bleibt dieses Feld aber leer.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Text'),
     'help'       : _(u"""<p>
Geben Sie hier bitte die Beschreibung Ihrer Mindmap ein.
Ihnen stehen dabei die wichtigsten Möglichkeiten eines Editors zur Verfügung. 
Wenn Sie die Maus längere Zeit über die Symbole halten, werden in kleinen
Fenstern erläuternde Informationen angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Intro - "Mehr ..."'),
     'help'       : _(u"""<p>
Mit diesem Eingabefeld können Sie eine ausführlichere Beschreibung
anbieten, der automatisch mit "Mehr ..." aufrufbar ist.
</p>""") }

# ----------------------------------------------------------------
help_form['url_more'] = {
     'title'      : _(u'Web-Adresse'),
     'help'       : _(u"""<p>
Geben Sie hier gegebenenfalls die vollständige Web-Adresse
für weiterführende Informationen an.
Vergessen Sie bitte nicht <tt>http://</tt>.
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
Bei Bedarf können Sie rechts neben Ihrem Text ein Bild anzeigen lassen.
Da Sie hier die Web-Adresse (http://..) des Bildes angeben, muss sich dieses Bild bereits 
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
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihre Datei im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------
help_form['has_comments'] = {
     'title'      : _(u'Kann kommentiert werden'),
     'help'       : _(u"""<p>
Dieser Schalter legt fest, ob diese Datei kommentiert werden kann
bzw. darf. In der Regel wird diese Option ausgeschaltet.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften des Freemind-Players fest.
Sie können die Mindmap ein-, ausfalten sowie drucken. Änderungen sind aber nicht möglich!
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihre Dateibeschreibung mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_update'] = {
     'title'      : _(u'Upload'),
     'info'       : _(u"""<p>
Hier können Sie die auf dem Server vorhandene Datei ersetzen.<br />
<b>Achtung:</b> Die von Ihnen ausgewählte Datei muss den gleichen Namen wie die
Datei auf dem Server haben.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Weiteres'),
     'info'       : _(u"""<p>
Hier finden Sie Optionen, die eher selten gebraucht werden.
</p>""") }

