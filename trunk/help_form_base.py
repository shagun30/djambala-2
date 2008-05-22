# -*- coding: utf-8 -*-
"""
/dms/base_help_form.py

.. enthaelt einige der wichtigsten Kontext-Hilfetexte fuer
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.05.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

def get_help_form():
  help_form = {}
  
  # ----------------------------------------------------------------
  help_form['visible_end'] = {
      'title'      : _(u'Sichtbar bis'),
      'help':_(u"""<p>
  Dieses Feld legt fest, bis zu welchem Zeitpunkt dieser Beitrag/dieses Objekt sichtbar ist.
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['visible_start'] = {
      'title'      : _(u'Sichtbar von'),
      'help'       : _(u"""<p>
  Dieses Feld legt fest, ab welchem Zeitpunkt dieser Beitrag/dieses Objekt sichtbar ist.
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['is_browseable'] = {
      'title'      : _(u'Wird angezeigt'),
      'help'       : _(u"""<p>
  Mit diesem Schalter legen Sie fest, ob dieser Beitrag/ dieses Objekt
  angezeigt wird oder nicht.
  </p>
  <p>
  <b>Wichtiger Hinweis:</b> Falls der Name des Beitrags/ des Objektes bekannt ist, kann die Seite
  durch die direkte Angabe der Web-Adresse trotzdem angezeigt werden!
  </p>""") }

  # ----------------------------------------------------------------
  help_form['has_comments'] = {
      'title'      : _(u'Kann kommentiert werden'),
      'help'       : _(u"""<p>
  Dieser Schalter legt fest, ob diese Seite kommentiert werden kann
  bzw. darf. In der Regel wird diese Option ausgeschaltet.
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['license'] = {
      'title'      : _(u'Lizenz'),
      'help'       : _(u"""<p>
  Hier legen Sie fest, welche Lizenz Sie für Ihren Beitrag verwenden
  möchten. <b>Bitte beachten Sie, dass Sie nur dann eine Lizenz angeben
  dürfen, wenn Sie das entsprechende Recht besitzen
  bzw. die entsprechende Ressource explizit unter die betreffende Lizenz
  gestellt wurde!</b>
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['anti_spam_question'] = {
      'title'      : _(u'Anti-Spam-Frage'),
      'help'       : _(u"""<p>
  Mit dieser Frage wird verhindert, dass so genannte Spam-Roboter hier Ihre
  "Botschaften" hinterlassen können.
  </p>""") }
  
  help_form['anti_spam_answer'] = {
      'title'      : _(u'Antwort zur Anti-Spam-Frage'),
      'help'       : _(u"""<p>
  Geben Sie bitte hier die korrekte Antwort ein. Es wird nicht zwischen Groß- und
  Kleinschreibung unterschieden.
  </p>""") }

  # ----------------------------------------------------------------
  help_form['copyright'] = {
      'title'      : _(u'Copyright'),
      'help'       : _(u"""<p>
  <b>Sie dürfen hier nur dann Dateien/Texte/Bilder/Grafiken etc. auf den Server hochladen,
  wenn Sie die Inhalte dieser Datei entweder selbst erzeugt haben oder Ihnen der Verfasserin
  bzw. der Verfasser der Information (schriftlich) versichert hat, dass Sie diese
  Inhalte veröffentlichen dürfen.</b>
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['tab_intro'] = {
      'title'      : _(u'Intro'),
      'info'       : _(u"""<p>
  Die Intro-Information wird unterhalb der Überschrift angezeigt.
  Falls Sie bei "Intro - Mehr" Informationen eingeben, wird die Anzeige
  automatisch über einen entsprechenden Verweis zugänglich.
  </p>""") }

  help_form['tab_visibility'] = {
      'title'      : _(u'Sichtbarkeit'),
      'info'       : _(u"""<p>
  Sie können die Sichtbarkeit dieses Beitrags auf unterschiedliche Weisen steuern.
  </p>""") }

  help_form['tab_license'] = {
      'title'      : _(u'Lizenz'),
      'info'       : _(u"""<p>
  Hier legen Sie entsprechende Lizenzangaben fest.
  </p>""") }

  return help_form
