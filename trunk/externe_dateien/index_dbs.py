#!/usr/bin/python
#-*-coding: utf-8 -*-
#
# Vgl. http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.05.2007  vorlaeufiger Abschluss der Arbeit
0.02  20.10.2007  Optimierung des Speicherverbrauchs
0.03  30.12.2007  Integratin von pdftotext und wvText
"""

import xapian
import string
import re
import MySQLdb
import time
import os
import mimetypes
import codecs

from dms.models   import DmsItemContainer
from dms.utils    import get_breadcrumb
from dms.queries  import get_eduitem
from dms.queries  import get_item_container_by_id
from dms.queries  import get_site_url
from dms.queries  import is_file_by_item_container

from dms.file.utils     import get_file_name

from dms.settings import *
from dms.encode_decode import decode_html

MAX_PROB_TERM_LENGTH = 64

def p_alnum(c):
    return (c in string.ascii_letters + u'äöüßÄÖÜ' or c in string.digits)
    return (c in string.ascii_letters or c in string.digits)

def p_notalnum(c):
    return not p_alnum(c)

def p_notplusminus(c):
    return c != '+' and c != '-'

def find_p(string, start, predicate):
    while start<len(string) and not predicate(string[start]):
        start += 1
    return start

def get_eduitem_field(field):
  #temp = remove_html(field).strip()
  temp = field.strip()
  if temp != '':
    temp += '\n'
  return temp

def get_item_list(query_set):
  ret = ''
  for q in query_set.all():
    if ret != '':
      ret += '\n'
    ret += str(q.id)
  return ret

def do_add(doc, name, line):
  items = string.splitfields(line, '\n')
  for item in items:
    item = item.lower().strip()
    doc.add_term(name + item)

URL   = 0
TITLE = 1
DATE  = 2

def remove_html(s):
  s = s.replace(u'&#228;', u'ä')
  s = s.replace(u'&#246;', u'ö')
  s = s.replace(u'&#252;', u'ü')
  s = s.replace(u'&#223;', u'ß')
  s = s.replace(u'&#196;', u'Ä')
  s = s.replace(u'&#214;', u'Ö')
  s = s.replace(u'&#220;', u'Ü')
  l1 = re.sub(u'<.?>', '', s.strip())
  l2 = re.sub(u'</.?>', '', l1)
  l3 = re.sub(u'<a ', '', l2)
  return l3

db = xapian.WritableDatabase(DB_SEARCHENGINE, xapian.DB_CREATE_OR_OVERWRITE)
#db = xapian.WritableDatabase(DB_SEARCHENGINE, xapian.DB_CREATE_OR_OPEN)
stem = xapian.Stem("german2")

item_container_count = DmsItemContainer.objects.count()
ic_start = 0
ic_diff = 5000
while ic_start < item_container_count:
  ic_end = ic_start + 5000
  if ic_end > item_container_count:
    ic_end = item_container_count
  print ic_start, ic_end
  item_containers = DmsItemContainer.objects.all().select_related()[ic_start:ic_end]
  error_count = 0
  for item_container in item_containers:
    if item_container.is_browseable and not item_container.is_deleted:
      para = ''
      folders = string.splitfields(item_container.container.path, '/')
      for folder in folders:
        para += folder + ' '
      para += item_container.item.name + '\n'
      para += item_container.item.title + '\n'
      para += item_container.item.sub_title + '\n'
      para += item_container.item.text + '\n'
      para += item_container.item.text_more + '\n'
      para += item_container.item.owner.last_name + ' ' + item_container.item.owner.first_name + '\n'
      if is_file_by_item_container(item_container):
        p = item_container.container.is_protected()
        filepath = get_file_name(item_container, p)
        #print filepath
        filename = filepath[filepath.rfind('/')+1:]
        mimetype, encoding = mimetypes.guess_type(filepath)
        if mimetype in ['application/pdf', 'application/msword']:
          temp_file = TMP_PATH + filename[:filename.rfind('.')] + '.txt'
          if mimetype == 'application/pdf':
            command_str = '%s %s %s' % (PDF_TO_TEXT, filepath, temp_file)
          elif mimetype == 'application/word':
            command_str = '%s %s %s' % (WORD_TO_TEXT, filepath, temp_file)
          try:
            f = open(filepath, 'r')
            f.close()
            ok = True
          except:
            ok = False
          if ok:
            print command_str
            os.system(command_str)
            # nicht alle PDF-Dateien geben den Text frei
            try:
              f = codecs.open(temp_file, 'r', 'utf-8')
              text = f.read()
              f.close()
              para += text
              os.unlink(tempfile)
            except:
              pass
      it_app_name = item_container.item.app.name
      if it_app_name.find('Edu') > 0 and it_app_name != 'dmsEduFolder':
        edu_item = get_eduitem(item_container.item)
        if edu_item == None:
          error_count += 1
          x3 = x4 = x5 = x6 = x7 = x8 = x9 = ''
        else:
          para += get_eduitem_field(edu_item.autor)
          para += get_eduitem_field(edu_item.herausgeber)
          para += get_eduitem_field(edu_item.anbieter_herkunft)
          para += get_eduitem_field(edu_item.isbn)
          para += get_eduitem_field(edu_item.titel_lang)
          para += get_eduitem_field(edu_item.beschreibung_lang)+ '\n'
          para += get_eduitem_field(edu_item.standards_kmk)
          para += get_eduitem_field(edu_item.standards_weitere)
          para += get_eduitem_field(edu_item.techn_voraus)
          para += get_eduitem_field(edu_item.lernziel)
          para += get_eduitem_field(edu_item.lernzeit)
          para += get_eduitem_field(edu_item.methodik)
          para += get_eduitem_field(edu_item.lehrplan)
          para += get_eduitem_field(edu_item.rechte)
          # --- Mehrfachbelegung
          x3 = get_item_list(edu_item.fach_sachgebiet)
          x4 = get_item_list(edu_item.zielgruppe)
          x5 = get_item_list(edu_item.schulstufe)
          x6 = get_item_list(edu_item.schulart)
          x7 = get_item_list(edu_item.sprache)
          x8 = get_item_list(edu_item.schlagwort)
          x9 = str(item_container.item.integer_3) # lernrestyp
      else:
        x3 = x4 = x5 = x6 = x7 = x8 = x9 = ''
      #try:
      text = decode_html(para)
      #except:
      #  text = para
      doc = xapian.Document()
      doc.set_data(text)
      i = 0
      pos = 0
      while i < len(para):
        i = find_p(para, i, p_alnum)
        j = find_p(para, i, p_notalnum)
        k = find_p(para, j, p_notplusminus)
        if k == len(para) or not p_alnum(para[k]):
          j = k
        if (j - i) <= MAX_PROB_TERM_LENGTH and j > i:
          term = string.lower(para[i:j])
          doc.add_posting(stem(term), pos)
          pos += 1
        i = j
        if item_container.item.app.is_folderish:
          path = get_site_url(item_container, 'index.html')
        else:
          path = get_site_url(item_container, item_container.item.name)
      doc.add_value(URL, path.lower())
      doc.add_value(TITLE, item_container.item.title)
      doc.add_value(DATE, str(item_container.last_modified))
      doc.add_term('X1' + item_container.item.owner.username)
      site = path[7:].lower()
      doc.add_term('X2' + site[:site.find('/')])
      if x3 != '': do_add(doc, 'X3', x3)
      if x4 != '': do_add(doc, 'X4', x4)
      if x5 != '': do_add(doc, 'X5', x5)
      if x6 != '': do_add(doc, 'X6', x6)
      if x7 != '': do_add(doc, 'X7', x7)
      if x8 != '': do_add(doc, 'X8', x8)
      if x9 != '': do_add(doc, 'X9', x9)
      db.replace_document(item_container.item.id, doc)
      #print '.', #item_container.id, item_container.item.id
  db.flush()
  time.sleep(5);
  ic_start = ic_end

print 'Fehlerhafte Edu-Objekte', error_count
