# -*- coding: utf-8 -*-
"""
/dms/edumediaitem/views_show.py

.. zeigt den Inhalt des Medienpakets in einem Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  11.09.2007  Beginn der Arbeit
0.02  28.09.2007  Mini-Bilder anzeigen
0.03  29.10.2007  alternative Darstellung
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_data_item_container
from dms.queries        import get_eduitem

from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link

from dms.folder.utils   import get_folder_content as get_folder_folder_content
from dms.file.utils     import get_file_url
from dms.edulinkitem.views_show import get_details
from dms.edumediaitem.utils  import get_user_support
from dms.edufolder.utils  import get_folder_content
from dms.edufileitem.utils  import get_edu_file_url
from dms.newsboard.utils  import get_folder_content as get_newsboard_content
from dms.views_comment  import item_comment

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edumediaitem_show(request, item_container):
  """ zeigt den Inhalt eines Materialpools """

  app_name = 'edumediaitem'
  # --- Detail-Ansicht
  if request.GET.has_key('show_details'):
    vars = get_item_vars_show(request, item_container, app_name,
                              ignore_own_breadcrumb=True)
    data = get_eduitem(item_container.item)
    vars['text_more'] += get_details(item_container, True, data)
    if data.beschreibung_lang != '':
      vars['text'] += data.beschreibung_lang
    if item_container.item.has_comments:
      comments = item_comment(request, item_container=item_container)
    else:
      comments = ''
    vars['comments'] = comments
    return render_to_response ( 'base-full-width.html', vars )

  def get_item_data(i, links):
    """ extrahiert die entsprechenden Informationen """
    tEduLrSection = get_template('app/edufolder/lernres_section.html')
    edu_object_url = i.get_absolute_url()
    if i.item.app.name == 'dmsEduTextItem':
      url = show_link(i.get_absolute_url(), i.item.title)
      info = _(u'Text')
    elif i.item.app.name == 'dmsEduFileItem':
      url = show_link(get_edu_file_url(i), i.item.title)
      info = _(u'Datei')
    elif i.item.app.name == 'dmsEduMediaItem':
      url = show_link(i.get_absolute_url(), i.item.title)
      info = _(u'Medienpaket')
      edu_object_url += '?show_details=1'
    elif i.item.app.name == 'dmsEduWebquestItem':
      url = show_link(i.get_absolute_url(), i.item.title)
      info = _(u'Webquest')
      edu_object_url += '?show_details=1'
    else:
      url = show_link(i.item.url_more, i.item.title)
      info = _(u'Verweis')
    t = '%s / <span class="grey">%s</span>' % (url, info)
    if i.item.integer_1 != 0:
      t = '<i>%s</i>' % i.item.title
      info = _(u'<p>Nur für Fach-Community-Mitglieder</p>')
      cSection = Context ( { 'title': t,
                             'text': info,
                            } )
    elif i.item.integer_2 != 0:
      t = '<i>%s</i>' % i.item.title
      info = _(u'<p>Nur für Schulverbünde</p>')
      cSection = Context ( { 'title': t,
                             'text': info,
                            } )
    else:
      cSection = Context ( { 'title': t,
                              'text': i.item.text,
                              'image_url': i.item.image_url,
                              'image_url_url': i.item.image_url_url,
                              'id': i.item.id,
                              'edu_object_url': edu_object_url } )
    links.append(tEduLrSection.render(cSection))
    return links

  def get_section_view(news_item_container, items, sections, width, lrtypen, d_lrtypen):
    """ erzeugt die nach Lernressourcen geordnete Sicht auf die Edu-Objekte """

    def get_edu_objects(lrtypen):
      """ liefert die Edu-Objekte """

      def get_name(lernrestyp):
        pat = '<a name="' + pat_section  + '"></a>\n'
        return pat % d_lrtypen[lernrestyp].id

      tEduLrSection = get_template('app/edufolder/lernres_section.html')
      tEduLernres = get_template('app/edufolder/lernres.html')
      lernrestyp = '-2'
      links = []
      content = ''
      """
      Belegung der Joker-Felder in DmsItem:
      string_1  = quelle_id
      string_2  = lokal_id
      integer_1 = community_id
      integer_2 = schulverbund_id
      integer_3 = lern_res_typ_id
      integer_4 = medienformat_id
      integer_5 = zertifikat_id
      """
      for i in lrtypen:
        if i.item.integer_3 > 0:
          if lernrestyp != i.item.integer_3:
            #l = lernrestyp
            if lernrestyp != -2 and links != []:
              cSection = Context ( { 'section': get_lernrestyp_by_id(lernrestyp),
                                     'links': links } )
              content += get_name(lernrestyp) + tEduLernres.render(cSection)
            lernrestyp = i.item.integer_3
            links = []
          links = get_item_data(i, links)
      if int(lernrestyp) != -2 and links != []:
        cSection = Context ( { 'section': get_lernrestyp_by_id(lernrestyp),
                               'links': links } )
        content += get_name(lernrestyp) + tEduLernres.render ( cSection)
      elif int(lernrestyp) == -2 and links != []:
        cSection = Context ( { 'section': _(u'Weitere Objekte'),
                               'links': links } )
        content += tEduLernres.render ( cSection)
      return content

    # --- "Hauptprogramm"
    pat_section = 'section_%i'
    content = get_edu_objects(lrtypen)

    return content

  def get_sections_section_view(items, sections):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/edufolder/lernres.html')
    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    for i in items :
      if section != i.section :
        if section != unknown :
          if section != '--START--' and links != [] :
            cSection = Context ( { 'section': section, 'links': links } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          links = []
      links = get_item_data(i, links)
      #links.append(get_link_by_item_container(i))
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return content

  # --- Objekte des Medienpakets zeigen
  width = '180px'
  if item_container.container.sections.strip() != '':
    items, sections, d_sections = get_folder_folder_content(item_container)
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_sections_section_view(items, sections))
  else:
    news_item_container, \
    items, \
    sections, \
    lrtypen, \
    d_lrtypen, \
    lr_typen = get_folder_content(item_container)
    vars = get_folderish_vars_show(request, item_container, app_name,
              get_section_view(news_item_container, items, sections, width,
                                lrtypen, d_lrtypen),
              get_user_support(item_container, request.user.is_authenticated()))
  edu_item = get_eduitem(item_container.item)
  vars['text_more'] += edu_item.beschreibung_lang
  return render_to_response ( 'app/base_folderish.html', vars )
