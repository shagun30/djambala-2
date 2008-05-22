# -*- coding: utf-8 -*-
"""
zecomPdfSend.py

Dieses Programm erzeugt aus den in der Datei .. uebergebenden Daten eine
PDF-Seite, auf der die ueber die betreffende Person
gesammelten Informationen aufgefuehrt werden.

Hans Rauch
hans.rauch@gmx.net

0.03  13.02.2003
0.04  28.06.2007  Umsetzung Djambala
"""

from django.utils.encoding  import smart_unicode

import smtplib
import email
import mimetypes
import string

from email import Encoders
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart

from django.utils.translation import ugettext as _

from dms.settings       import SENDER_EMAIL
from dms.settings       import BACKUP_EMAIL
from dms.settings       import COMMUNITY_URL
from dms.settings       import GOOD_BYE
from dms.settings       import TMP_PATH

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
class pdfSend:

  def getAttachment ( self, path ) :
    ctype, encoding = mimetypes.guess_type ( path )
    if ctype is None or encoding is not None :
      ctype = "application/octet-stream"
    maintype, subtype = ctype.split ( "/", 1 )

    f = open ( path, "r" )
    if maintype == "text" :
      msg = MIMEText ( f.read(), _subtype=subtype )
    elif maintype == "image" :
      msg = MIMEImage ( f.read(), _subtype=subtype )
    elif maintype == "audio" :
      msg = MIMEAudio ( f.read(), _subtype=subtype )
    else :
      msg = MIMEBase ( maintype, subtype )
      msg.set_payload ( f.read() )
      Encoders.encode_base64 ( msg )
    f.close ()
    msg.add_header ( 'Content-Disposition', 'attachment', filename=path[string.rfind(path,"/")+1:] )
    return msg

  # ------------------------------------------------------------------------
  #
  # Hauptprogramm
  #
  # ------------------------------------------------------------------------

  def doIt(self, dPara, send_all=True):

    # --- Kontrollmeldung
    myAddress    = SENDER_EMAIL
    toAddress    = BACKUP_EMAIL

    outer = MIMEMultipart ()
    outer['Subject'] = "[Bildungsserver-Community] " + dPara['user']
    outer['From'] = myAddress
    outer['To'] = toAddress
    outer.epilogue = ""

    cText = ""
    cText += u'Vorname: ' + dPara['vorname'] + '\n'
    cText += u'Nachname: ' + dPara['nachname'] + ' ' + dPara['titel'] + '\n'
    cText += u'Zugangsname: ' + dPara['user'] + '\n'
    cText += u'E-Mail: ' + dPara['email'] + '\n'
    cText += u'Geschlecht: ' + dPara['geschlecht'] + '\n'
    cText += u'Kennwort: ' + dPara['kennwort'] + '\n'
    cText += u'Organisation: ' + dPara['d_org'] + '\n'
    cText += u'Straße: ' + dPara['d_strasse'] + '\n'
    cText += u'Ort: ' + smart_unicode(dPara['d_plz']) + ' ' + dPara['d_ort'] + '\n'
    cText += u'Telefon: ' + dPara['d_telefon'] + '\n'
    cText += u'Fax: ' + dPara['d_fax'] + '\n'

    outer.attach ( MIMEText(cText.encode('iso-8859-1')) )

    s = smtplib.SMTP ()
    s.connect ()
    s.sendmail ( myAddress, toAddress, outer.as_string() )
    s.close ()

    # --- E-Mail an Community-Mitglied

    cBescheinigungPdf = TMP_PATH + dPara['user'] + "-bestaetigung.pdf"
    cInfoPdf = TMP_PATH + dPara['user'] +"-infos.pdf"

    #myAddress = "h.rauch@help.hessen.de"
    toAddress = dPara['email']
    # !!!!!!!!!!!!!!!!!!!
    #toAddress = "hrauch@localhost"

    outer = MIMEMultipart ()
    outer['Subject'] = "Mitgliedschaft in der Community"
    outer['From'] = myAddress
    outer['To'] = toAddress
    #outer.preamble = "Was ist eine Praeambel?"
    outer.epilogue = ""

    cText = "Sehr geehrte"
    if dPara['geschlecht'] == "w" :
      cText = cText + " Frau "
    else :
      cText = cText + "r Herr "
    cText = cText + dPara['vorname'] + " " + dPara['nachname'] + ",\n"

    if send_all:
      cText += u"""

anbei senden wir Ihnen zwei PDF-Dateien, die Sie bitte auf Ihrer Festplatte
abspeichern und anschließend ausdrucken.

Die erste Datei liefert den Vordruck einer Bescheinigung, die Sie von
der Leitung Ihrer Dienststelle bestätigen lassen und an uns per normaler
Post zurücksenden. Innerhalb von maximal einer Woche schalten wir Ihren
Zugang frei. Erst dann können Sie auf geschützte Bereiche zugreifen. 
Mit unserer Freigabe erhalten Sie gleichzeitig eine entsprechende E-Mail.

Die zweite Datei enthält die Informationen, die gegenwärtig in diesem
Zusammenhang über Sie auf unserem Server gespeichert sind. Diese Datei
enthält Ihr Kennwort; verwahren Sie den Ausdruck (und die Datei) daher
sorgfältig auf.

Ihr Kennwort sowie Ihre E-Mail können Sie auf foldender Seite ändern:

    """
    else :
      cText += u"""

anbei senden wir Ihnen eine PDF-Datei, die Sie bitte auf Ihrer Festplatte
abspeichern und anschließend ausdrucken.

Diese PDF-Datei enthält die Informationen, die gegenwärtig für Ihren
Zugang zum Bildungsserver Hessen über Sie gespeichert sind. Diese Datei
enthält Ihr Kennwort; verwahren Sie den Ausdruck (und die Datei) daher
sorgfältig auf.

Ihr Kennwort oder Ihre E-Mail können Sie auf foldender Seite ändern:

    """
    cText += COMMUNITY_URL + u'\n\n'
    cText += smart_unicode(GOOD_BYE)
    outer.attach ( MIMEText(cText.encode('iso-8859-1')) )

    if send_all == 1 :
      outer.attach ( self.getAttachment ( cBescheinigungPdf ) )
    outer.attach ( self.getAttachment ( cInfoPdf ) )

    s = smtplib.SMTP ()
    s.connect ()
    s.sendmail ( myAddress, toAddress, outer.as_string() )
    s.close ()

