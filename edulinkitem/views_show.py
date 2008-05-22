# -*- coding: utf-8 -*-
"""
/dms/edulinkitem/views_show.py

.. zeigt den Inhalt eines Verweises innerhalb der Online-Lernarchive an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.07.2007  Beginn der Arbeit
0.02  05.09.2007  get_schlagwort_by_stem
0.03  19.10.2007  Anzeige der Metadaten-URL
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.settings       import MP3_DOWNLOAD

from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_eduitem
from dms.queries        import get_medienformat_by_id
from dms.queries        import get_edu_org_beschreibung
from dms.queries        import get_schlagwort_by_stem
from dms.queries        import get_linked_item_containers
from dms.queries        import get_data_item_container

from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms.edulinkitem.utils  import get_description_link

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_url(item_container):
  """ liefert die passende Adresse """
  if item_container.item.url_more.find('stream://') == 0:
    return MP3_DOWNLOAD + item_container.item.url_more[9:]
  else:
    return item_container.item.url_more

# -----------------------------------------------------
def get_details(item_container, show_all, data):
  """ erzeugt die Detail-Sicht des Edu-Verweises """

  def get_item_list(query_set):
    ret = ''
    for q in query_set.all():
      if ret != '':
        ret += ' <b>&middot;</b> '
      ret += q.name
    return ret

  def get_item_list_by_list(items):
    ret = ''
    for i in items:
      if ret != '':
        ret += ' <b>&middot;</b> '
      ret += i
    return ret

  def get_schlagworte_sorted(schlagworte):
    """ uebersetzt die gestemmten Schlagwoerter in die ursruenglichen Schlagwoerter """
    items = []
    for schlagwort in schlagworte.all():
      items.append(get_schlagwort_by_stem(schlagwort))
    items.sort()
    return get_item_list_by_list(items)

  tDetails = get_template('app/edulinkitem/show_more.html')
  if item_container.item.app.name == 'dmsEduLinkItem':
    if item_container.item.url_more.find('stream://') == 0:
      eduobject_url = show_link(get_url(item_container))
    else:
      eduobject_url = show_link(get_url(item_container))
  else:
    eduobject_url = show_link(item_container.get_absolute_url())
  eduobject_virtual_urls = ''
  for ic in get_linked_item_containers(item_container):
    if eduobject_virtual_urls != '':
      eduobject_virtual_urls += '<br />\n'
    eduobject_virtual_urls += get_description_link(ic, False)
  if item_container.item.string_2 != '' and item_container.item.app.name != 'dmsEduExerciseItem':
    eduobject_description_url = show_link(item_container.item.string_2) + '<br />\n' + \
                                get_description_link(get_data_item_container(item_container))
  else:
    eduobject_description_url = get_description_link(get_data_item_container(item_container))
  if data != None:
    schlagworte_sorted = get_schlagworte_sorted(data.schlagwort)
    details = Context( {
                        'show_all': show_all,
                        'eduobject_lernrestyp': get_lernrestyp_by_id(
                                                    item_container.item.integer_3).name,
                        'eduobject_url': eduobject_url,
                        'eduobject_description_url': eduobject_description_url,
                        'eduobject_virtual_urls': eduobject_virtual_urls,
                        'fach_sachgebiet': get_item_list(data.fach_sachgebiet),
                        'titel_lang': data.titel_lang,
                        'schlagwort': schlagworte_sorted,
                        'medienformat':
                            get_medienformat_by_id(item_container.item.integer_4),
                        'zielgruppe': get_item_list(data.zielgruppe),
                        'schulstufe': get_item_list(data.schulstufe),
                        'schulart': get_item_list(data.schulart),
                        'lernzeit': data.lernzeit,
                        'methodik': data.methodik,
                        'lehrplan': data.lehrplan,
                        'standards_kmk': data.standards_kmk,
                        'standards_weitere': data.standards_weitere,
                        'lernziel': data.lernziel,
                        'autor': data.autor,
                        'herausgeber': data.herausgeber,
                        'isbn': data.isbn,
                        'preis': data.preis,
                        'rechte': data.rechte,
                        'anbieter': data.anbieter_herkunft,
                        'techn_voraus': data.techn_voraus,
                        'sprache': get_item_list(data.sprache),
                        'einrichtung':
                            get_edu_org_beschreibung(item_container.item.string_1),
                        'einsteller': item_container.item.owner.get_full_name(),
                        'last_modified': item_container.get_last_modified(),
                      } )
  else:
    details = Context( {
                        'show_all': show_all,
                        'eduobject_lernrestyp': get_lernrestyp_by_id(
                                                    item_container.item.integer_3).name,
                        'eduobject_url': eduobject_url,
                        'eduobject_description_url': eduobject_description_url,
                        'eduobject_virtual_urls': eduobject_virtual_urls,
                        'medienformat':
                            get_medienformat_by_id(item_container.item.integer_4),
                        'einrichtung':
                            get_edu_org_beschreibung(item_container.item.string_1),
                        'einsteller': item_container.item.owner.get_full_name(),
                        'last_modified': item_container.get_last_modified(),
                      } )
  return tDetails.render(details)

# -----------------------------------------------------
def edulinkitem_show(request, item_container):
  """ zeigt Details des Verweises an """
  app_name = 'edulinkitem'
  vars = get_item_vars_show(request, item_container, app_name)
  url = get_url(item_container)
  if url.rfind('.mp3') > 0:
    info = _(u'Zur Audio-Datei ...')
  elif url.rfind('.pdf') > 0:
    info = _(u'Zur PDF-Datei ...')
  else:
    info = _(u'Zum Material ...')
  vars['title_info'] = show_link(url, info)
  data = get_eduitem(item_container.item)
  if data != None:
    if data.beschreibung_lang != '':
      vars['text_more'] += data.beschreibung_lang
  vars['text_more'] += get_details(item_container, request.GET.has_key('show_all'), data)
  parent = item_container.get_parent()
  if parent.item.has_comments:
    comments = item_comment(request, item_container=item_container)
  else:
    comments = ''
  vars['comments'] = comments
  visibility = u', <i>[' + u'%s-%s' % \
                ( item_container.visible_start.strftime('%d.%m.%Y'),
                  item_container.visible_end.strftime('%d.%m.%Y') ) + u']</i>'
  vars['last_modified'] = item_container.get_last_modified() + visibility
  return render_to_response ( 'base-full-width.html', vars )
