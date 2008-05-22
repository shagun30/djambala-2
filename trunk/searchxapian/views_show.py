# -*- coding: utf-8 -*-
"""
/dms/searchxapian/views_show.py

.. zeigt Suchinterface fuer Xapian-Volltextsuche an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

Vgl. http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/

0.01  13.05.2007  Beginn der Arbeit
0.04  15.05.2007  diverse Verbesserungen der Nutzungsschnittstelle
"""
import xmlrpclib
import urllib

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template    import Context
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.settings       import SEARCH_DOMAIN
from dms.queries        import get_search_engines
from dms.queries        import get_item_container
from dms.queries        import get_site_url
from dms.utils          import get_tabbed_form
from dms.utils          import show_link
from dms.utils          import get_german_date
from dms.utils_form     import get_item_vars_add
from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.searchxapian.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def searchxapian_show(request):
  """ zeigt den Inhalt eines Dokumentes """

  SORT_BY = { -1: _(u'Relevanz'), 
               0: _(u'URL'), 
               1: _(u'Überschrift/Titel'),
               2: _(u'Datum der letzten Änderung') }
  if request.path.find('index.html') < 0:
    my_path = request.path.replace('searchxapian', 'index.html/searchxapian')
  else:
    my_path = request.path
  item_container = get_item_container(my_path, '/searchxapian/')

  def get_sort_by_choices():
    ret = []
    ret.append((-1, SORT_BY[-1]))   # Siehe SORT_BY
    ret.append((0, SORT_BY[0]))
    ret.append((1, SORT_BY[1]))
    ret.append((2, SORT_BY[2]))
    return ret

  def get_domain_choices():
    """ """
    ret = []
    ret.append( ('', _(u'Alle Seiten')) )
    if item_container != None:
      url = item_container.container.site.url[7:]
      ret.append( (url, _(u'Nur Seiten der Domaine <i>') + url + '</i>') )
    return ret

  class DmsItemForm(forms.Form):
    query    = forms.CharField(required=False, max_length=60,
                     widget=forms.TextInput(attrs={'size':60}) )
    sort_by  = forms.CharField(
                     widget=forms.Select(choices=
                                  get_sort_by_choices(),
                                  attrs={'size':4, 'style':'width:60%'} ) )
    domain   = forms.ChoiceField(required=False, choices=get_domain_choices(),
                                  widget=forms.RadioSelect() )

  def get_prev_next(query, offset, delta, domain, sort_by, count):
    aquery = u'query=%s' % urllib.quote_plus(query)
    if domain == '':
      site = ''
    else:
      site = '&domain=' + domain
    show_prev = ''
    show_next = ''
    show_middle = ''
    n_start = 0
    if count > offset + 10*delta:
      show_next_more = True
      count = offset + 10*delta
    else:
      show_next_more = False
    if offset > 10*delta:
      show_prev_more = True
      n_start = offset - 10*delta
    else:
      show_prev_more = False
    n = n_start
    while n < count:
      if n < offset:
        show_prev += show_link(u'./?%s&offset=%i&sort_by=%i%s' % (aquery, n, sort_by, site),
                               smart_unicode(n), url_class='navLink') + ' '
      elif n == offset:
        show_middle = '<b>%i</b> ' % n
      else:
        show_next += show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                               (aquery, n, sort_by, site),
                               smart_unicode(n), url_class='navLink') + ' '
      n += delta
    if show_next_more:
      show_next += show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                              (aquery, n, sort_by, site),
                              ' &raquo; Weiter', url_class='navLink')
    if show_prev_more:
      show_prev = show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                              (aquery, n_start-delta, sort_by, site),
                              'Zurück &laquo; ', url_class='navLink') + show_prev
    if count < delta:
      show_middle = ''
    return show_prev, show_middle, show_next

  def get_search_results(request):
    sort_by = -1
    offset = 0
    delta  = 20
    count = -1
    if show_errors:
      data = request.POST.copy()
      query = data['query']
      domain = data['domain']
    else:
      data = { 'query': '', 'sort_by': -1,}
      query = ''
      domain = ''
      if params.has_key('offset'):
        offset = int(params['offset'])
      if params.has_key('sort_by'):
        sort_by = int(params['sort_by'])
      if params.has_key('domain'):
        domain = params['domain']
      if params.has_key('query'):
        query = params['query']
        data = { 'query': query, 'sort_by': sort_by, 'domain': domain}
    s = xmlrpclib.Server('http://localhost:3000')
    sort_by = int(data['sort_by'])
    ascending = sort_by==2
    res = s.search(query, offset, delta, domain, sort_by, ascending)
    return res, query, offset, delta, domain, sort_by, data

  def get_link_list(rs):
    results = []
    for r in rs:
      this_link = show_link(r['url'], r['title']) + u' {%s}' % r['percent']
      # --- Siehe SORT_BY
      if sort_by == 0:
        this_link += '<br />' + r['url']
      elif sort_by == 2:
        this_link += ', ' + get_german_date(r['date'])
      results.append(this_link)
    return results

  app_name = 'searchxapian'
  my_title = _(u'Suchanfrage stellen')
  if item_container != None:
    my_absolute_url = item_container.get_absolute_url()
  else:
    my_absolute_url = './'
  show_errors = ( request.method == 'POST' )
  params = request.GET.copy()
  if params!={} or show_errors:
    res, query, offset, delta, domain, sort_by, data = get_search_results(request)
    query = decode_html(query)
    # --- Rohdaten in Liste ueberfuehren
    count = res['count']
    rs = res['results']
    results = get_link_list(rs)
    if query.find('&') >= 0:
      q = query
    else:
      try:
        q = encode_html(query.decode('iso-8859-1'))
      except:
        q = encode_html(query)
    show_prev, show_middle, show_next = \
         get_prev_next(q, offset, delta, domain, sort_by, count)
  else :
    sort_by = -1
    query = ''
    count = 20
    data = { 'query': '', 'sort_by': sort_by, 'doamin': '', }
    results = []
    show_prev = ''
    show_middle = ''
    show_next = ''

  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ('tab_base',['query',]),
           ('tab_more', ['sort_by', 'domain', ]) ]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- externe Suchmaschinen
  search_engines = get_search_engines()
  links = []
  for engine in search_engines:
    if query.find('&') < 0:
      url = engine.url_query % (urllib.quote_plus(encode_html(query.decode('iso-8859-1'))),
                                SEARCH_DOMAIN)
    else:
      url = engine.url_query % (urllib.quote_plus(query), SEARCH_DOMAIN)
    links.append(show_link(url, engine.name, url_class="navLink"))
  t = get_template('utils/info_slot_right_list_simple.html')
  c = Context ( { 'header': _(u'Externe Suche'),
                  'links': links
                } )
  slot_info_right = t.render(c)
  # --- Zur Ausgangsseite
  back_link = show_link(my_absolute_url, _(u'Zur Ausgangsseite ...'),
                        url_class="navLink")
  t = get_template('utils/info_slot_right.html')
  c = Context ( { 'header': _(u'Ausgangsseite'),
                  'info': back_link
                } )
  slot_info_right += '<br /><br />\n' + t.render(c)

  vars = get_item_vars_add(request, item_container, app_name, my_title,
                           content, show_errors)
  vars['next'] = get_site_url(item_container, 'searchxapian/')
  vars['path'] = item_container.container.path + 'searchxapian/'
  vars['sub_title'] = ''
  vars['slot_right_info'] = slot_info_right
  vars['action'] = ''
  vars['results'] = results
  vars['count'] = count
  vars['show_prev'] = show_prev
  vars['show_middle'] = show_middle
  vars['show_next'] = show_next
  vars['sort_by'] = SORT_BY[sort_by]
  vars['google_search'] = 'google'
  vars['no_top_main_navigation'] = True
  return render_to_response ( 'app/searchxapian/base.html', vars )
