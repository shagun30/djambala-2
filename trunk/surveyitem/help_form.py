# -*- coding: utf-8 -*-
"""
/dms/surveyitem/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Fragen-Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.01.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Sie können dieses Feld normalerweise freilassen. Es wird nur benötigt, wenn
Community-Informationen automatisch eingetragen werden sollen. In diesem Fall
müssen Sie einen der folgenden Namen verwenden: <tt>sex, first_name, last_name,
title, email, username, organisation, sub_organisation, street, zip, town, homepage</tt>
</p>""") }

# ----------------------------------------------------------------
help_form['string_1'] = {
     'title'      : _(u'Typ der Frage'), 
     'help'       : _(u"""<p>
In diesem Feld wird der Typ der Frage gespeichert. Dieser kann nachträglich nicht
geändert werden.
</p>""") }

# ----------------------------------------------------------------
help_form['title'] = {
     'title'      : _(u'Frage (Kurzfassung)'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihre (möglichst kurze) Frage ein.
</p>""") }

# ----------------------------------------------------------------
help_form['sub_title'] = {
     'title'      : _(u'Erläuterung'), 
     'help'       : _(u"""<p>
Tragen Sie hier bitte Ihre komplette Frage ein. Gegebenenfalls können Sie dieses
Feld auch leer lassen.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Optionen'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte jeweils in einer Zeile die möglichen Optionen ein.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Default'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte gegebenenfalls die Vorbelegung des Eingabefeldes ein.
</p>""") }

# ----------------------------------------------------------------
help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Reiter'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Reiter Ihre Frage angezeigt werden soll.
Die Frage kann später bei Bedarf umgeordnet werden.
</p>""") }

# ----------------------------------------------------------------
help_form['integer_1'] = {
     'title'      : _(u'Muss-Feld'),
     'help'       : _(u"""<p>
Hier legen Sie fest, ob diese Frage beantwortet werden muss oder nicht.
</p>""") }

# ----------------------------------------------------------------
help_form['integer_2'] = {
     'title'      : _(u'Max. Zeichen'),
     'help'       : _(u"""<p>
Wie viele Zeichen dürfen maximal eingegeben werden?
</p>""") }

# ----------------------------------------------------------------
help_form['integer_3'] = {
     'title'      : _(u'Breite'),
     'help'       : _(u"""<p>
Wie breit soll das Eingabefeld sein?
</p>""") }

# ----------------------------------------------------------------
help_form['integer_4'] = {
     'title'      : _(u'Spalten'),
     'help'       : _(u"""<p>
Wie viele Spalten soll das Eingabefeld haben?
</p>""") }

# ----------------------------------------------------------------
help_form['integer_5'] = {
     'title'      : _(u'Zeilen'),
     'help'       : _(u"""<p>
Wie viele Zeilen soll das Eingabefeld haben?
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die Eigenschaften Ihrer Frage fest.
</p>""") }
