#!/usr/bin/python
#-*-coding: utf-8 -*-
#
#
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.10.2007  Beginn der Arbeit
"""

import string
import re
import MySQLdb
import time
import codecs

from dms.settings import *
from dms.models   import DmsItemContainer
from dms.queries  import get_eduitem
from dms.queries  import get_schlagwort_by_stem
from dms.queries  import get_linked_item_containers
from dms.queries  import get_medienformat_by_id
from dms.queries  import get_lernrestyp_by_id
from dms.edufileitem.utils  import get_edu_file_url

XML_FILE = '/srv/www/htdocs/elixier/elixier.xml'

"""
from dms.queries            import get_edu_faecher
from dms.queries            import get_item_by_url_more
from dms.elixier.queries    import get_elixier_data
from dms.elixier.queries    import get_elixier_items
from dms.elixier.queries    import get_elixier_item_status
from dms.elixier.queries    import set_elixier_item_status
from dms.elixier.queries    import set_elixier_item_fach_sachgebiet
from dms.elixier.queries    import append_elixier_item_status
from dms.elixier.queries    import get_elixier_org_by_id_local

from dms.encode_decode import decode_html
"""

def get_copyright():
  """ Copyright-Vermerk """
  return """		<!-- Alle Rechte am Datensatz liegen beim Bildungsserver Hessen.
		Alle in dieser Datei enthaltenen Metadaten sind urheberrechtlich
		geschuetzt und duerfen ausschliesslich im Rahmen der Vereinbarungen
		zum Datenaustausch zwischen den deutschen Bildungsservern verwendet
		werden. -->
"""

def get_item_containers(app_name, THIS_ORG):
  """ liefert die zu app_name und THIS_ORG passenden Einträge der der Datenbank
      dabei werden keine Einblendungen beruecksichtigt
      ausgeschlossen werden andere Lernorte, Institutionen, Lehrplaene, Hauptdokument
  """
  return DmsItemContainer.objects.filter(item__app__name=app_name)\
                                 .filter(item__string_1=THIS_ORG)\
                                 .filter(is_data_object=True)\
                                 .exclude(item__integer_3__in=[6, 13, 14, 24])

def write_xml(f, name, info, html_code=False):
  """ """
  if (html_code and info != '') or info.find('&') >= 0:
    info = '<![CDATA[' + info + ']]>'
  s = '\t\t<%s>%s</%s>\n' % (name, info, name)
  f.write(s)

def write_mult_xml(f, tags, tag, objs):
  """ """
  #s = '\t\t<%s>\n' % tags
  #f.write(s)
  for obj in objs:
    if obj.strip() != '':
      obj = obj.strip()
      if obj.find('&') >= 0:
        obj = '<![CDATA[' + obj + ']]>'
      s = '\t\t\t<%s>%s</%s>\n' % (tag, obj, tag)
      f.write(s)
  #s = '\t\t</%s>\n' % tags
  #f.write(s)

def get_item_list(query_set):
  ret = []
  for q in query_set.all():
    ret.append(q.name)
  return ret

def get_schlagworte_sorted(schlagworte):
  """ uebersetzt die gestemmten Schlagwoerter in die ursruenglichen Schlagwoerter """
  items = []
  for schlagwort in schlagworte.all():
    items.append(get_schlagwort_by_stem(schlagwort))
  items.sort()
  return items

def do_main_export(f, THIS_ORG):
  """ Hauptprogramm: schreibt die Daten von THIS_ORG heraus """
  apps = ['dmsEduTextItem', 'dmsEduFileItem', 'dmsMediaItem', 'dmsEduWebquestItem', 'dmsEduLinkItem']
  #apps = ['dmsEduTextItem', 'dmsEduFileItem', 'dmsMediaItem', 'dmsEduWebquestItem']
  for app in apps:
    ics = get_item_containers(app, THIS_ORG)
    copyright = get_copyright()
    count = 0
    for ic in ics:
      if ic.container.path.find('/lehrplaene/') < 0:
        count += 1
        data = get_eduitem(ic.item)
        f.write('\t<datensatz>\n')
        f.write(copyright)
        write_xml(f, 'id_local', THIS_ORG + ':' + str(ic.item.id))
        write_xml(f, 'titel_lang', data.titel_lang, True)
        write_xml(f, 'titel', ic.item.title, True)
        write_mult_xml(f, 'sprachen', 'sprache', get_item_list(data.sprache))
        write_xml(f, 'beschreibung', ic.item.text, True)
        write_xml(f, 'beschreibung_lang', ic.item.text_more, True)
        write_xml(f, 'bild_url', ic.item.image_url)
        schlagworte_sorted = get_schlagworte_sorted(data.schlagwort)
        write_mult_xml(f, 'schlagworte', 'schlagwort', schlagworte_sorted)
        write_xml(f, 'autor', data.autor)
        write_xml(f, 'autor_email', '')
        write_xml(f, 'herausgeber', data.herausgeber)
        write_xml(f, 'anbieter_herkunft', data.anbieter_herkunft)
        write_xml(f, 'einsteller', ic.item.owner.username)
        write_xml(f, 'einsteller_email', ic.item.owner.email)
        write_xml(f, 'letzte_aenderung', ic.last_modified.strftime('%Y%m%d%H%M%S'))
        write_xml(f, 'publikationsdatum', data.publikations_datum)
        write_xml(f, 'verfallsdatum', ic.visible_end.strftime('%Y-%m-%d'))
        write_mult_xml(f, 'fach_sachgebiete', 'fach_sachgebiet', get_item_list(data.fach_sachgebiet))
        path = ic.container.path
        folders = string.splitfields(path, '/')
        systematikpfade = []
        for folder in folders:
          if folder not in ['unterricht', 'lernarchiv']:
            systematikpfade.append(folder.strip())
        write_mult_xml(f, 'systematikpfade', 'systematikpfad', systematikpfade)
        write_xml(f, 'isbn', data.isbn)
        write_mult_xml(f, 'bildungsebenen', 'bildungsebene', get_item_list(data.schulstufe))
        write_mult_xml(f, 'schulformen', 'schulform', get_item_list(data.schulart))
        write_xml(f, 'lehrplanbezug', data.lehrplan, True)
        write_xml(f, 'medienformat', get_medienformat_by_id(ic.item.integer_4).name)
        if app == 'dmsEduLinkItem':
          url = ic.item.url_more
        elif app in ['dmsEduTextItem', 'dmsEduWebquestItem', 'dmsEduMediaItem', 'dmsEduGalleryItem']:
          url = ic.get_absolute_url()
        else:
          url = get_edu_file_url(ic)
        write_xml(f, 'url_ressource', url, True)
        write_xml(f, 'url_datensatz', ic.get_absolute_url() + '?show_details=1')
        write_xml(f, 'techn_voraussetzungen', data.techn_voraus, True)
        write_xml(f, 'lernressourcentyp', get_lernrestyp_by_id(ic.item.integer_3).name)
        write_xml(f, 'lernziel', data.lernziel, True)
        write_xml(f, 'lernzeit', data.lernzeit)
        write_xml(f, 'methodik', data.methodik, True)
        write_mult_xml(f, 'zielgruppen', 'zielgruppe', get_item_list(data.zielgruppe))
        write_xml(f, 'preis', data.preis)
        write_xml(f, 'rechte', data.rechte, True)
        write_mult_xml(f, 'zertifizierungen', 'zertifizierung', [])
        write_xml(f, 'kmk_standards', data.standards_kmk, True)
        write_xml(f, 'weitere_kompetenzen', data.standards_weitere, True)
        write_xml(f, 'quelle_id', THIS_ORG)
        #write_xml(f, 'quelle_logo_url', 'http://portal.bildung.hessen.de/logo_thumbs/hessen.gif')
        write_xml(f, 'quelle_logo_url', 'http://download.bildung.hessen.de/unterricht/lernarchiv/logo_thumbs/elixier_he.gif')
        write_xml(f, 'quelle_homepage_url', 'http://www.bildung.hessen.de/')
        write_xml(f, 'quelle_pfad', 'Bildungsserver Hessen')
        f.write('\t</datensatz>\n')
    print app, count

# ###################################################################

f = codecs.open(XML_FILE, "wb", "utf-8")
f.write("""<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE elixier SYSTEM "http://www.bildungsserver.de/elixier/elixier.dtd"  >
""")
f.write('<elixier>\n')
do_main_export(f, 'HE')
f.write('</elixier>\n')
f.close()
