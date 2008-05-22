# -*- coding: utf-8 -*-
"""
/dms/searcheduxapian/views_show.py

.. zeigt Suchinterface fuer Xapian-Volltextsuche an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

Vgl. http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/

0.01  25.09.2007  Beginn der Arbeit
"""
import xmlrpclib
import urllib
import types

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template    import Context
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.settings       import SEARCH_DOMAIN
from dms.settings       import RPC_SEARCHENGINE
from dms.queries        import get_search_engines
from dms.queries        import get_item_container
from dms.queries        import get_site_url
from dms.utils          import get_tabbed_form
from dms.utils          import show_link
from dms.utils          import get_german_date
from dms.utils_form     import get_item_vars_add
from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.edulinkitem.utils       import get_lernrestyp_choices
from dms.edulinkitem.utils       import get_fach_list
from dms.edulinkitem.utils       import get_zielgruppen_list
from dms.edulinkitem.utils       import get_schularten_list
from dms.edulinkitem.utils       import get_schulstufen_list
from dms.edulinkitem.utils       import get_sprachen_list

from dms.searchxapian.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def searcheduxapian_show(request):
  """ zeigt den Inhalt eines Dokumentes """

  SEARCH_NAME = 'searchxapianedu'
  SORT_BY = { -1: _(u'Relevanz'), 
               0: _(u'URL'), 
               1: _(u'Überschrift/Titel'),
               2: _(u'Datum der letzten Änderung') }
  found = False
  my_path = request.path
  while not found:
    if request.path.find('index.html') < 0:
      my_path = my_path.replace(SEARCH_NAME, 'index.html/'+SEARCH_NAME)
    item_container = get_item_container(my_path, '/%s/' % SEARCH_NAME)
    found = (item_container != None)
    if not found:
      my_path = my_path[:my_path.rfind('index.html')]
    #assert False

  def get_sort_by_choices():
    ret = []
    ret.append((-1, SORT_BY[-1]))   # Siehe SORT_BY
    ret.append((0, SORT_BY[0]))
    ret.append((1, SORT_BY[1]))
    ret.append((2, SORT_BY[2]))
    return ret

  def get_this_domain():
    """ liefert die URL des Lernarchivs """
    return item_container.container.site.url[7:]

  def get_domain_choices():
    """ liefert die Liste moeglicher Suchhorizonte """
    ret = []
    ret.append( ('', _(u'Alle Seiten')) )
    if item_container != None:
      url = get_this_domain()
      ret.append( (url, url) )
    return ret

  class DmsItemForm(forms.Form):
    query    = forms.CharField(required=False, max_length=60,
         widget=forms.TextInput(attrs={'size':60}) )
    sort_by  = forms.CharField(
         widget=forms.Select(choices=get_sort_by_choices(),
                             attrs={'size':4, 'style':'width:60%'} ) )
    domain   = forms.ChoiceField(required=False, choices=get_domain_choices(),
         widget=forms.RadioSelect() )
    lernrestyp = forms.MultipleChoiceField(required=False,
         choices=get_lernrestyp_choices(),
                    widget=forms.CheckboxSelectMultiple() )
    fach = forms.MultipleChoiceField(required=False,
         choices=get_fach_list(),
                    widget=forms.CheckboxSelectMultiple() )
    zielgruppe = forms.MultipleChoiceField(required=False,
         choices=get_zielgruppen_list(),
                    widget=forms.CheckboxSelectMultiple() )
    schulart = forms.MultipleChoiceField(required=False,
         choices=get_schularten_list(),
                    widget=forms.CheckboxSelectMultiple() )
    schulstufe = forms.MultipleChoiceField(required=False,
         choices=get_schulstufen_list(),
                    widget=forms.CheckboxSelectMultiple() )
    sprache = forms.MultipleChoiceField(required=False,
         choices=get_sprachen_list(),
                    widget=forms.CheckboxSelectMultiple() )
    schlagwort  = forms.CharField(required=False, max_length=80,
                       widget=forms.TextInput(attrs={'size':60}) )

  def get_extra_query(items, item_name, extra_query):
    """ """
    if items != '':
      if type(items) == types.StringType:
        items = eval(items)
      if type(items) != types.ListType:
        items = [items]
      for i in items:
        extra_query += '&' + item_name + '=' + str(i)
    return extra_query

  def get_prev_next(query, offset, delta, domain, lernrestyp, fach, zielgruppe,
                    schulart, schulstufe, sprache, schlagwort, sort_by, count):
    aquery = u'query=%s' % urllib.quote_plus(query)
    if domain == '':
      extra_query = ''
    else:
      extra_query = '&domain=' + domain
    extra_query = get_extra_query(lernrestyp, 'lernrestyp', extra_query)
    extra_query = get_extra_query(fach, 'fach', extra_query)
    extra_query = get_extra_query(zielgruppe, 'zielgruppe', extra_query)
    extra_query = get_extra_query(schulart, 'schulart', extra_query)
    extra_query = get_extra_query(schulstufe, 'schulstufe', extra_query)
    extra_query = get_extra_query(sprache, 'sprache', extra_query)
    extra_query += '&schlagwort='+schlagwort.lower()
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
        show_prev += show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                               (aquery, n, sort_by, extra_query),
                               smart_unicode(n), url_class='navLink') + ' '
      elif n == offset:
        show_middle = '<b>%i</b> ' % n
      else:
        show_next += show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                               (aquery, n, sort_by, extra_query),
                               smart_unicode(n), url_class='navLink') + ' '
      n += delta
    if show_next_more:
      show_next += show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                              (aquery, n, sort_by, extra_query),
                              ' &raquo; Weiter', url_class='navLink')
    if show_prev_more:
      show_prev = show_link(u'./?%s&offset=%i&sort_by=%i%s' % \
                              (aquery, n_start-delta, sort_by, extra_query),
                              'Zurück &laquo; ', url_class='navLink') + show_prev
    if count < delta:
      show_middle = ''
    return show_prev, show_middle, show_next

  def get_search_results(request):
    sort_by = -1
    offset = 0
    delta  = 20
    count = -1
    if has_params:
      data = request.POST.copy()
      query = data['query'].lower()
      if data.has_key('domain'):
        domain = data['domain']
      else:
        domain = ''
      lernrestyp = ''
      if data.has_key('lernrestyp'):
        lernrestyp = data.setlistdefault('lernrestyp')
      fach = ''
      if data.has_key('fach'):
        fach = data.setlistdefault('fach')
      zielgruppe = ''
      if data.has_key('zielgruppe'):
        zielgruppe = data.setlistdefault('zielgruppe')
      schulart = ''
      if data.has_key('schulart'):
        schulart = data.setlistdefault('schulart')
      schulstufe = ''
      if data.has_key('schulstufe'):
        schulstufe = data.setlistdefault('schulstufe')
      sprache = ''
      if data.has_key('sprache'):
        sprache = data.setlistdefault('sprache')
      schlagwort = ''
      if data.has_key('schlagwort'):
        schlagwort = data['schlagwort']
    else:
      data = { 'query': '', 'sort_by': -1,}
      query = ''
      domain = get_this_domain()
      lernrestyp = ''
      if params.has_key('lernrestyp'):
        lernrestyp = params.setlistdefault('lernrestyp')
      fach = ''
      if params.has_key('fach'):
        fach = params.setlistdefault('fach')
      zielgruppe = ''
      if params.has_key('zielgruppe'):
        zielgruppe = params.setlistdefault('zielgruppe')
      schulart = ''
      if params.has_key('schulart'):
        schulart = params.setlistdefault('schulart')
      schulstufe = ''
      if params.has_key('schulstufe'):
        schulstufe = params.setlistdefault('schulstufe')
      sprache = ''
      if params.has_key('sprache'):
        sprache = params.setlistdefault('sprache')
      schlagwort = ''
      if params.has_key('schlagwort'):
        schlagwort = params['schlagwort']
      if params.has_key('offset'):
        offset = int(params['offset'])
      if params.has_key('sort_by'):
        sort_by = int(params['sort_by'])
      if params.has_key('domain'):
        domain = params['domain']
      if params.has_key('query'):
        query = params['query'].lower()
        data = { 'query': query, 
                 'sort_by': sort_by, 
                 'domain': domain,
                 'lernrestyp': lernrestyp,
                 'fach': fach,
                 'zielgruppe': zielgruppe,
                 'schulart': schulart,
                 'schulstufe': schulstufe,
                 'sprache': sprache,
                 'schlagwort': schlagwort}
    s = xmlrpclib.Server(RPC_SEARCHENGINE)
    sort_by = int(data['sort_by'])
    ascending = sort_by==2
    res = s.search_edu(query, offset, delta, domain, lernrestyp, fach, zielgruppe,
                       schulart, schulstufe, sprache, schlagwort, 
                       sort_by, ascending)
    return res, query, offset, delta, domain, str(lernrestyp), str(fach), \
           str(zielgruppe), str(schulart), schulstufe, sprache, schlagwort, \
           sort_by, data

  def get_link_list(rs):
    """ liefert aufbereitete Link-Liste """
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

  # --- Hauptroutine
  app_name = 'searchxapian'
  my_title = _(u'Suchanfrage in den Lernarchiven')
  my_absolute_url = item_container.get_absolute_url()
  has_params = (request.method == 'POST')
  # wurden Parameter in der URL uebergeben?
  params = request.GET.copy()
  if params!={} or has_params:
    res, query, offset, delta, domain, lernrestyp, fach, zielgruppe, schulart,\
    schulstufe, sprache, schlagwort, sort_by, data = get_search_results(request)
    q = query
    query = decode_html(query)
    try:
      q2 = query.decode('iso--8859-1')
    except:
      q2 = query
    # --- Rohdaten in Liste ueberfuehren
    count = res['count']
    rs = res['results']
    results = get_link_list(rs)
    if query.find('&') >= 0:
      q = query
    else:
      q = encode_html(query)
    show_prev, show_middle, show_next = \
         get_prev_next(q, offset, delta, domain, lernrestyp, fach, zielgruppe,
                       schulart, schulstufe, sprache, schlagwort, sort_by, count)
  else:
    count = 0
    sort_by = -1
    query = ''
    domain = ''
    data = { 'query': query,
             'sort_by': sort_by,
             'domain': domain, }
    results = []
    show_prev = ''
    show_middle = ''
    show_next = ''

  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ('tab_base',['query', ]),
           ('tab_course', ['fach', ]),
           ('tab_description', ['lernrestyp', ]),
           ('tab_details', ['zielgruppe', 'schulart', 'schulstufe', 'sprache' ]),
           ('tab_keyword', ['schlagwort', ]),
           ('tab_more', ['sort_by', 'domain' ]),
         ]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- externe Suchmaschinen
  search_engines = get_search_engines()
  links = []
  for engine in search_engines:
    if query.find('&') < 0:
      url = engine.url_query % (urllib.quote_plus(query.encode("utf-8")), SEARCH_DOMAIN)
    else:
      url = engine.url_query % (urllib.quote_plus(query.encode("utf-8")), SEARCH_DOMAIN)
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
                           content, has_params)
  vars['next'] = get_site_url(item_container, SEARCH_NAME+'/')
  vars['path'] = item_container.container.path + SEARCH_NAME + '/'
  vars['sub_title'] = ''
  vars['slot_right_info'] = slot_info_right
  vars['action'] = ''
  vars['results'] = results
  vars['count'] = count
  vars['show_prev'] = show_prev
  vars['show_middle'] = show_middle
  vars['show_next'] = show_next
  vars['sort_by'] = SORT_BY[sort_by]
  vars['no_top_main_navigation'] = True
  ajax_url = get_site_url(item_container, '/ajax/searcheduxapian_ajax_get_schlagwort/')
  t_org = get_template('app/searchxapian/ajax_get_schlagwort.html')
  vars['ajax'] = t_org.render(Context({ 'ajax_url': ajax_url, }))
  return render_to_response ( 'app/searchxapian/base_edu.html', vars )
