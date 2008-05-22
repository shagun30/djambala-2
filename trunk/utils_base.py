#-*-coding: utf-8 -*-
"""
/dms/base_utils.py

.. enthaelt grundlegende Hilfefunktionen fuer 
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.05.2007  Beginn der Arbeit
0.02  07.03.2008  check_slot
0.03  07.04.2008  MAIL_ICON
"""

import  datetime, time
import  string
import  re

from django.utils.translation import ugettext as _

from dms.text_icons         import * #EXTERN_ICON, NEW_WINDOW_ICON
from dms.encode_decode      import decode_html

ACL_USERS = 'acl_users'

# -----------------------------------------------------
def convert_str_to_date(s):
  """ konvertiert (deutsches) Datum in ein Date-Objekt """
  if len(string.splitfields(s, ' ')) == 1:
    return datetime.datetime(*(time.strptime(s, '%d.%m.%Y')[0:6]))
  else:
    return datetime.datetime(*(time.strptime(s, '%d.%m.%Y %H:%M')[0:6]))

# -----------------------------------------------------
def show_email(email, info='', url_class=''):
  """ zeigt die E-Mail-Adresse """
  if info == '':
    info = email
  ret = '<a href="mailto:%s"' % email
  if url_class != '':
    ret += ' class="%s"' % url_class
  ret += '>%s</a>' % info
  return ret

# -----------------------------------------------------
def show_link(url, info='', url_extern=False, url_class='', title=''):
  """ zeigt Verweise an - externe Verweise werden optisch gekennzeichnet """
  if info == '':
    if url.startswith('http://'):
      info += url[7:]
    else:
      info = url
  from dms.settings import MY_DOMAINS
  from django.template.loader import get_template
  from django.template import Context
  t = get_template('utils/show_link.html')
  target = ''
  start  = ''
  is_my_domain = False
  # --- Parameter in URL ausschliessen
  n_pos = url.find('?')
  if n_pos > -1:
    u = url[:n_pos]
  else:
    u = url
  if u.startswith('http://'):
    my_do = MY_DOMAINS
    for domain in MY_DOMAINS:
      do = domain
      if u.find(domain) >= 0:
        is_my_domain = True
        break
    if is_my_domain:
      if url_extern:
        target = '_extern'
        start  = NEW_WINDOW_ICON
    else:
      target = '_extern'
      start  = EXTERN_ICON
  elif u.startswith('mailto:'):
    start = MAIL_ICON
  if url_class != '' and not url_class.startswith('class='):
    url_class = u' class="%s"' % url_class
  if title != '' and not title.startswith('title='):
    title = u' title="%s"' % title
  c = Context ( {'start': start, 'url' : url, 'class': url_class, 
                 'target': target, 'info': info, 'title': title } )
  u = t.render(c)
  return t.render(c)

# -----------------------------------------------------
def remove_link_icons(t):
  """ entfernt Icons, mit denen Verweise (automatisch) gekennzeichnet werden """
  EXTERN_ICON_OLD = u'<span class="red"><strong>»</strong></span> '
  NEW_WINDOW_OLD = u'<span class="red"><strong>··</strong></span> '
  t = t.replace(EXTERN_ICON_OLD + '<a', '<a')
  t = t.replace(EXTERN_ICON + '<a', '<a')
  t = t.replace(NEW_WINDOW_OLD + '<a', '<a')
  t = t.replace(NEW_WINDOW_ICON + '<a', '<a')
  t = t.replace(MAIL_ICON + '<a', '<a')
  t = t.replace('<span class="red"></span>', '')
  #t = string.replace(t, EXTERN_ICON + '<a', '<a')
  #t = string.replace(t, NEW_WINDOW_ICON + '<a', '<a')
  return t

# -----------------------------------------------------
def expand_link_icons(s):
  """ korrigiert URLs, indem externe Verweise ausgezeichnet werden """

  def get_expanded_url(u_str):

    def get_attr(u_str, attr_name):
      l = len(attr_name)+2
      search = u'%s=".*?"' % attr_name
      obj = re.search(search, u_str)
      if obj != None:
        return u_str[obj.start()+l:obj.end()-1]
      else:
        return ''

    url = get_attr(u_str, 'href')
    title = get_attr(u_str, 'title')
    target = get_attr(u_str, 'target')
    url_class = get_attr(u_str, 'class')
    obj = re.search('>.*?</a>', u_str)
    info = u_str[obj.start()+1:obj.end()-4]
    return string.strip(show_link(url, info, target, url_class, title))

  res = ''
  com = re.compile('<a.*?</a>')
  url_obj = com.search(s)
  while url_obj != None:
    start = url_obj.start()
    end = url_obj.end()
    res += s[:start]
    res += get_expanded_url(s[start:end])
    s = s[end:]
    url_obj = com.search(s)
  return res + s

# -----------------------------------------------------
def instance_dict(instance, key_format=None):
    """
    Returns a dictionary containing field names and values for the given instance
    djangosnippets 199 von SmileyCris
    """
    from django.db.models.fields.related import ForeignKey
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()
        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() \
            for obj in getattr(instance, field.attname).all()]
    return d

# -----------------------------------------------------
def links_as_text(code):
  """ ersetzt alle Vorkommen von '<a href="xxxxxxxx" ... >yyyy</a>' durch '(xxxxxxxx : yyyy)' """

  def link_as_text(code):
    ret = code
    i = code.rfind('<a href="')
    if i>-1:
      j = code.find('"', i+9)
      k = code.find('>', j)
      l = code.find('<', k)
      ret = code[:i] + '(' + code[i+9:j] + ' : ' + code[k+1:l] + ')' + code[l+4:]
    return i, ret

  i=1
  ret = code
  while i>-1:
    i, ret = link_as_text(ret)
  return ret

# -----------------------------------------------------
def html2txt(s):
  """Convert the html to raw txt
  - suppress all return
  - <p>, <tr> to return
  - <td> to tab
  version 0.0.1 20020930
  |(<li.*?>) 01.02.2008
  """
  s = links_as_text(s)
  p = re.compile('(<p.*?>)|(<tr.*?>)|(<li.*?>)', re.I)
  t = re.compile('<td.*?>', re.I)
  comm = re.compile('<!--.*?-->', re.M)
  tags = re.compile('<.*?>', re.M)
  s = s.replace('\n', '') # remove returns time this compare to split filter join
  s = p.sub('\n', s) # replace p and tr by \n
  s = t.sub('\t', s) # replace td by \t
  s = comm.sub('', s) # remove comments
  s = tags.sub('', s) # remove all remaining tags
  s = re.sub(' +', ' ', s) # remove running spaces this remove the \n and \t
  s = decode_html(s)
  # handling of entities
  return s

# -----------------------------------------------------
def check_slot(request, item_container, text_raw):
  """ prueft und ersetzt gegebenenfalls einen Programmslot """
  # Beispiel: {{ slot:hessen.schooldb.views_show.get_regionschulen(schul_amt='MR') }}
  if text_raw == '' or text_raw.find('slot') < 0:
    return text_raw
  prog = re.compile('{{[ \t]slot\:.*?}}')
  obj = prog.search(text_raw)
  while obj != None:
    f = text_raw[obj.start():obj.end()]
    f_raw = f[f.find(':')+1:-2].strip()
    pos = f_raw.find('(')
    f_param = f_raw[pos:]
    modules = string.splitfields(f_raw[:pos], '.')
    this_module = modules[-3]
    modules[-1] = this_module + '_slot_' + modules[-1] + '(request, item_container, ' + f_param[1:]
    f = u'.'.join(modules)
    from dms import *
    text_raw = text_raw[:obj.start()] + eval(f) + text_raw[obj.end():]
    obj = prog.search(text_raw)
  return text_raw

