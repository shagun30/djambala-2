#-*-coding: utf-8 -*-
"""
/dms/encode_decode.py

.. enthaelt Routinen zum Kodieren und Dekodieren von HTML/Umlauten
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.05.2007  Beginn der Arbeit
0.02  10.10.2007  unichr
0.3   14.12.2007  decode_html_dir
"""

import  re
from htmlentitydefs import codepoint2name, name2codepoint

from django.utils.encoding  import smart_unicode
from django.utils.translation import ugettext as _

# -----------------------------------------------------
def encode_html(text):
  """ wandelt Sonderzeichen in HTML-Entities um, Quelle: Unicode to HTML entities """
  try:
    return u"".join([codepoint2name.has_key(ord(x)) \
           and '&%s;' % codepoint2name[ord(x)] or x for x in unicode(text)])
  except:
    return u"".join([codepoint2name.has_key(ord(x)) \
         and '&%s;' % codepoint2name[ord(x)] or x for x in text])

# -----------------------------------------------------
#def decode_html(text):
#  """ wandelt HTML-Entities in normale Zeichen um """
#  if text == None:
#    return None
#  text = text.replace(u'„', u'"').replace(u'“', u'"')
#  text = text.replace('&ndash;','-'). replace('&bdquo;','"').replace('&ldquo;','"').replace('&euro;',u'€')
#  print text
#  try:
#    return re.sub('&(%s);' % '|'.join(name2codepoint),
#                lambda m: unichr(name2codepoint[m.group(1)]), text.encode('iso-8859-15'))
#  except:
#    return re.sub('&(%s);' % '|'.join(name2codepoint),
#                lambda m: chr(name2codepoint[m.group(1)]), text.encode('iso-8859-15')).\
#                decode('iso-8859-15')

# -----------------------------------------------------
def _replace_entity(m):
     s = m.group(1)
     if s[0] == u'#':
         s = s[1:]
         try:
             if s[0] in u'xX':
                 c = int(s[1:], 16)
             else:
                 c = int(s)
             return unichr(c)
         except ValueError:
             return m.group(0)
     else:
         try:
             return unichr(name2codepoint[s])
         except (ValueError, KeyError):
             return m.group(0)

_entity_re = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")
def decode_html(s):
  """ wandelt HTML-Entities in normale Zeichen um
  http://mail.python.org/pipermail/python-list/2007-January/424262.html
  """
  if s == None:
    return s
  s = s.replace('&#145;', "'").replace('&#146;', "'").replace('&#147;', '"').replace('&#148;', '"')\
       .replace('&#149;', '&middot;').replace('&#150;', '-').replace('&#151;', '-')\
       .replace('&#128;', u'€').replace('&#130;', "'").replace('&#132;', '"').replace('&#65533;', ' ')\
       .replace('&#1048707;', ' ')\
       .replace('&ndash;', '-').replace('&rarr;', '->').replace('&rArr;', '->').replace('&#8594;', '->')\
       .replace('&harr;', '<->')
  return _entity_re.sub(_replace_entity, s)

# -----------------------------------------------------
def encode_html_dir(new):
  """ konvertiert bestimmte Spalte in HTML-Entities """

  def encode(key):
    return encode_html(unicode(new[key]))

  if new.has_key('title') and new['title'].find('&') < 0:
    new['title'] = encode('title')
  if new.has_key('sub_title') and new['sub_title'].find('&') < 0:
    new['sub_title'] = encode('sub_title')
  if new.has_key('sections') and new['sections'].find('&') < 0:
    new['sections'] = encode('sections')
  if new.has_key('section') and new['section'].find('&') < 0:
    new['section'] = encode('section')
  if new.has_key('anti_spam_question'):
    new['anti_spam_question'] = encode('anti_spam_question')
  return new

# -----------------------------------------------------
def decode_html_dir(new):
  """ konvertiert bestimmte Spalte in HTML-Entities """

  def decode(key):
    return decode_html(unicode(new[key]))

  if new.has_key('title') and new['title'].find('&') >= 0:
    new['title'] = decode('title')
  if new.has_key('sub_title') and new['sub_title'].find('&') >= 0:
    new['sub_title'] = decode('sub_title')
  if new.has_key('text') and new['text'].find('&') >= 0:
    new['text'] = decode('text')
  if new.has_key('text_more') and new['text_more'].find('&') >= 0:
    new['text_more'] = decode('text_more')
  if new.has_key('sections') and new['sections'].find('&') >= 0:
    new['sections'] = decode('sections')
  if new.has_key('section') and new['section'].find('&') >= 0:
    new['section'] = decode('section')
  if new.has_key('anti_spam_question'):
    new['anti_spam_question'] = decode('anti_spam_question')
  return new
