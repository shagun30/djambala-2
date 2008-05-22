# -*- coding: utf-8 -*-
"""
/dms/edufolder/views_show.py

.. zeigt den Inhalt eines Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  05.06.2007  Beginn der Arbeit
0.02  09.10.2007  MP3_DOMAIN, CURRICULUM_DOMAIN
0.03  17.10.2007  string_1, string_2, Redirects werden anders angezeigt
0.04  07.11.2007  MP3-Dateien werden auch zum Download angeboten
0.05  04.03.2008  Anbindung an neue Fortbildungsdatenbank
0.06  11.03.2008  dmsEduScormItem
0.07  03.04.2008  das Datum des aktuellsten Beitrags wird angezeigt
"""

import datetime

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect
from django.template    import Context
from django.template.loader import get_template
from django.utils.safestring import SafeData, mark_safe, SafeUnicode
from django.utils.translation import ugettext as _

from dms.settings       import CURRICULUM_DOMAIN
from dms.settings       import MP3_DOMAIN
from dms.settings       import MP3_DOWNLOAD
from dms.settings       import ELIXIER_LOGOS_URL
from dms.settings       import EDUFOLDER_TRAINING_URL
from dms.text_icons     import SEPERATOR_ICON_GREY

from dms.text_icons     import SEPERATOR_ICON
from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_data_item_container
from dms.queries        import get_fach_by_id
from dms.queries        import get_schulart_by_id
from dms.queries        import get_base_site_url
from dms.queries        import get_site_url

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import get_link_by_item_container
from dms.utils_base     import show_link

from dms.encode_decode  import decode_html

from dms.edufolder.utils  import get_user_support
from dms.edufolder.utils  import get_extra
from dms.edufolder.utils  import get_image_url
from dms.edufolder.utils  import get_folder_content
from dms.newsboard.utils  import get_folder_content as get_newsboard_content

from dms.edufileitem.utils  import get_edu_file_url
from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def edufolder_show(request, item_container):
  """ zeigt den Inhalt eines Lernarchivs """

  
  def get_info_slot():
    """ """
    tSection = get_template('app/edufolder/infos.html')
    cSection = Context ( { 'path': item_container.container.path, } )
    info = tSection.render(cSection)
    tSection = get_template('utils/info_slot_right_command.html')
    cSection = Context ( { 'header': _(u'Informationen'),
                           'info': info, } )
    return '<br />\n<br />\n' + tSection.render(cSection)

  def get_redirect_slot():
    """ """
    if item_container.item.url_more=='':
      return ''
    redirects = []
    links = []
    if item_container.item.string_1 != '':
      wiki_name = item_container.item.string_1
      links.append(show_link(item_container.item.url_more, wiki_name, url_class='navLink'))
    else:
      links.append('<br /><a href="%s" target="_extern" /><img src="%s%s" /></a>\n' % \
                   (item_container.item.url_more, ELIXIER_LOGOS_URL, 'wikipedia.png'))
      wiki_name = _(u'Wikipedia')
      links.append(show_link(item_container.item.url_more, wiki_name, url_class='navLink'))
    tSection = get_template('app/edufolder/see_also.html')
    info = tSection.render(Context ( { 'links': links, } ))
    tSection = get_template('utils/info_slot_right.html')
    cSection = Context ( { 'header': _(u'Siehe auch ...'),
                            'info': info, } )
    return tSection.render(cSection)

  def get_fortbildung_slot():
    """ """
    import  urllib

    def add_to_url(url, extra, key):
      def correct_umlaute(value):
        return value.replace(u'%26ouml%3B', u'%F6').replace(u'%26auml%3B', u'%E4').replace(u'%26uuml%3B', u'%FC')

      try:
        value = extra[key]
      except:
        return url
      if value == '':
        return url
      if url != '':
        url += '&'
      if key in ['fach', 'schulart']:
        url += '%s=%s' % (key, value)
      elif key == 'freie_suche':
        v = value.encode('iso-8859-15')
        url += u'%s=%s' % (key, correct_umlaute(urllib.quote_plus(v)))
      return url

    extra = get_extra(item_container)
    if extra == None:
      return ''
    url = ''
    url = add_to_url(url, extra, 'fach')
    url = add_to_url(url, extra, 'schulart')
    url = add_to_url(url, extra, 'freie_suche')
    if url == '':
      return ''
    url = EDUFOLDER_TRAINING_URL + '?' + url #+ '&query_typ=Kombiniert&submit=Filtern+...'
    tSection = get_template('app/edufolder/infos.html')
    cSection = Context ( { 'path': item_container.get_absolute_url(), } )
    info = show_link(url, 'Fortbildungsangebote', True)
    tSection = get_template('utils/info_slot_right.html')
    cSection = Context ( { 'header': _(u'Fortbildung'),
                           'info': info, } )
    return tSection.render(cSection)

  def get_section_view(news_item_container, items, sections, width, lrtypen, d_lrtypen, last_modified):
    """ erzeugt die nach Lernressourcen geordnete Sicht auf die Edu-Objekte """

    def get_news_items(news_item_container, last_modified):
      """ liefert die Nachrichten dieses Archivs """
      if news_item_container < 0:
        return '', last_modified
      fSection = get_template('app/folder/section.html')
      item_containers = get_newsboard_content(news_item_container)
      if len(item_containers) > 0:
        links = []
        for i in item_containers:
          if not i.item.app.is_folderish:
            links.append(show_link(i.get_absolute_url(), i.item.title))
            if last_modified < i.last_modified:
              last_modified = i.last_modified
        all_news = show_link(news_item_container.get_absolute_url(),
                             _(u'zum Nachrichtenbrett'))
        nSection = Context( { 'section': _(u'Aktuelle Informationen'),
                              'to_top_of_page': ' / '  + all_news,
                              'width': '30px',
                              'list_style': 'outside',
                              'links': links, } )
        news_section = fSection.render(nSection) + '<br />\n'
      else:
        news_section = ''
      return news_section, last_modified

    def get_local_menu(lr_typen, d_lrtypen):
      """ liefert das lokale Menue fuer dieses Lernarchiv """
      local_menu = ''
      n_local = 0
      for lr in lr_typen:
        if local_menu != '':
          local_menu += ' %s ' % SEPERATOR_ICON_GREY
        n_local += 1
        i = lr.id
        #hr ?? local_menu += show_link('#' + pat_section % d_lrtypen[lr.id].id, lr.name,
        #                        url_class='navLink')
        local_menu += show_link('#' + pat_section % lr.id, lr.name,
                                url_class='navLink')
      if n_local < 2:
        return ''
      return _(u'Materialtypen: ') + local_menu

    def get_edu_folders(items, local_menu, sections, last_modified):
      """ liefert die Liste der enthaltenen EduFolders """
      tSection = get_template('app/edufolder/section.html')
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
              if last_modified < i.last_modified:
                last_modified = i.last_modified
            #if decode_html(i.section) in sections :
            if i.section in sections :
              section = i.section
            else :
              section = unknown
            links = []
        if i.is_browseable:
          links.append(get_link_by_item_container(i, True))
      if section in ['--START--', unknown]:
        section = ''
      cSection = Context ( { 'section': section, 
                             'links': links,
                             'local_menu': local_menu } )
      content += tSection.render ( cSection)
      if item_container.get_parent().item.app.name == 'dmsEduFolder':
        if len(items) > 0:
          my_title = _(u'Unterarchive')
        else:
          my_title = _(u'Auswahl der Materialtypen')
      else:
        my_title = _(u'"Wegweiser" zu den Lernarchiven')
      image_url = get_image_url(item_container)
      if image_url != '':
        tFSection = get_template('app/edufolder/subfolders_with_image.html')
        folder_section = Context( { 'title': my_title,
                                    'image_url': image_url,
                                    'width': width,
                                    'content': content } )
      else:
        tFSection = get_template('app/edufolder/subfolders.html')
        folder_section = Context( { 'title': my_title,
                                    'content': content } )
      return tFSection.render(folder_section), last_modified

    def get_edu_objects(lrtypen, last_modified):
      """ liefert die Edu-Objekte """

      def get_name(lernrestyp):
        pat = '<a name="' + pat_section  + '"></a>\n'
        return pat % lernrestyp

      def get_top_of_page_url():
        return ' &nbsp;&nbsp;&nbsp; <a href="#start_of_page" class="frameLink">%s</a>\n' % \
               _(u'&rarr; Seitenanfang ...')

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
        if last_modified < i.last_modified:
          last_modified = i.last_modified
        if i.item.integer_3 > 0:
          if lernrestyp != i.item.integer_3:
            #l = lernrestyp
            if lernrestyp != -2 and links != []:
              cSection = Context ( { 'section': get_lernrestyp_by_id(lernrestyp),
                                     'to_top_of_page': get_top_of_page_url(),
                                     'links': links } )
              content += get_name(lernrestyp) + tEduLernres.render(cSection)
            lernrestyp = i.item.integer_3
            links = []
          edu_object_url = i.get_absolute_url()
          if i.item.app.name == 'dmsEduTextItem':
            url = show_link(i.get_absolute_url(), i.item.title)
            info = _(u'Text')
          elif i.item.app.name == 'dmsEduFileItem':
            url = show_link(get_edu_file_url(i), i.item.title, i.item.url_more_extern)
            info = _(u'Datei')
          elif i.item.app.name == 'dmsEduScormItem':
            url = '%s?show_index=1' % i.get_absolute_url()
            #url = '%s/scorm/' % get_edu_file_url(i)
            #url = url[:url.rfind('.')] + '/'
            url = show_link(url, i.item.title, i.item.url_more_extern)
            info = _(u'Scorm-Paket')
          elif i.item.app.name in ['dmsEduWebquestItem', 'dmsEduMediaItem',
                                   'dmsEduGalleryItem', 'dmsEduExerciseItem']:
            if i.is_data_object:
              url = show_link(i.get_absolute_url(), i.item.title)
              edu_object_url += '?show_details=1'
            else:
              ic = get_data_item_container(i)
              url = '&raquo; ' + show_link(ic.get_absolute_url(), i.item.title,
                    title=_(u'Einblendung: Inhalt erscheint an anderer Stelle ...'))
              edu_object_url = ic.get_absolute_url() + '?show_details=1'
            if i.item.app.name == 'dmsEduMediaItem':
              info = _(u'Medienpaket')
            elif i.item.app.name == 'dmsEduGalleryItem':
              info = _(u'Galerie')
            elif i.item.app.name == 'dmsEduWebquestItem':
              info = _(u'Webquest')
            elif i.item.app.name == 'dmsEduExerciseItem':
              info = _(u'Aufgabe')
          else:
            if i.item.url_more.find('stream://') == 0:
              mp3 = MP3_DOWNLOAD + i.item.url_more[9:]
              url = show_link(mp3, i.item.title)
            else:
              url = show_link(i.item.url_more, i.item.title)
            info = _(u'Verweis')
          if not i.is_data_object and i.item.app.name != 'dmsEduLinkItem':
            url = '&raquo;' + url
          t = '%s / <span class="grey">%s</span>' % (url, info)
          if i.item.integer_1 != 0:
            t = '<i>%s</i>' % i.item.title
            info = _(u'<p>Nur fur Fach-Community-Mitglieder</p>')
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
                                  'image_url': i.item.image_url,
                                  'image_url_url': i.item.image_url_url,
                                  'text': i.item.text,
                                  'id': i.item.id,
                                  'edu_object_url': edu_object_url,
                                  'is_data_object': i.is_data_object } )
          links.append(tEduLrSection.render(cSection))
          if last_modified < i.last_modified:
            last_modified = i.last_modified
      if lernrestyp != -2 and links != []:
        cSection = Context ( { 'section': get_lernrestyp_by_id(lernrestyp),
                               'to_top_of_page': get_top_of_page_url(),
                               'links': links } )
        content += get_name(lernrestyp) + tEduLernres.render ( cSection)
      return content, last_modified

    # --- "Hauptprogramm"
    pat_section = 'section_%i'
    content = ''
    news, last_modified = get_news_items(news_item_container, last_modified)
    content += news
    folders, last_modified = get_edu_folders(items, get_local_menu(lr_typen, d_lrtypen), sections, last_modified)
    content += folders
    objects, last_modified = get_edu_objects(lrtypen, last_modified)
    content += objects
    return content, last_modified

  # --- Soll an eine andere Adresse weitergeleitet werden?
  if item_container.item.string_1 != '':
    return HttpResponseRedirect(item_container.item.string_1)

  app_name = 'edufolder'
  width = '180px'
  news_item_container, \
  items, \
  sections, \
  lrtypen, \
  d_lrtypen, \
  lr_typen = get_folder_content(item_container)
  # aktuellesten Beitrag auswerten
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(news_item_container, items, sections, width, lrtypen, d_lrtypen, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
             get_user_support(item_container, request.user, news_item_container), last_modified=last_modified)
  # --- Anzeige erfolgt neben den Lernarchiven
  vars['image_url'] = ''
  vars['width'] = width
  if item_container.get_parent().item.app.name == 'dmsEduFolder' and \
    item_container.container.path.find(CURRICULUM_DOMAIN) < 0:
    fortbildung = get_fortbildung_slot()
  else:
    fortbildung = ''
  vars['slot_right_info'] += get_redirect_slot() + fortbildung + get_info_slot()
  return render_to_response ( 'app/base_folderish.html', vars )
