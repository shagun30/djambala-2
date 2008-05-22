#-*-coding: utf-8 -*-
"""
pdf_saved_infos.py

Dieses Programm erzeugt aus den in der Datei .. uebergebenden Daten eine
PDF-Seite, auf der die ueber die betreffende Person
gesammelten Informationen aufgefuehrt werden.

Hans Rauch
hans.rauch@gmx.net

0.01  13.02.2003
0.02  27.06.2007  Umsetzung Djambala
"""

from django.utils.encoding  import smart_unicode

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import *
from reportlab.platypus import Paragraph, Spacer, Frame, XPreformatted, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,mm
from reportlab.pdfgen.canvas import Canvas
import string
import time

from django.utils.translation import ugettext as _

from dms.settings import BOTTOM_OF_LETTER
from dms.settings import ORGANISATION
from dms.settings import ADDRESS_OF_LETTER
from dms.settings import KONTACT_NAME
from dms.settings import KONTACT_PHONE
from dms.settings import KONTACT_FAX
from dms.settings import KONTACT_EMAIL
from dms.settings import GOOD_BYE
from dms.settings import INST_LOGO_PATH
from dms.settings import TMP_PATH

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
class pdfSavedInfos:

  def __init__ ( self ) :
    """ """
    self.second_page = 0

  def getPreformatted ( self, c, x, y, w, h, style, info, mm_mode = 1 ) :
    """ formatieren Bereich zurueckgeben """
    lInfo = []
    lInfo.append(XPreformatted( info, style ))
    if mm_mode == 1 :
      f = Frame ( x, y, w, h, showBoundary=0 )
    else :
      f = Frame ( x*mm, y*mm, w*mm, h*mm, showBoundary=0 )
    f.addFromList ( lInfo, c )
    return f

  def getParagraph ( self, c, x, y, w, h, style, info, mm_mode = 1 ) :
    """ formatieren Bereich zurueckgeben """
    lInfo = []
    lInfo.append(Paragraph(info, style, encoding="utf-8"))
    if mm_mode == 1 :
      f = Frame ( x, y, w, h, showBoundary=0 )
    else :
      f = Frame ( x*mm, y*mm, w*mm, h*mm, showBoundary=0 )
    f.addFromList ( lInfo, c )
    return f

  def getHelpLinks ( self, c, style ) :
    """ Trennungslinie links """
    w = 70 * mm
    h = 20 * mm
    x = 14 * mm
    y = 262 * mm
    c.setLineWidth ( 0.2 )
    c.line ( x,y+5*mm,x+w,y+5*mm )
    c.setLineWidth ( 1 )

  def getHelpRechts ( self, c, style, info ) :
    """ HeLP """
    w = 75 * mm
    h = 20 * mm
    x = 124 * mm
    y = 262 * mm
    style.fontSize = 12
    style.leading = 12
    self.getPreformatted ( c, x+9*mm, y, w, h, style, info )
    style.fontSize = 10
    style.leading = 10
    c.setLineWidth ( 0.2 )
    c.line ( x,y+5*mm,x+w,y+5*mm )
    c.setLineWidth ( 1 )

  def getHelpMitte ( self, c ) :
    """ Hessen-Loewe """
    w = 20 * mm
    h = 20 * mm
    x = 95 * mm
    y = 262 * mm
    c.drawImage(INST_LOGO_PATH,x,y,2*77/3,2*87/3)

  def getAbsender ( self, c, style, info ) :
    """ Absender mit duenner Linie anzeigen """
    w = 80 * mm
    h = 15 * mm
    x = 20 * mm
    y = 245 * mm
    self.getPreformatted ( c, x, y, w, h, style, info )
    c.setLineWidth ( 0.2 )
    c.line ( x,y+5*mm,x+w-15*mm,y+5*mm )
    c.setLineWidth ( 1 )

  def getAdresse ( self, c, style, info ) :
    """ Adresse fuer Fensterumschlag anzeigen """
    self.getPreformatted ( c, 20, 202, 85, 35, style, info, 0 )

  def getAbsenderBereich ( self, c, style, t ) :
    """ Adresse fuer Fensterumschlag anzeigen """
    f = Frame ( 135*mm, 195*mm, 65*mm, 60*mm, showBoundary=0 )
    f.addFromList ( [t], c )

  def getBetreff ( self, c, style, info ) :
    """ Betreffzeile """
    self.getParagraph ( c, 20, 190, 175, 10, style, info, 0 )

  def getSeitenAbschluss ( self, c, style, info ) :
    """ Seitenabschluss """
    w = 200 * mm
    h = 15 * mm
    x = 5 * mm
    y = 10 * mm
    self.getPreformatted ( c, x, y, w, h, style, info )
    c.setLineWidth ( 0.2 )
    c.line ( x,y+h,x+w,y+h )
    c.setLineWidth ( 1 )

  def getAnrede ( self, c, style, info ) :
    """ Anrede des Briefes """
    self.getParagraph ( c, 20, 30, 175, 150, style, info, 0 )

  def getTextBaustein ( self, c, style, info, zusatz ) :
    """ Anrede des Briefes """
    f = self.getParagraph ( c, 20, 20, 175, 150, style, info, 0 )
    f.addFromList ( zusatz, c )
  
  def getTextBaustein2 ( self, c, style, info, zusatz ) :
    """ Anrede des Briefes """
    f = self.getParagraph ( c, 20, 50, 175, 200, style, info, 0 )
    f.addFromList ( zusatz, c )
  
  def writeSeitenabschluss ( self, c, style ) :
    """Arbeitszeiten ...  """
    myString = BOTTOM_OF_LETTER.replace('\\n', '\n')
    style.alignment = TA_CENTER
    style.fontSize = 8
    style.leading = 10
    self.getSeitenAbschluss ( c, style, myString)
    style.alignment = TA_LEFT
    style.fontSize = 10
    style.leading = 12

  def writeKopf ( self, c, style) :
    """ """
    # --------------------------------------------
    self.getHelpLinks ( c, style )
    style.fontName = "Helvetica-Bold"
    myString = ORGANISATION
    self.getHelpRechts ( c, style, myString)
    style.fontName = "Helvetica"
    self.getHelpMitte ( c )

  # ------------------------------------------------------------------------  
  #
  # Hauptprogramm
  #
  # ------------------------------------------------------------------------

  def doIt(self, dPara):

    cDateiname = TMP_PATH + dPara['user'] + "-infos.pdf"

    PAGE_WIDTH, PAGE_HEIGHT = A4
    # --- Umrechnung in mm
    PAGE_WIDTH = PAGE_WIDTH/72*inch/mm
    PAGE_HEIGHT = PAGE_HEIGHT/72*inch/mm

    c = Canvas ( cDateiname, pagesize=A4 )

    styles = getSampleStyleSheet ()
    styleN = styles["Normal"]
    styleN.fontName = "Helvetica"
    #styleN.spaceBefore = 0
    #styleN.spaceAfter = 0
    #styleN.leftIndent = -2 * mm

    # --------------------------------------------
    self.writeKopf ( c, styleN )

    # --------------------------------------------
    # --- Absendeadresse
    myString = ''
    for s in string.splitfields(ADDRESS_OF_LETTER.replace('\\n','\n'), '|'):
      myString += s + '\n'
    styleN.fontSize = 8
    styleN.leading = 8
    self.getAbsender ( c, styleN, myString)
    styleN.fontSize = 10
    styleN.leading = 12

    # --------------------------------------------
    t = time.time()
    cHeute = time.strftime("%d.%m.%Y",time.localtime(t))
    data = [
            ['',''],
            ['',''],
            ['',''],
            ['',''],
            ['',''],
            ['Bearbeiter',KONTACT_NAME],
            ['Durchwahl',KONTACT_PHONE],
            ['Telefax',KONTACT_FAX],
            ['',''],
            ['E-Mail',KONTACT_EMAIL],
            ['',''],
            ['Datum',cHeute],
           ]
    tStyle = [
              ('FONT', (0,0), (-1,-1), "Helvetica" ),
              ('FONTSIZE', (0,0), (-1,-1), 8 ),
              ('LEADING', (0,0), (-1,-1), 10 ),
              ('LEFTPADDING', (0,0), (-1,-1), 0 ),
              ('RIGHTPADDING', (0,0), (-1,-1), 0 ),
              ('TOPPADDING', (0,0), (-1,-1), 0 ),
              ('BOTTOMPADDING', (0,0), (-1,-1), 0 ),
             ]
    t = Table ( data, colWidths=(24*mm,40*mm), style=tStyle )
    self.getAbsenderBereich ( c, styleN, t )

    # --------------------------------------------
    self.writeSeitenabschluss ( c, styleN )
    
    #styleN.fontName = "Times-Roman"

    # --------------------------------------------
    myString = dPara['d_org'] + "\n" + \
               dPara['vorname'] + " " + dPara['nachname'] + "\n" + \
               dPara['d_strasse'] + "\n" + \
               "<b>" + smart_unicode(dPara['d_plz']) + " " + dPara['d_ort'] + "</b>"
    self.getAdresse ( c, styleN, myString)

    # --------------------------------------------
    myString = "<b>Ihre bei der Community gespeicherten Informationen</b>"
    styleN.fontName = "Helvetica-Bold"
    self.getBetreff ( c, styleN, myString)
    styleN.fontName = "Helvetica"

    # --------------------------------------------
    myString = "Sehr geehrte"
    if dPara['geschlecht'] == "w" :
      myString = myString + " Frau "
    else :
      myString = myString + "r Herr "
    myString = myString  + dPara['nachname'] + ","
    self.getAnrede ( c, styleN, myString)

    # --------------------------------------------
    myString = """folgende Informationen sind zu Ihrer
    Person bei unserer Community gespeichert:"""
    lInfo = []
    lInfo.append ( Spacer(0,3*mm) )
    lInfo.append ( Paragraph("<b>Angaben zur Person</b>", styleN, encoding="utf-8") )
    lInfo.append ( Spacer(0,2*mm) )
    data = [
              ['Vorname',dPara['vorname']],
              ['Nachname',dPara['nachname']],
              ]
    if dPara['titel'] != '':
      data.append ( ['Titel',dPara['titel']] )
    data.append ( ['E-Email',dPara['email']] )
    data.append ( ['Zugangsname (User-ID)',dPara['user']] )
    data.append ( ['Kennwort',dPara['kennwort']] )
    tStyle = [
                 ('GRID', (0,0), (-1,-1), 0.5, colors.grey ),
                 ('BACKGROUND', (0,0), (0,-1), colors.lightgrey )
                 ]
    t = Table ( data, colWidths=(50*mm,100*mm), style=tStyle )
    lInfo.append ( t )
    lInfo.append ( Spacer(0,3*mm) )
    lInfo.append ( Paragraph("<b>Angaben zu Ihrer Dienststelle (Schule, Einrichtung)</b>", styleN, encoding="utf-8") )
    lInfo.append ( Spacer(0,2*mm) )
    data2 = []
    data2.append ( ['Dienststelle',dPara['d_org']] )
    data2.append ( ['Adresse',dPara['d_strasse'] + ", " + \
                    smart_unicode(dPara['d_plz']) + " " + dPara['d_ort']
                   ] )
    data2.append ( ['Telefon, Fax',dPara['d_telefon'] + ", " + \
                    dPara['d_fax']
                   ] )

    tStyle2 = [
                 ('GRID', (0,0), (-1,-1), 0.5, colors.grey ),
                 ('BACKGROUND', (0,0), (0,-1), colors.lightgrey )
                 ]
    t2 = Table ( data2, colWidths=(50*mm,100*mm), style=tStyle2 )
    lInfo.append ( t2 )

    lInfo.append ( Spacer(0,5*mm) )
    
    myString3 = GOOD_BYE.replace('\\n', '\n')
    lInfo.append ( XPreformatted(myString3, styleN) )

    if self.second_page == 1 :
      self.getTextBaustein2 ( c, styleN, myString, lInfo )
    else :
      self.getTextBaustein ( c, styleN, myString, lInfo )
    c.save ()
