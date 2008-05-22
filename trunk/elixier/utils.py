# -*- coding: utf-8 -*-
"""
/dms/elixier/utils.py

.. enthaelt Hilfefunktionen fuer den Elixier-Austausch
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.06.2007  Beginn der Arbeit
0.02  19.10.2007  Elixier-Beitraege werden ausgewertet
"""

import string
import datetime
import time

from django.db          import transaction
from django.db.models       import Q
from django.shortcuts   import render_to_response
from django.utils.encoding  import smart_unicode

from django.utils.translation import ugettext as _

from dms.roles          import require_permission

from dms.settings       import EDUFOLDER_BASE_PATH

from dms.models         import DmsItemContainer
from dms.utils          import show_link
from dms.utils          import encode_email
from dms.utils_form     import get_item_vars_show

from dms.queries        import get_item_container_by_path
#from dms.queries        import get_folder_filtered_items
from dms.queries        import get_lernrestyp_by_name
from dms.queries        import get_medienformat_by_name
from dms.queries        import set_extra_data
from dms.queries        import get_app
from dms.queries        import get_null_license
from dms.queries        import get_edu_fach_id_by_name
from dms.queries        import get_schulart_id_by_name
from dms.queries        import get_schulstufe_id_by_name
from dms.queries        import get_edu_sprache_id
from dms.queries        import get_zielgruppe_id_by_name
from dms.queries        import get_lernrestyp_by_name
from dms.queries        import save_item_values

from dms.mail               import send_control_email
from dms.edufolder.utils    import get_org_image_url
from dms.edufolder.models   import DmsEduItem
from dms.edulinkitem.utils  import save_schlagworte

from dms.elixier.queries  import set_elixier_item_status

from dms.encode_decode  import encode_html
from dms.encode_decode  import decode_html

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_folder_filtered_items(item_container, alpha_mode=False, app_types=[]):
  """ liefert die Liste der entsprechenden item_container zurueck """
  myQ = None
  for app_name in app_types:
    if myQ == None:
      myQ = Q(item__app__name=app_name)
    else:
      myQ = myQ | Q(item__app__name=app_name)
  items = DmsItemContainer.objects.select_related().\
                            filter(parent_item_id=item_container.item.id). \
                            filter(is_deleted=False). \
                            exclude(item__app__name='dmsUserFolder'). \
                            filter(myQ). \
                            order_by('item__title')
  return items

# -----------------------------------------------------
@require_permission('perm_manage')
def views_select_dest(request, item_container, op):
  """ waehlt Zielordner aus """

  def get_edufolders(dest_folder):
    """ liefert Uebersicht der Lernarchive """

    def get_link(base_folder, folder, title=''):
      """ baut den Verweis zusammen """
      if folder == '':
        folder_name = _(u'oberste Ebene')
      else:
        folder_name = folder
      if title == '':
        title = folder_name
      path = '%s%s/' % (base_folder, folder)
      radio = ''
      radio += '<input type="radio" name="folder_new" value="%s" />\n' % path
      radio += '<a href="?elixier_op=select_dest&select_folder=%s">%s</a>'
      radio = radio % (path, title )
      return radio

    ret = ''
    # --- letztes / entfernen
    folders = string.splitfields(dest_folder[:-1], '/')
    n_current = 1
    base_folder = ''
    for folder in folders:
      ret += '%s %s<br />\n' % ('&nbsp;.&nbsp;&nbsp;'*n_current, get_link(base_folder, folder) )
      base_folder += folder + '/'
      n_current += 1
    edu_item_container = get_item_container_by_path(EDUFOLDER_BASE_PATH+dest_folder)
    folders = get_folder_filtered_items(edu_item_container, app_types=['dmsEduFolder'])
    for folder in folders:
      ret += '%s &nbsp;&nbsp;&nbsp; %s<br />\n' % \
             ('&nbsp;.&nbsp;&nbsp;'*n_current, get_link(base_folder, folder.item.name, folder.item.title))
    return ret

  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['content_div_style'] = 'frame-util-images'
  vars['no_breadcrumb'] = True
  if request.GET.has_key('select_folder'):
    select_folder = request.GET['select_folder']
  else:
    if request.COOKIES.has_key('elixier_dest_folder'):
      select_folder = request.COOKIES['elixier_dest_folder']
    else:
      select_folder = '/'
      request.COOKIES['elixier_dest_folder'] = select_folder
  vars['edufolders'] = get_edufolders(select_folder)
  return render_to_response ( 'app/elixier/select_destination.html', vars )

# -----------------------------------------------------
@require_permission('perm_add')
#@ transaction.commit_manually
def do_check(request, item, item_org, new_status, dest_folder):
  """ """
  set_elixier_item_status(item, new_status)
  if new_status == 1:
    edu_item_container = get_item_container_by_path(EDUFOLDER_BASE_PATH+dest_folder)
    new = {}
    community_id = 0
    schulverbund_id = 0
    new['is_exchangeable'] = False
    new['string_1']  = decode_html(item_org.quelle_id)
    new['string_2']  = item_org.url_datensatz
    new['integer_1'] = community_id
    new['integer_2'] = schulverbund_id
    # --- eine Normierung ist dringend erforderlich
    lernrestypen = item_org.lernressourcentyp.replace(',', '|').replace(';', '|')
    lernrestypen = string.splitfields(lernrestypen, '|')
    found = False
    for lernrestyp in lernrestypen:
      lernrestyp = lernrestyp.strip()
      if lernrestyp != '':
        lernrestyp = get_lernrestyp_by_name(lernrestyp)
        if lernrestyp != -1:
          new['integer_3'] = lernrestyp.id
          found = True
    if not found:
      new['integer_3'] = get_lernrestyp_by_name(_(u'Arbeitsmaterial')).id
    new['integer_4'] = get_medienformat_by_name(_(u'Online-Ressource')).id
    new['integer_5'] = 1  # zertifikat_id
    schlagworte_raw = item_org.schlagwort.replace(';', '\n').replace(',', '\n')
    schlagworte = ''
    for s in string.splitfields(schlagworte_raw, '\n'):
      s = s.strip()
      if s != '':
        schlagworte += s + '\n'
    new['extra'] = encode_html(set_extra_data(schlagwort_org=schlagworte))
    new['schlagwort'] = schlagworte
    dsatz = item_org.url_datensatz
    image_url, image_url_url, image_extern = get_org_image_url(item_org.url_datensatz)
    if item_org.bild_url == '' and image_url != '':
      new['image_url'] = image_url
      new['image_url_url'] = image_url_url
      new['image_extern'] = image_extern
    elif item_org.bild_url != '':
      new['image_url'] = item_org.bild_url
      new['image_url_url'] = ''
      new['image_extern'] = True
    else:
      new['image_url'] = item_org.quelle_logo_url
      new['image_url_url'] = item_org.quelle_homepage_url
      new['image_extern'] = True

    #new['app'] = get_app('dmsEduLinkItem')
    #new['owner'] = request.user
    new['license'] = 1  #get_null_license()
    now = smart_unicode(time.time())
    name = 'edu_' + now[:string.find(now, '.')] + '.html'
    #new['name'] = 'edu_' + now[:string.find(now, '.')] + '.html'
    new['title'] = decode_html(item_org.titel)
    new['sub_title'] = ''
    new['text'] = decode_html(item_org.beschreibung)
    # Problem: Originaleinsteller
    new['text_more'] = ''
    url = item_org.url_ressource.strip()
    if not url.startswith('http://'):
      url = item_org.url_datensatz.strip()
    new['url_more'] = url
    new['url_more_extern'] = True
    new['is_wide'] = True
    new['is_important'] = False
    new['info_slot_right'] = ''
    new['has_user_support'] = False
    new['has_comments'] = edu_item_container.item.has_comments
    new['is_moderated'] = edu_item_container.item.is_moderated
    item_container_new = save_item_values(request.user, 'dmsEduLinkItem', name, new,
                                          edu_item_container, True, False)
    new['autor'] = decode_html(item_org.autor)
    new['herausgeber'] = decode_html(item_org.herausgeber)
    new['anbieter_herkunft'] = decode_html(item_org.anbieter_herkunft)
    new['isbn'] = decode_html(item_org.isbn)
    new['preis'] = decode_html(item_org.preis)
    new['titel_lang'] = decode_html(item_org.titel_lang)
    new['beschreibung_lang'] = encode_html(decode_html(item_org.beschreibung_lang))
    if item_org.einsteller != '':
      email = encode_email(item_org.einsteller_email, item_org.einsteller)
      new['beschreibung_lang'] += '<p>%s: %s</p>\n' % (_(u'Einsteller/in: '), email)
    new['publikations_datum'] = item_org.publikationsdatum
    new['standards_kmk'] = encode_html(decode_html(item_org.kmk_standards))
    new['standards_weitere'] = encode_html(decode_html(item_org.weitere_kompetenzen))
    new['techn_voraus'] = encode_html(decode_html(item_org.techn_voraussetzungen))
    new['lernziel'] = encode_html(decode_html(item_org.lernziel))
    new['lernzeit'] = encode_html(decode_html(item_org.lernzeit))
    new['methodik'] = encode_html(decode_html(item_org.methodik))
    new['lehrplan'] = encode_html(decode_html(item_org.lehrplanbezug))
    new['rechte'] = encode_html(decode_html(item_org.rechte))
    edu_item = DmsEduItem.save_values(DmsEduItem(), item_container_new, new, True)
    faecher = item_org.fach_sachgebiet.replace(',', '|').replace(';', '|')
    faecher = string.splitfields(faecher, '|')
    for fach_sachgebiet in faecher:
      fach_sachgebiet = fach_sachgebiet.strip()
      if fach_sachgebiet != '':
        fach_id = get_edu_fach_id_by_name(fach_sachgebiet)
        if fach_id != -1:
          edu_item.fach_sachgebiet.add(fach_id)
    schularten = item_org.schulform.replace(',', '|').replace(';', '|')
    schularten = string.splitfields(schularten, '|')
    found = False
    for schulart in schularten:
      schulart = schulart.strip()
      if schulart != '':
        schulart_id = get_schulart_id_by_name(schulart)
        if schulart_id != -1:
          edu_item.schulart.add(schulart_id)
          found = True
    if not found:
      for schulart_id in [1, 2, 3]:
        edu_item.schulart.add(schulart_id)
    schulstufen = item_org.bildungsebene.replace(',', '|').replace(';', '|')
    schulstufen = string.splitfields(schulstufen, '|')
    for schulstufe in schulstufen:
      schulstufe = schulstufe.strip()
      if schulstufe != '':
        schulstufe_id = get_schulstufe_id_by_name(schulstufe)
        if schulstufe_id != -1:
          edu_item.schulstufe.add(schulstufe_id)
    sprachen = item_org.sprache.replace(',', '|').replace(';', '|')
    sprachen = string.splitfields(sprachen, '|')
    found = False
    for sprache in sprachen:
      sprache = sprache.strip()
      if sprache != '':
        sprache_id = get_edu_sprache_id(sprache)
        if sprache_id != -1:
          edu_item.sprache.add(sprache_id)
    if not found:
      sprache_id = get_edu_sprache_id(_(u'de'))
      edu_item.sprache.add(sprache_id)
    zielgruppen = item_org.zielgruppe.replace(',', '|').replace(';', '|')
    zielgruppen = string.splitfields(zielgruppen, '|')
    found = False
    for zielgruppe in zielgruppen:
      zielgruppe = zielgruppe.strip()
      if zielgruppe != '':
        zielgruppe_id = get_zielgruppe_id_by_name(sprache)
        if zielgruppe_id != -1:
          edu_item.zielgruppe.add(zielgruppe_id)
          found = True
    if not found:
      for zielgruppe_id in [3, 4, 5]:
        edu_item.zielgruppe.add(zielgruppe_id)
    save_schlagworte(edu_item, new)
    if item_org.verfallsdatum:
      v = item_org.verfallsdatum
      item_container_new.visible_end = item_org.verfallsdatum
    item_container_new.save()
    item_container_new.last_modified = item_org.letzte_aenderung
    item_container_new.save()
    send_control_email(item_container_new)

    """
    # autor_email entfaellt
    # id_local hat nur interne Bedeutung
    # quelle_pfad hat nur interne Bedeutung
    #systematikpfad entfaellt - wird bei der Angabe des Zielordners ausgewertet
    # zertifizierung entfaellt - muss haendisch ausgewertet werden
    #zeitstempel enfaellt
    """
  #transaction.commit()
