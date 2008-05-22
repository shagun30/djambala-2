# -*- coding: utf-8 -*-
"""
/dms/search_xapian/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer die Volltextsuche
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.05.2007  Beginn der Arbeit
0.02  25.09.2007  Zielgruppe
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------
help_form['query'] = {
     'title'      : _(u'Suchbegriff'),
     'help'       : _(u"""<p>
Tragen Sie bitte die gewünschten Suchbegriffe ein. Sofern Sie zwischen
den Suchbegriffen keine Suchverknüpfung (and, or ..) einfügen, müssen
alle Begriffe auf der Seite vorkommen.
</p>

<p>
Es wird nicht zwischen Groß- und Kleinschreibung unterschieden. Wenn Sie
"Schule" eingeben, sollten auch alle Seiten, auf denen "Schulen" vorhanden ist,
gefunden werden. - Dieses "Stemming" funktioniert gut, aber leider nicht immer
perfekt!
</p>

<ul>
<li>
  <b>AND</b> schränkt den Suchhorizont ein, da alle mit "und" verknüpften
  Begriffe auf der betreffenden Seite vorkommen müssen.
</li>
<li>
  <b>OR</b> erweitert den Suchhorizont, da mindetens einer der Begriffe auf der
  Seite vorkommen muss - es dürfen aber auch beide Begriffe erscheinen.
</li>
<li>
  <b>*</b> darf als <i>Wildcard</i> oder Joker am Ende eines Begriffs verwendet
  werden. Beispiel: <tt>schul*</tt> findet u.a. Schule, Schulbildung, schulische ...
</li>
<li>
  <b>NOT</b> verlangt, dass das betreffende Wort nicht auf der Seite
  vorkommen darf.
</li>
<li>
  <b>Klammern</b> erlauben komplexere Suchanfragen.
</li>
<li>
  <b>NEAR</b> fordert, das die verknüpften Begriffe eng zusammenstehen. "Eng"
  bedeutet, dass höchstens neun andere Wörter dazwischen stehen dürfen.
</li>
<li>
  <b>Satzteile</b> können gefunden werden, wenn Sie in Anführungszeichen
  gesetzt werden.
</li>
<li>
  <b>+</b> und <b>-</b> müssen zusammen verwendet werden. Plus-Terme müssen
  vorhanden sein, während Minus-Terme nicht auf der gleichen Seite erscheinen dürfen.
</li>
</ul>
""") }

# ----------------------------------------------------------------
help_form['sort_by'] = {
     'title'      : _(u'Sortierung nach'),
     'help'       : _(u"""<p>
Hier legen Sie fest, wie die Suchergebnisse sortiert werden sollen.
</p>
""") }

# ----------------------------------------------------------------
help_form['domain'] = {
     'title'      : _(u'Suchhorizont'),
     'help'       : _(u"""<p>
Sie können den Suchhorizont von 'alle Seiten' auf Ihre
aktuelle Domaine einschränken.
</p>
""") }

# ----------------------------------------------------------------
help_form['zielgruppe'] = {
     'title'      : _(u'Zielgruppe(n)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Zielgruppe(n) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['schulart'] = {
     'title'      : _(u'Schulart(en)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Schulart(en) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['sprache'] = {
     'title'      : _(u'Sprache(n)'),
     'help'       : _(u"""<p>
Bitte geben Sie die Sprache an, in der die Lernressource geschrieben sein soll.
</p>""") }

# ----------------------------------------------------------------
help_form['fach'] = {
     'title'      : _(u'Fach/Sachgebiet(e)'),
     'help'       : _(u"""<p>
Bitte wählen Sie das passende Fach bzw.Sachgebiet aus. Sie können auch mehrere Fächer bzw. Sachgebiete ankreuzen.
</p>""") }

# ----------------------------------------------------------------
help_form['schulstufe'] = {
     'title'      : _(u'Schulstufe(n)'),
     'help'       : _(u"""<p>
Bitte wählen Sie die passende Schulstufe(n) aus.
</p>""") }

# ----------------------------------------------------------------
help_form['lernrestyp'] = {
     'title'      : _(u'Art der Lernressource'),
     'help'       : _(u"""<p>
Hier legen Sie die Art der Lernressource fest.
</p>""") }

# ----------------------------------------------------------------
help_form['schlagwort'] = {
     'title'      : _(u'Schlagwort'),
     'auto_complete': True,
     'help'       : _(u"""<p>
Geben Sie in diesem Eingabefeld das gewünschte Schlagwort ein.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Volltextsuche'),
     'info'       : _(u"""<p>
Die hier eingegebenen Begriffe werden in (nahezu) allen
Feldern der Datenbank gesucht.
</p>""") }

help_form['tab_course'] = {
     'title'      : _(u'Fach/Sachgebiet'),
     'info'       : _(u"""<p>
Hier legen Sie fest, welchem Fach bzw. welchen Fächern Ihre
Lernressource zugeordnet sein soll.
</p>""") }

help_form['tab_description'] = {
     'title'      : _(u'Lernressource'),
     'info'       : _(u"""<p>
Hier können Sie die Lernressource genauer beschreiben.
</p>""") }

help_form['tab_details'] = {
     'title'      : _(u'Zuordnungen'),
     'info'       : _(u"""<p>
Hier ordnen Sie die Lernressource verschiedenen Dimensionen zu.
</p>""") }

help_form['tab_keyword'] = {
     'title'      : _(u'Schlagwort'),
     'info'       : _(u"""<p>
Geben Sie hier bitte eines der vordefinierten Schlagworte ein.
</p>""") }

help_form['tab_more'] = {
     'title'      : _(u'Sortierung'),
     'info'       : _(u"""<p>
Hier können Sie das Suchverhalten beeinflussen.
</p>""") }

