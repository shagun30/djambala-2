# -*- coding: utf-8 -*-
"""
pdf_confirm.py

Dieses Programm erzeugt aus den in der Datei .. uebergebenden Daten eine
PDF-Seite, die als Bescheinigung der dienstlichen Taetigkeit dient.

Hans Rauch
hans.rauch@gmx.net

0.05  17.02.2003
0.06  27.06.2007  Umsetzung fuer Djambala
0.07  07.12.2007  Unicode Gemurkse etwas geordnet
"""

from django.utils.encoding  import smart_unicode

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import *
from reportlab.platypus import Paragraph, Frame, XPreformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen.canvas import Canvas
import string
import time

from django.utils.translation import ugettext as _

from dms.settings import START_OF_LETTER
from dms.settings import ADDRESS
from dms.settings import TMP_PATH

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
class pdfConfirm:

  def __init__ ( self ) :
    """
    Konstruktor
    """
    self.cMyName    = ''
    self.cMyAddress = ''
    self.load_config ()

  def load_config ( self ) :
    """
    Die entsprechenden Items aus einer cfg-Datei gelesen.
    """
    self.cMyName    = smart_unicode(START_OF_LETTER)
    self.cMyAddress = ''
    items = string.splitfields(smart_unicode(ADDRESS), "|")
    for item in items :
      self.cMyAddress += item + '\n'

  def getPreformatted ( self, c, x, y, w, h, style, info, mm_mode = 1 ) :
    """ formatieren Bereich zurueckgeben """
    lInfo = []
    lInfo.append(XPreformatted( info, style))
    if mm_mode == 1 :
      f = Frame ( x, y, w, h, showBoundary=0 )
    else :
      f = Frame ( x*mm, y*mm, w*mm, h*mm, showBoundary=0 )
    f.addFromList ( lInfo, c )

  def getParagraph ( self, c, x, y, w, h, style, info, mm_mode = 1 ) :
    """ formatieren Bereich zurueckgeben """
    lInfo = []
    #lInfo.append(Paragraph( info.decode('utf-8').encode('iso-8859-1'), style ))
    lInfo.append(Paragraph( info, style, encoding="utf-8"))
    if mm_mode == 1 :
      f = Frame ( x, y, w, h, showBoundary=0 )
    else :
      f = Frame ( x*mm, y*mm, w*mm, h*mm, showBoundary=0 )
    f.addFromList ( lInfo, c )

  def getAbsender ( self, c, style, info ) :
    """ Absender mit duenner Linie anzeigen """
    # --- Absenderfeld im Briefkopf
    w = 85 * mm
    h = 15 * mm
    x = 20 * mm
    y = 245 * mm - h
    self.getPreformatted ( c, x, y, w, h, style, info )
    c.line ( x,y+5*mm,x+w,y+5*mm )

  def getAdresse ( self, c, style, info ) :
    """ Adresse fuer Fensterumschlag anzeigen """
    self.getPreformatted ( c, 20, 235-35, 85, 35, style, info, 0 )

  def getAbsenderBereich ( self, c, style, info ) :
    """ Adresse fuer Fensterumschlag anzeigen """
    self.getPreformatted ( c, 120, 245-50, 75, 50, style, info, 0 )
    c.setFillColorRGB ( 0.9, 0.9, 1.0 )
    c.rect ( (120-5)*mm, 205*mm, 2*mm, 40*mm, stroke=0, fill=1 )

  def getDatum ( self, c, style, info ) :
    """ Adresse fuer Fensterumschlag anzeigen """
    self.getPreformatted ( c, 120, 215-10, 75, 10, style, info, 0 )

  def getBetreff ( self, c, style, info ) :
    """ Betreffzeile """
    self.getParagraph ( c, 20, 190-10, 175, 10, style, info, 0 )

  def getSeitenAbschluss ( self, c, style, info ) :
    """ Seitenabschluss """
    w = 175 * mm
    h = 10 * mm
    x = 20 * mm
    y = 20 * mm - h
    style.alignment = TA_CENTER
    self.getParagraph ( c, x, y, w, h, style, info )
    style.alignment = TA_LEFT
    c.line ( x,y+h,x+w,y+h )

  def getAnrede ( self, c, style, info ) :
    """ Anrede des Briefes """
    self.getParagraph ( c, 20, 175-150, 175, 150, style, info, 0 )

  def getTextBaustein ( self, c, style, info ) :
    """ Anrede des Briefes """
    self.getParagraph ( c, 20, 165-150, 175, 150, style, info, 0 )

  def getUnterschrift ( self, c, style, info ) :
    """ Unterschrift """
    w = 80 * mm
    h = 10 * mm
    x = 20 * mm
    y = 90 * mm
    c.setFillColorRGB ( 0.97, 0.97, 1.0 )
    c.rect ( x, y, w, h, stroke=0, fill=1 )
    style.alignment = TA_CENTER
    self.getParagraph ( c, x, y, w, h, style, info )
    style.alignment = TA_LEFT
    c.line ( x,y+10*mm,x+w,y+10*mm )

  def getSchulstempel ( self, c, style, info ) :
    """ Unterschrift """
    w = 80 * mm
    h = 10 * mm
    x = ( 175 + 20 - 85 ) * mm
    y = 85 * mm
    c.setFillColorRGB ( 0.97, 0.97, 1.0 )
    c.setDash ( 3, 3 )
    c.setLineWidth ( 0.1 )
    c.circle ( x + w / 2, y + h + 20 * mm, 30 * mm, stroke=1, fill=1 )
    c.setLineWidth ( 1 )
    style.alignment = TA_CENTER
    self.getParagraph ( c, x, y, w, h, style, info )
    style.alignment = TA_LEFT

  def doIt(self, dPara):

    cDateiname = TMP_PATH + dPara['user'] + "-bestaetigung.pdf"

    PAGE_WIDTH, PAGE_HEIGHT = A4
    # --- Umrechnung in mm
    PAGE_WIDTH = PAGE_WIDTH/72*inch/mm
    PAGE_HEIGHT = PAGE_HEIGHT/72*inch/mm

    c = Canvas ( cDateiname, pagesize=A4 )

    styles = getSampleStyleSheet ()
    styleN = styles["Normal"]
    styleN.spaceBefore = 0
    styleN.spaceAfter = 0
    styleN.leftIndent = -2 * mm

    # --------------------------------------------
    myString = dPara['d_org'] + "\n" + \
               dPara['d_strasse'] + " / " + \
               smart_unicode(dPara['d_plz']) + " " + dPara['d_ort']
    styleN.fontName = "Helvetica"
    styleN.fontSize = 8
    styleN.leading = 8
    self.getAbsender(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    if dPara['org_id'] > 0:
      myString = dPara['d_org'] + "\n" + \
                 dPara['d_strasse'] + "\n\n" + \
                 smart_unicode(dPara['d_plz']) + " " + dPara['d_ort']
    else :
      myString = self.cMyAddress
    styleN.fontSize = 12
    styleN.leading = 12
    self.getAdresse(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    myString = dPara['d_org'] + "\n" + \
               dPara['d_strasse'] + "\n" + \
               smart_unicode(dPara['d_plz']) + " " + dPara['d_ort'] + "\n\n" + \
               "Fon " + dPara['d_telefon'] + "\n" + \
               "Fax " + dPara['d_fax']
    self.getAbsenderBereich(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    t = time.time()
    cHeute = time.strftime("%d.%m.%Y",time.localtime(t))
    myString = "Datum           " + cHeute
    self.getDatum(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    if dPara['org_id'] > 0:
      myString = u"<b>Bestätigung der Registrierung von %s %s</b>" %(dPara['vorname'], dPara['nachname'])
    else :
      myString = u"<b>Bescheinigung der Beschäftigung von %s %s</b>" %(dPara['vorname'], dPara['nachname'])
    self.getBetreff(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    myString = dPara['d_org'] + " / " + \
               dPara['d_strasse'] + " / " + \
               smart_unicode(dPara['d_plz']) + " " + dPara['d_ort']
    styleN.fontSize = 10
    styleN.leading = 10
    self.getSeitenAbschluss(c, styleN, smart_unicode(myString))
    styleN.fontSize = 12
    styleN.leading = 12

    # --------------------------------------------
    myString = self.cMyName # "Sehr geehrter Herr Budde,"
    self.getAnrede(c, styleN, smart_unicode(myString))

    # --------------------------------------------
    if dPara['org_id'] > 0:
      myString = u"hiermit bestätige ich, dass ich mich als " + \
                 ' Mitglied der Schulgemeinde online registriert habe.\n'
  
      self.getTextBaustein(c, styleN, smart_unicode(myString))
  
      # --------------------------------------------
      myString = u"Unterschrift"
      self.getUnterschrift(c, styleN, smart_unicode(myString))
    else :
      myString = u"hiermit bestätigen wir, dass "
      if dPara['geschlecht'] == "w" :
        myString += u"Frau "
      else :
        myString += u"Herr "
      myString = myString  + dPara['vorname'] + " " + \
                  dPara['nachname'] + u' in unserer Einrichtung tätig ist.\n'
  
      self.getTextBaustein(c, styleN, smart_unicode(myString))
  
      # --------------------------------------------
      myString = u"Unterschrift der Leitung"
      self.getUnterschrift(c, styleN, smart_unicode(myString))
  
      # --------------------------------------------
      myString = u"Stempel der Einrichtung"
      self.getSchulstempel(c, styleN, smart_unicode(myString))

    c.save ()
