#-*-coding: utf-8 -*-
"""
/dms/mail.py

.. enthaelt Hilfefunktionen fuer E-Mails
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.05.2007  Beginn der Arbeit
"""
import smtplib
import StringIO

from django.core.mail       import send_mail
from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

from dms.models             import DmsItemContainer
from dms.settings           import CONTROL_EMAIL
from dms.utils_base         import html2txt

# -----------------------------------------------------
def createhtmlmail(html, text, subject):
  """Create a mime-message that will render HTML in popular MUAs, text in better ones"""
  import MimeWriter
  import mimetools
  import cStringIO

  out = StringIO.StringIO() # output buffer for our message 
  htmlin = StringIO.StringIO(html.encode('utf8'))
  txtin = StringIO.StringIO(text.encode('utf8'))
  
  writer = MimeWriter.MimeWriter(out)
  #
  # set up some basic headers... we put subject here
  # because smtplib.sendmail expects it to be in the
  # message body
  #
  writer.addheader("Subject", subject)
  writer.addheader("MIME-Version", "1.0")
  #
  # start the multipart section of the message
  # multipart/alternative seems to work better
  # on some MUAs than multipart/mixed
  #
  writer.startmultipartbody("alternative")
  writer.flushheaders()
  #
  # the plain text section
  #
  subpart = writer.nextpart()
  subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
  pout = subpart.startbody("text/plain", [("charset", 'utf-8')])
  mimetools.encode(txtin, pout, 'quoted-printable')
  txtin.close()
  #
  # start the html subpart of the message
  #
  subpart = writer.nextpart()
  subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
  #
  # returns us a file-ish object we can write to
  #
  pout = subpart.startbody("text/html", [("charset", 'utf-8')])
  mimetools.encode(htmlin, pout, 'quoted-printable')
  htmlin.close()
  #
  # Now that we're done, close our writer and
  # return the message body
  #
  writer.lastpart()
  msg = out.getvalue()
  out.close()
  #print msg
  return msg

# -----------------------------------------------------
def send_control_email(item_container, feed=None):
  """ """
  if feed == None:
    subject = _(u'Kontrolle eines Beitrags: ')
    text = item_container.item.title + '\n\n' + item_container.item.text + '\n\n' + item_container.get_absolute_url()
  else:
    subject = _(u'Kontrolle eines RSS-Feed-Beitrags: ')
    text = feed.title + '\n\n' + item_container.item.text + '\n\n' + item_container.get_absolute_url()
  subject += item_container.item.title.replace('\n', ' ').replace('\r', '')
  from_addr = CONTROL_EMAIL
  # --- Problem eines Zirkel-Imports!!!
  parent = item_container.get_parent()
  email = parent.item.owner.email
  to_addr = [email]
  send_mail(subject, html2txt(text), from_addr, to_addr, fail_silently=False)

# -----------------------------------------------------
def send_control_member_active(user):
  """ """
  subject = _(u'Mitgliedschaft in der Community freigeschaltet')
  text = _(u'Ihre Community-Zugang ist jetzt freigeschaltet.')
  from_addr = CONTROL_EMAIL
  to_addr = [user.email]
  send_mail(subject, html2txt(text), from_addr, to_addr, fail_silently=False)

# -----------------------------------------------------
def send_control_new_membership(item_container, user, role):
  """ sendet E-Mail ueber neue Mitgliedschaft """
  # --- Schueler/innen haben keine E-Mail-Adresse
  if user.email.strip() == '':
    return
  t = get_template('mail/new_membership.html')
  c = Context({'url': item_container.get_absolute_url(), 
               'username': user.username, 
               'role': role.description})
  text_html = t.render(c)
  text = html2txt(text_html)
  msg = createhtmlmail(text_html, text, _(u'Mitarbeit in einem geschlossenen Bereich'))
  s = smtplib.SMTP()
  s.connect()
  s.sendmail(CONTROL_EMAIL, [user.email], msg)
  s.close()

# -----------------------------------------------------
def send_password(email, username, password):
  """ sendet E-Mail Zugangsdaten """
  t = get_template('mail/community.html')
  c = Context({'username': username, 
               'password': password})
  text_html = t.render(c)
  text = html2txt(text_html)
  msg = createhtmlmail(text_html, text, _(u'Zugangsdaten zur Community des Bildungsservers Hessen'))
  s = smtplib.SMTP()
  s.connect()
  s.sendmail(CONTROL_EMAIL, [email], msg)
  s.close()
