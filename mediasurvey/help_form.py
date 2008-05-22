# -*- coding: utf-8 -*-
"""
/dms/mediasurvey/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer den Medien-Fragebogen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.04.2007  Beginn der Arbeit
0.02  04.05.2007  Korrekturen
"""

from django.utils.translation import ugettext as _

help_form = {}

# ----------------------------------------------------------------

help_form['name'] = {
     'title'      : _(u'Kurzname/ID'),
     'help'       : _(u"""<p>
Tragen Sie hier den Kurznamen Ihrer Informationsseite ein. Dieser Kurzname wird beim Aufrufen
der Informationsseite in der Web-Adresse verwendet. Der Kurzname sollte den Inhalt
möglichst präzise beschreiben und gleichzeitig möglichst kurz
sein.
</p>

<p>
Beim Aufrufen der Seiten wird zwischen Groß- und Kleinschreibung unterschieden. Bitte
verwenden Sie beim Kurznamen ausschließlich Kleinbuchstaben. Leerzeichen werden durch
einen Unterstrich, Umlaute durch "ae", "oe" usw. ersetzt.
</p>""") }

# ----------------------------------------------------------------

help_form['title'] = {
     'title'      : _(u'Überschrift'), 
     'help'       : _(u"""<p>
Tragen Sie hier die Überschrift Ihrer Informationsseite ein. Unter dieser Überschrift wird 
Ihre Seite angezeigt. Dieser Titel erscheint ebenfalls in der Übersicht des Ordners, der
Ihre Seite enthält.
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
Dieser Text wird direkt unterhalb der Überschrift angezeigt.
</p>""") }

# ----------------------------------------------------------------
help_form['text'] = {
     'title'      : _(u'Intro'),
     'help'       : _(u"""<p>
Hier sollten Sie kurz den Sinn des Medienfragebogens erlätern.
</p>""") }

# ----------------------------------------------------------------
help_form['text_more'] = {
     'title'      : _(u'Erweiterungstext'),
     'help'       : _(u"""<p>
Verwenden Sie dieses Eingabefeld bitte nur bei Informationsseiten
in einem Materialpool.
</p>""") }

# ----------------------------------------------------------------
help_form['image_url'] = {
     'title'      : _(u'Schmuckbild'),
     'help'       : _(u"""<p>
Bei Bedarf können Sie rechts neben Ihrem Text ein Bild anzeigen lassen.
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

help_form['info_slot_right'] = {
     'title'      : _(u'Seiteninfo'),
     'help'       : _(u"""<p>
In der rechten Spalte können Sie zusätziche Informationen anzeigen.
Diese werden in Blöcken organisiert, wobei ein Block aus einer
Überschrift sowie dem eigentlichen Text besteht. Für Zwischenüberschriften 
verwenden Sie bitte das Format "Überschrift 4", da diese automatisch umgewandelt werden.
</p>

<ul>
<li>
Falls Sie Bilder einbinden wollen, sollten dies nicht breiter als
120 Pixel sein.
</li>
<li>
Wegen der geringen Spaltenbreite sollten Ihre Texte möglichst
knapp gehalten werden. Bei sehr langen Worten stößt das
System an technische Grenzen.
</li>
</ul>""") }

# ----------------------------------------------------------------

help_form['order_by'] = {
     'title'      : _(u'Ordnungszahl'),
     'help'       : _(u"""<p>
Mit dieser Zahl bestimmen Sie die Sortierreihenfolge. Kleine Zahlen erscheinen
weiter oben, größere Zahlen weiter unten. Haben zwei Objekte die
gleiche Ordnungszahl, so werden Sie alphabetisch nach der Überschrift sortiert.
</p>""") }

# ----------------------------------------------------------------

help_form['section'] = {
     'title'      : _(u'Zuordnung zu einem Zwischentitel'),
     'help'       : _(u"""<p>
Hier legen Sie fest, bei welchem Zwischentitel Ihre Informationsseite im
Ordner angezeigt wird.
</p>""") }

# ----------------------------------------------------------------

help_form['visible_end'] = {
     'title'      : _(u'Sichtbar bis'),
     'help':_(u"""<p>
Dieses Feld legt fest, bis zu welchem Zeitpunkt diese Seite sichtbar ist.
</p>""") }

# ----------------------------------------------------------------
help_form['visible_start'] = {
     'title'      : _(u'Sichtbar von'),
     'help'       : _(u"""<p>
Dieses Feld legt den Zeitpunkt fest, ab dem diese Seite sichtbar ist.
</p>""") }

# ----------------------------------------------------------------

help_form['is_browseable'] = {
     'title'      : _(u'Wird angezeigt'),
     'help'       : _(u"""<p>
Mit diesem Schalter legen Sie fest, ob <i>diese</i> Seite
automatisch in Ihrem Ordner angezeigt wird oder nicht.
</p>
<p>
<b>Wichtiger Hinweis:</b> Falls der Name bekannt ist, kann die Seite
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
help_form['rss_feeds'] = {
     'title'      : _(u'RSS-Feeds'),
     'help'       : _(u"""<p>
Tragen Sie hier bitte den bzw. die RSS-Feeds, in die Ihr Beitrag aufgenommen
werden soll.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _(u'Basisdaten'),
     'info'       : _(u"""<p>
Mit diesem Formular legen Sie die wichtigsten Eigenschaften dieser
Informationsseite fest.
</p>""") }

help_form['tab_image'] = {
     'title'      : _(u'Bild'),
     'info'       : _(u"""<p>
Sie können Ihre Informationsseite mit einem kleinen Bild schmücken.
</p>""") }

help_form['tab_frame'] = {
     'title'      : _(u'Seiteninfo'),
     'info'       : _(u"""<p>
Im rechten Seitenbereich können Sie auf aktuelle Ereignisse,
neue Angebote usw. hinweisen.
</p>""") }

help_form['tab_visibility'] = {
     'title'      : _(u'Zuordnung/Sichtbarkeit'),
     'info'       : _(u"""<p>
Sie können die Sichtbarkeit Ihrer Seite auf unterschiedliche Weisen steuern.
</p>""") }

help_form['tab_rss'] = {
     'title'      : _(u'RSS-Feeds'),
     'info'       : _(u"""<p>
Falls Sie möchten, können Sie hier die Aufnahme in einen oder
mehrere RSS-Feeds beantragen.
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_col_1'] = {
     'title'      : _(u'Gelegentlicher Einsatz'),
     'help'       : _(u"""<p>
Gelegentlicher Einsatz
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_col_2'] = {
     'title'      : _(u'Häufiger Einsatz'),
     'help'       : _(u"""<p>
Häfiger
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_0'] = {
     'title'      : _(u'Sachunterricht'),
     'help'       : _(u"""<p>
Sachunterricht
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_1'] = {
     'title'      : _(u'Naturwissenschaften'),
     'help'       : _(u"""<p>
Naturwissenschaften
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_2'] = {
     'title'      : _(u'Mathematik'),
     'help'       : _(u"""<p>
Mathematik
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_3'] = {
     'title'      : _(u'Informatik'),
     'help'       : _(u"""<p>
Informatik
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_4'] = {
     'title'      : _(u'Gesellschaftswissenschaften'),
     'help'       : _(u"""<p>
Gesellschaftswissenschaften
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_row_5'] = {
     'title'      : _(u'Deutsch'),
     'help'       : _(u"""<p>
Deutsch
</p>""") }

# ----------------------------------------------------------------
help_form['com_einsatz_0'] = {
     'title'      : _(u'Sachunterricht'),
     'help'       : _(u"""<p>
Sachunterricht
</p>""") }

# ----------------------------------------------------------------
help_form['tab_1'] = {
     'title'      : _(u'1'),
     'info'       : _(u"""<p><b>IT-Ausstattung für den Einsatz im Unterricht</b></p>
<p>
Verfügt Ihre Schule über Computer für den Unterrichtseinsatz?
</p>
<p>
Falls Sie diese Frage mit  <i>nein</i> beantworten, dann müssen Sie nur noch
1.1 beantworten und sind nach dem Speichern mit der Arbeit fertig.
</p>
""") }

help_form['tab_1_1'] = {
     'title'      : _(u'1.1'),
     'info'       : _(u"""<p><b>Unterrichtsräume</b></p>
""") }

help_form['tab_1_2'] = {
     'title'      : _(u'1.2'),
     'info'       : _(u"""<p><b>Hardware</b></p>
""") }

help_form['tab_1_3'] = {
     'title'      : _(u'1.3'),
     'info'       : _(u"""<p><b>Spezielle Peripheriegeräte</b></p>
""") }

help_form['tab_1_4'] = {
     'title'      : _(u'1.4'),
     'info'       : _(u"""<p><b>Software</b></p>
""") }

help_form['tab_1_5'] = {
     'title'      : _(u'1.5'),
     'info'       : _(u"""<p><b>Lernplattformen</b></p>
""") }

help_form['tab_2'] = {
     'title'      : _(u'2'),
     'info'       : _(u"""<p><b>Vernetzung</b></p>
""") }

help_form['tab_3'] = {
     'title'      : _(u'3'),
     'info'       : _(u"""<p><b>Internetzugang</b></p>
""") }

help_form['tab_4_1'] = {
     'title'      : _(u'4.1'),
     'info'       : _(u"""<p><b>Computereinsatz</b></p>
<p>
Bitte geben Sie an, in welchen Lernbereichen, Fächern, beruflichen Einsatzfeldern und
AGs <b>Computer</b> in Ihrer Schule eingesetzt werden.
</p>""") }

help_form['tab_4_2'] = {
     'title'      : _(u'4.2'),
     'info'       : _(u"""<p><b>Nutzung von Spezialsoftware</b></p>
<p>
Bitte geben Sie an, ob Sie in Ihrer Schule neben Standardsoftware zur
Textverarbeitung etc. Spezialsoftware einsetzten.
</p>""") }

help_form['tab_4_3'] = {
     'title'      : _(u'4.3'),
     'info'       : _(u"""<p><b>Interneteinsatz</b></p>
<p>
Bitte geben Sie an, in welchen Lernbereichen, Fächern, beruflichen Einsatzfeldern und
AGs das <b>Internet</b> in Ihrer Schule eingesetzt werden.
</p>""") }

help_form['tab_4_4'] = {
     'title'      : _(u'4.4'),
     'info'       : _(u"""<p><b>Weitere Informationen zum Interneteinsatz</b></p>
<p>
Die folgenden Fragen erschließen weitere Nutzungen des Internets durch
Ihre Schule.
</p>""") }

help_form['tab_4_5'] = {
     'title'      : _(u'4.5'),
     'info'       : _(u"""<p><b>Einsatzschwerpunkte</b></p>
<p>
Bitte geben Sie an, in welchen Lern- und Lehrzusammenhängen
Computer an Ihrer Schule im Fachunterricht bzw.
in zusätzlichen Lernangeboten oder zur Fortbildung hauptsächlich eingesetzt werden. 
(Mehrfachnennungen möglich)
</p>
<ul>
<li>
<b>Information</b>:
Informationsbeschaffung
</li>
<li>
<b>Arbeiten</b>:
Selbstständiges Arbeiten mit Medien; E-Learning
</li>
<li>
<li>
<b>Lernen</b>:
Einsatz fachbezogener Lernsoftware
</li>
<li>
<b>Erziehung</b>:
Medienkompetenz, Medienerziehung
</li>
</ul>
""") }

help_form['tab_4_6'] = {
     'title'      : _(u'4.6'),
     'info'       : _(u"""<p><b>Landeslizenzen</b></p>
<p>
Welche der durch Landeslizenzen erworbenen Programme werden an Ihrer Schule
in welcher Häufigkeit genutzt: (s.a. Bildungsserver "Landeslizenzen")
</p>""") }

help_form['tab_4_7'] = {
     'title'      : _(u'4.7'),
     'info'       : _(u"""<p><b>Unterstützungssysteme</b></p>
<p>
Welche Unterstützungssysteme werden für die medienpädagogische
Arbeit  in Anspruch genommen? ( Mehrfachnennungen möglich)
</p>""") }

help_form['tab_4_8'] = {
     'title'      : _(u'4.8'),
     'info'       : _(u"""<p><b>Fortbildung</b></p>
""") }

help_form['tab_4_9'] = {
     'title'      : _(u'4.9'),
     'info'       : _(u"""<p><b>Nutzung der Medien durch das Kollegium</b></p>
<p>
Alte und neue Medien fließen zusammen: Filme werden heute auch über
DVDs und Computer mit Beamer vorgeführt, "Dias" werden mit Hilfe von Computern
projiziert, Vorträge werden mit dynamischen Modellen angereichert, Musikstücke
können mittels Computer vorgeführt werden, etc. In allen Anwendungen der
neuen Medien kann gezielt und unmittelbar Einfluss auf die Präsentation
genommen werden.<br />
Bitte berücksichtigen Sie bei der Beantwortung der o.g. Fragen auch diese
Veränderungen im Unterricht, die erst durch den Einsatz der neuen Medien
möglich sind.
</p>
<p>
Wie groß ist der Anteil der Lehrerinnen und Lehrer die Computer/Neue Medien im Unterricht einsetzen?
</p>
""") }

# ----------------------------------------------------------------
# ----------------------------------------------------------------

help_form['eigene_com'] = {
     'title': _(u'Eigene Computer'),
     'help' :''
}

# ----------------------------------------------------------------
# 1.1
raeume_gesamt = {}
raeume_gesamt['title']     = '<h5>Wie viele Räume für Unterrichtszwecke ' + \
                             'hat Ihre Schule insgesamt?</h5>'
raeume_gesamt['cols']      = [ _(u'Räume') ]
raeume_gesamt['rows']      = [ _(u'Unterrichtsräume insgesamt') ]
raeume_gesamt['show_cols'] = False

raeume_com = {}
raeume_com['title']     = '<h5>In welchen <i>Unterrichtsräume</i> befinden sich in ' + \
                             'Ihrer Schule <i>stationäre Computer</i>?</h5>'
raeume_com['cols']      = [ _(u'Unterrichtsräume <i>mit stationären</i> Computern'),
                            _(u'Unterrichtsräume <i>ohne stationäre</i> Computer'),
                            _(u'Anzahl der <i>stationären</i> Computer'),
                          ]
raeume_com['rows']      = [ _(u'PC-Räume (Computerräme)'),
                            _(u'Klassen- und Fachräume')
                          ]
raeume_com['show_cols'] = True

nutzung_sch_com = {}
nutzung_sch_com['title']     = '<h5>Besteht für Schüler/innen außerhalb ' + \
      'des Unterrichts die Möglichkeitder Computernutzung in der Schule ?</h5>'
nutzung_sch_com['cols']      = [ _(u'Computernutzung') ]
nutzung_sch_com['rows']      = [ _(u'Computernutzung außerhalb des Unterrichts') ]
nutzung_sch_com['show_cols'] = False

nutzung_raum_com = {}
nutzung_raum_com['title']     = '<h5>Wenn ja, wo findet die Nutzung statt?</h5>'
nutzung_raum_com['cols']      = [ _(u'Art der Räume') ]
nutzung_raum_com['rows']      = [ _(u'Art der Räume') ]
nutzung_raum_com['show_cols'] = False
nutzung_raum_com['valign']    = True

# ----------------------------------------------------------------
# 1.2
typ_com = {}
typ_com['title']     = """
<p>
Die Computertypen 1 und 2 sind wie folgt zu klassifizieren:
</p>
<ul>
<li><b>Computertyp 1:</b> nicht multimediafähiger PC: Taktfrequenz &lt; 550 MHz
</li>
<li><b>Computertyp 2:</b> multimediafähiger PC: Taktfrequenz &gt;= 550 MHz, mit Soundkarte, CD-ROM/DVD-Laufwerk; oder gleichwertig (z.B. Macintosh G3/G4/G5/Intel-Prozessor; Thin Client)
</li>
</ul>
<p>
Ältere Computertypen werden nicht erfasst. - <i>Mobile Systeme</i> sind definiert als schuleigene Laptops, Notebooks oder fahrbare Medieninseln mit PC, die in die Unterrichtsräume transportiert werden können.
</p>
"""

typ_com['cols']      = [ _(u'Anzahl'),
                         _(u'davon mobil'),
                       ]
typ_com['rows']      = [ _(u'Computertyp 1'),
                         _(u'Computertyp 2')
                       ]
typ_com['show_cols'] = True

notebook = {}
notebook['title']     = '<h5>Wie viele Notebooks sind in wie vielen Notebook-Klassen ' + \
                        '(Notebooks in Klassenstärke) vorhanden?'
notebook['cols']      = [ _(u'Anzahl') ]
notebook['rows']      = [ _(u'Notebooks'), _(u'Notebook-<i>Klassen</i>') ]
notebook['show_cols'] = False

# ----------------------------------------------------------------
# 1.3
peripherie = {}
peripherie['title']     = '<h5>Welche der folgenden Peripheriegeräte stehen an der ' + \
                    'Schule zur Verfügung? (Mehrfachnennungen sind möglich)</h5>'
peripherie['cols']      = ['']
peripherie['rows']      = [ _(u'Art der Geräte') ]
peripherie['show_cols'] = False
peripherie['valign']    = True

# ----------------------------------------------------------------
# 1.4
software = {}
software['title']     = '<h5>Bitte geben Sie an, welche der folgenden speziellen Programmtypen ' + \
                        'im Unterricht oder auch in Arbeitsgruppen in Ihrer Schule eingesetzt werden? ' + \
                        '(Mehrfachnennungen sind möglich)</h5>'
software['cols']      = [ _(u'Art der Software') ]
software['rows']      = [ _(u'Art der Software') ]
software['show_cols'] = False
software['valign']    = True

# ----------------------------------------------------------------
# 1.5
lernplattform = {}
lernplattform['title']     = '<h5>Welche Lernplattform(en) werden in Ihrer Schule genutzt? ' + \
                        '(Mehrfachnennungen möglich)</h5>'
lernplattform['cols']      = [ _(u'Art der Lernplattform') ]
lernplattform['rows']      = [ _(u'Art der Lernplattform') ]
lernplattform['show_cols'] = False
lernplattform['valign']    = True

eigene_plattform = {}
eigene_plattform['title']     = '<h5>Wurde in Ihrer Schule eine eigene Lernplattform eingerichtet?</h5>'
eigene_plattform['cols']      = [ _(u'Plattform') ]
eigene_plattform['rows']      = [ _(u'Eigene Lernplattform an Ihrer Schule eingerichtet') ]
eigene_plattform['show_cols'] = False

# ----------------------------------------------------------------
# 2
netz = {}
netz['title']     = '<h5>Existiert in Ihrer Schule ein Netzwerk mit Server(n)?</h5>'
netz['cols']      = [ _(u'Anzahl') ]
netz['rows']      = [ _(u'Netzwerk') ]
netz['show_cols'] = False

netz_bs = {}
netz_bs['title']     = '<h5>Falls ja: Mit welchem Betriebssystem arbeitet der Server?' + \
                       ' (Mehrfachnennungen möglich)</h5>'
netz_bs['cols']      = [ _(u'Anzahl') ]
netz_bs['rows']      = [ _(u'Netzbetriebssystem') ]
netz_bs['show_cols'] = False
netz_bs['valign']    = True

netz_com = {}
netz_com['title']     = '<h5>Wie viele Computer sind schulintern vernetzt?</h5>'
netz_com['cols']      = [ _(u'Anzahl') ]
netz_com['rows']      = [ _(u'Vernetzte Computer') ]
netz_com['show_cols'] = False

netz_wlan = {}
netz_wlan['title']     = '<h5>Wie viele davon über WLAN?</h5>'
netz_wlan['cols']      = [ _(u'Anzahl') ]
netz_wlan['rows']      = [ _(u'Mit WLAN vernetzte Computer') ]
netz_wlan['show_cols'] = False

netz_raum = {}
netz_raum['title']     = '<h5>Wie viele Klassen- und Fachräume sind mit dem PC-Netzwerk ' + \
                         'der Schule verbunden?</h5>'
netz_raum['cols']      = [ _(u'Anzahl') ]
netz_raum['rows']      = [ _(u'Vernetzte Räume') ]
netz_raum['show_cols'] = False

# ----------------------------------------------------------------
# 2
internet = {}
internet['title']     = '<h5>Hat Ihre Schule für Unterrichtszwecke einen Internetzugang?</h5>'
internet['cols']      = [ _(u'Anzahl') ]
internet['rows']      = [ _(u'Internetzugang') ]
internet['show_cols'] = False

internet_art = {}
internet_art['title']     = '<h5>Falls ja: Wie viele Computer Ihrer Schule sind mit dem Internet verbunden?</h5>'
internet_art['cols']      = [ _(u'Anzahl') ]
internet_art['rows']      = [ _(u'Art des Internetzugangs') ]
internet_art['show_cols'] = False
internet_art['valign']    = True

internet_anz = {}
internet_anz['title']     = '<h5>Wie viele Ihrer Computer haben Zugang zum Internet?</h5>'
internet_anz['cols']      = [ _(u'Anzahl') ]
internet_anz['rows']      = [ _(u'Anzahl der Computer mit Internetzugang') ]
internet_anz['show_cols'] = False

# ----------------------------------------------------------------
# 4.1
com_einsatz = {}
com_einsatz['title']     = '<h5>Allgemeinbildende Fächer</h5>'
com_einsatz['cols']      = ['']
com_einsatz['rows']      = []
com_einsatz['show_cols'] = False

com_einsatz_bf = {}
com_einsatz_bf['title']     = '<h5>Berufliche Bildung/Berufsfelder</h5>'
com_einsatz_bf['cols']      = ['']
com_einsatz_bf['rows']      = []
com_einsatz_bf['show_cols'] = False

# 4.2
com_beruf = {}
com_beruf['title']     = '<h5>Setzen Sie in Ihrer Schule in nennenswertem Umfang ' +\
                         'berufs- und brachenspezifische Applikationen ein? ' +\
                         '(CAD, CNC, SPS, FiBu, Warenwirtschaft etc.) </h5>'
com_beruf['cols']      = [ _(u'Software') ]
com_beruf['rows']      = [ _(u'Branchensoftware') ]
com_beruf['show_cols'] = False

com_foerder = {}
com_foerder['title']     = '<h5>Setzen Sie in Ihrer Schule Spezialhard- und -software ' +\
                         'zur Förderung behinderter Schülerinnen und ' +\
                         'Schüler ein?</h5>'
com_foerder['cols']      = [ _(u'Software') ]
com_foerder['rows']      = [ _(u'Spezialhard- und -software') ]
com_foerder['show_cols'] = False

# 4.3
int_einsatz = {}
int_einsatz['title']     = '<h5>Allgemeinbildende Fächer</h5>'
int_einsatz['cols']      = ['']
int_einsatz['rows']      = []
int_einsatz['show_cols'] = False

int_einsatz_bf = {}
int_einsatz_bf['title']     = '<h5>Berufliche Bildung/Berufsfelder</h5>'
int_einsatz_bf['cols']      = ['']
int_einsatz_bf['rows']      = []
int_einsatz_bf['show_cols'] = False

# 4.4
int_website = {}
int_website['title']     = '<h5>Hat Ihre Schule eine eigene Website? Falls ja, geben Sie ' + \
                           'bitte die Web-Adresse an. Falls nein, lassen Sie das Feld' +\
                           'bitte leer.</h5>'
int_website['cols']      = [ _(u'Website') ]
int_website['rows']      = [ _(u'Adresse der Website') ]
int_website['show_cols'] = False

interaktion= {}
interaktion['title']     = '<h5>Nutzen Sie an Ihrer Schule eines oder mehrere der ' +\
                        'folgenden interaktiven Module?</h5>'
interaktion['cols']      = ['']
interaktion['rows']      = [ _(u'Module') ]
interaktion['show_cols'] = False
interaktion['valign']    = True

# 4.5
einsatz = {}
einsatz['title']     = '<h5>Allgemeinbildende Fächer</h5>'
einsatz['cols']      = ['']
einsatz['rows']      = []
einsatz['show_cols'] = False

einsatz_bf = {}
einsatz_bf['title']     = '<h5>Berufliche Bildung/Berufsfelder</h5>'
einsatz_bf['cols']      = ['']
einsatz_bf['rows']      = []
einsatz_bf['show_cols'] = False

# 4.6
landeslizenz = {}
landeslizenz['title']     = ''
landeslizenz['cols']      = ['']
landeslizenz['rows']      = []
landeslizenz['show_cols'] = False

# ----------------------------------------------------------------
# 4.7
unterstuetzung = {}
unterstuetzung['title']     = ''
unterstuetzung['cols']      = ['']
unterstuetzung['rows']      = [ _(u'Unterstützungssystem') ]
unterstuetzung['show_cols'] = False
unterstuetzung['valign']    = True

# ----------------------------------------------------------------
# 4.8
fortbildung = {}
fortbildung['title']     = '<h5>Welche IT-Fortbildungsangebote werden von Ihrer Schule genutzt?</h5>'
fortbildung['cols']      = ['']
fortbildung['rows']      = [ _(u'Unterstützungssystem') ]
fortbildung['show_cols'] = False
fortbildung['valign']    = True

fortbildung_k = {}
fortbildung_k['title']     = '<h5>Wie werden Kolleginnen und Kollegen in die Mediennutzung ' + \
                             'an Ihrer Schule eingeführt?</h5>'
fortbildung_k['cols']      = ['']
fortbildung_k['rows']      = [ _(u'Art der Einführung') ]
fortbildung_k['show_cols'] = False
fortbildung_k['valign']    = True

# ----------------------------------------------------------------
# 4.9
nutzung = {}
nutzung['title']     = ''
nutzung['cols']      = ['']
nutzung['rows']      = [ _(u'Geschätzte Lehrerzahl') ]
nutzung['show_cols'] = False
nutzung['valign']    = True

help_form['org_id'] = {
     'title'      : _(u'Schulnummer'),
     'help'       : '' }
