# -*- coding: utf-8 -*-
"""
/dms/edufileitem/views_show.py

.. zeigt den Inhalt einer Datei innerhalb der Online-Lernarchive an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.09.2007  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_eduitem
from dms.queries        import get_medienformat_by_id
from dms.queries        import get_edu_org_beschreibung
from dms.queries        import get_schlagwort_by_stem
from dms.queries        import get_data_item_container
from dms.queries        import get_linked_item_containers

from dms.utils          import show_link
from dms.utils_form     import get_item_vars_show
from dms.views_comment  import item_comment

from dms.edulinkitem.utils  import get_description_link

from dms.edufileitem.utils  import get_edu_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_details(item_container):
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

  data = get_eduitem(item_container.item)
  schlagworte_sorted = get_schlagworte_sorted(data.schlagwort)
  tDetails = get_template('app/edufileitem/show_more.html')
  eduobject_virtual_urls = ''
  for ic in get_linked_item_containers(item_container):
    if eduobject_virtual_urls != '':
      eduobject_virtual_urls += '<br />\n'
    eduobject_virtual_urls += get_description_link(ic, False)
  if item_container.item.string_2 != '':
    eduobject_description_url = show_link(item_container.item.string_2) + '<br />\n' + \
                                get_description_link(get_data_item_container(item_container))
  else:
    eduobject_description_url = get_description_link(get_data_item_container(item_container))
  details = Context( {
                       'eduobject_lernrestyp': get_lernrestyp_by_id(
                                                   item_container.item.integer_3).name,
                       'beschreibung_lang': data.beschreibung_lang,
                       'eduobject_url': show_link(get_edu_file_url(item_container)),
                       'eduobject_description_url': eduobject_description_url,
                       'eduobject_virtual_urls': eduobject_virtual_urls,
                       'fach_sachgebiet': get_item_list(data.fach_sachgebiet),
                       'titel_lang': data.titel_lang,
                       'schlagwort': schlagworte_sorted,
                       'medienformat': get_medienformat_by_id(item_container.item.integer_4),
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
                       'einrichtung': get_edu_org_beschreibung(item_container.item.string_1),
                       'einsteller': item_container.item.owner.get_full_name(),
                       'last_modified': item_container.get_last_modified(),
                     } )
  return data.beschreibung_lang + tDetails.render(details)

# -----------------------------------------------------
def edufileitem_show(request, item_container):
  """ zeigt Details des Verweises an """
  app_name = 'edutextitem'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text_more'] += get_details(item_container)
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
