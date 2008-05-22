# -*- coding: utf-8 -*-
"""
/dms/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Kommentare
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.03.2007  Beginn der Arbeit
0.02  16.07.2007  Anti-Spam-Elemente
"""


from django.utils.translation import ugettext as _

def get_help_form():
  help_form = {}
  # ----------------------------------------------------------------
  help_form['username'] = {
      'title'      : _(u'Mein Name'), 
      'help'       : _(u"""<p>
  Tragen Sie hier bitte Ihren Vor- und Nachnamen ein. Anonyme Beiträge sind nicht erwünscht.
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['email'] = {
      'title'      : _(u'Meine E-Mail-Adresse'), 
      'help'       : _(u"""<p>
  Geben Sie bitte für Rückfragen oder direkte Reaktionen Ihre E-Mail-Adresse an.
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['title'] = {
      'title'      : _(u'Betreff'), 
      'help'       : _(u"""<p>
  Tragen Sie hier den Betreff Ihres Beitrages ein.
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
  
  # ----------------------------------------------------------------
  help_form['is_browseable'] = {
      'title'      : _(u'Wird angezeigt ...'),
      'help'       : _(u"""<p>
  Mit diesem Schalter legen Sie fest, ob dieser Beitrag
  angezeigt wird oder nicht.
  </p>
  <p>
  <b>Wichtiger Hinweis:</b> Falls der Name bekannt ist, kann die Seite
  durch die direkte Angabe der Web-Adresse trotzdem angezeigt werden!
  </p>""") }
  
  # ----------------------------------------------------------------
  help_form['rss_feeds'] = {
      'title'      : _(u'RSS-Feeds'),
      'help'       : _(u"""<p>
  Wählen Sie bitte den oder die RSS-Feeds aus, bei denen Ihr
  Beitrag erscheinen soll.</p>""") }
  
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
  help_form['tab_base'] = {
      'title'      : _(u'Kommentar'),
      'info'       : _(u"""<p>
  Mit diesem Formular legen Sie Ihren Beitrag fest.
  </p>""") }
  
  help_form['tab_base_moderated'] = {
        'title': _(u'Moderierter Kommentar'),
        'info' : _(u"""<p>
  <b>Ihr neuer Beitrag wird daher erst
  angezeigt, nachdem ihn die zuständige Person freigegeben hat.</b>
  </p>""") }
  
  help_form['tab_rss'] = {
      'title'      : _(u'RSS-Feed'),
      'info'       : _(u"""<p>
  Hier können Sie einen oder mehrere RSS-Feeds auswählen, bei denen
  Ihr Beitrag aufgenommen werden soll.
  </p>""") }

  return help_form

help_form = get_help_form()
