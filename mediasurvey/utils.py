# -*- coding: utf-8 -*-
"""
/dms/mediasurvey/utils.py

.. bietet Hilfsfunktionen fuer Medien-Fragebogen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.04.2008  Beginn der Arbeit
"""

import string, re, types

from django.utils.encoding  import smart_unicode
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.queries        import get_org_id
from dms.queries        import get_mediasurvey_gruppe_form
from dms.queries        import get_mediasurvey_by_org_id
from dms.queries        import get_mediasurvey_items_by_org_id
from dms.queries        import get_mediasurvey_gruppe_form_count
from dms.queries        import get_mediasurvey_option
from dms.queries        import get_base_site_url
from dms.queries        import get_site_url
from dms.queries        import get_mediasurvey_option_item
from dms.queries        import get_mediasurvey_gruppe_form_item

from dms.utils          import get_navigation_left
from dms.utils          import show_more
from dms.utils          import info_slot_to_header
from dms.utils          import get_tabbed_form
from dms.utils          import get_parent_section_choices
from dms.utils          import get_breadcrumb
from dms.utils          import get_prev_next_line
from dms.utils          import get_footer_email
from dms.utils          import get_item_actions
from dms.utils_form     import get_folderish_vars_show

from dms.views_error    import show_error

from dms.mediasurvey.models      import DmsMediaSurvey
from dms.mediasurvey.models      import DmsMediaSurvey_gruppe_form
from dms.mediasurvey.models      import DmsMediaSurvey_option
from dms.mediasurvey.models      import DmsMediaSurvey_items

from dms.mediasurvey.help_form   import help_form
# --- Beschreibung der Formulare
# 1.1 Raeume insgesamt
from dms.mediasurvey.help_form   import raeume_gesamt
from dms.mediasurvey.help_form   import raeume_com
from dms.mediasurvey.help_form   import nutzung_sch_com
from dms.mediasurvey.help_form   import nutzung_raum_com
# 1.2 Hardware
from dms.mediasurvey.help_form   import typ_com
from dms.mediasurvey.help_form   import notebook
# 1.3 Peripherie
from dms.mediasurvey.help_form   import peripherie
# 1.4 Software
from dms.mediasurvey.help_form   import software
# 1.5 Lernplattform
from dms.mediasurvey.help_form   import lernplattform
from dms.mediasurvey.help_form   import eigene_plattform
# 2 Vernetzung
from dms.mediasurvey.help_form   import netz
from dms.mediasurvey.help_form   import netz_bs
from dms.mediasurvey.help_form   import netz_com
from dms.mediasurvey.help_form   import netz_wlan
from dms.mediasurvey.help_form   import netz_raum
# 3 Internet
from dms.mediasurvey.help_form   import internet
from dms.mediasurvey.help_form   import internet_art
from dms.mediasurvey.help_form   import internet_anz
# 4.1 Computereinsatz
from dms.mediasurvey.help_form   import com_einsatz
from dms.mediasurvey.help_form   import com_einsatz_bf
# 4.2 Weiterer Softwareeinsatz
from dms.mediasurvey.help_form   import com_beruf
from dms.mediasurvey.help_form   import com_foerder
# 4.3 Interneteinsatz
from dms.mediasurvey.help_form   import int_einsatz
from dms.mediasurvey.help_form   import int_einsatz_bf
# 4.4 Weiterer Interneteinsatz
from dms.mediasurvey.help_form   import int_website
from dms.mediasurvey.help_form   import interaktion
# 4.5 Einsatzschwerpunkte
from dms.mediasurvey.help_form   import einsatz
from dms.mediasurvey.help_form   import einsatz_bf
# 4.6 Landeslizenzen
from dms.mediasurvey.help_form   import landeslizenz
# 4.7 Landeslizenzen
from dms.mediasurvey.help_form   import unterstuetzung
# 4.8 Fortbildung
from dms.mediasurvey.help_form   import fortbildung
from dms.mediasurvey.help_form   import fortbildung_k
# 4.9 Nutzung
from dms.mediasurvey.help_form   import nutzung

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_read')
def get_data_by_org_id(request, item_container, org_id):
  """ initialisiert die Datenstruktur """
  n_faecher = get_mediasurvey_gruppe_form_count('fach')
  n_berufsfelder = get_mediasurvey_gruppe_form_count('berufsfeld')
  n_landeslizenzen = get_mediasurvey_gruppe_form_count('landeslizenz')
  schwerpunkt_opts = []
  for n in xrange(6):
    opt = 'opt_schwerpunkt_%02i' % n
    schwerpunkt_opts.append(opt)

  def do_init_array(data_init, var_name, n_count, default):
    """ setzt die entsprechenden Defaultwerte """
    for n in xrange(n_count):
      data_init[var_name + '_%02i' % n] = default
    return data_init

  def do_checkbox_init_array(data_init, var_name, n_count, opts):
    for n in xrange(n_count):
      data_init[var_name + '_%02i' % n] = []
    return data_init

  data_init = {}
  # --- InitialiSierung der Daten
  data_init = { # 1 eigene Computer
                'eigene_com'       : 0,
                'mit_com_pcraum'   : 0, 'mit_com_fachraum' : 0,
                'ohne_com_pcraum'  : 0, 'ohne_com_fachraum': 0,
                'anz_com_pcraum'   : 0, 'anz_com_fachraum' : 0,
                'nutzung_sch_com'  : 0,
                'nutzung_raum_com' : [],
                # 1.1 Raeume insgesamt
                'raeume_gesamt'    : 0,
                # 1.2 Hardware
                'typ_1'            : 0,  'typ_1_mobil'      : 0,
                'typ_2'            : 0,  'typ_2_mobil'      : 0,
                'notebook'         : 0,  'notebook_klasse'  : 0,
                # 1.3 Peripherie
                'peripherie'       : [],
                # 1.4 Software
                'software'         : [],
                # 1.5 Lernplattform
                'lernplattform'    : [],
                # 1.5 Lernplattform
                'eigene_plattform' : 0,
                # 2 Netz
                'netz_bs'          : [],
                'netz'             : 0, 'netz_com'         : 0,
                'netz_wlan'        : 0, 'netz_raum'        : 0,
                # 3 Internet
                'internet_art'     : [],
                'internet'         : 0, 'internet_anz'     : 0,
                # 4.2
                'com_beruf'        : 0,
                'com_foerder'      : 0,
                # 4.3
                'int_website'      : 'http://',
                # 4.5 Unterstuetzung
                'unterstuetzung'   : [],
                # 4.6 Fortbildung
                'fortbildung'      : [],
                'fortbildung_k'    : [],
                # 4.7
                'nutzung'          : 0,
              }
  # 4.1 Computereinsatz
  data_init = do_init_array(data_init, 'com_einsatz', n_faecher, 'opt_einsatz_03')
  data_init = do_init_array(data_init, 'com_einsatz_bf', n_berufsfelder, 'opt_einsatz_03')
  # 4.2 Interneteinsatz
  data_init = do_init_array(data_init, 'int_einsatz', n_faecher, 'opt_einsatz_03')
  data_init = do_init_array(data_init, 'int_einsatz_bf', n_berufsfelder, 'opt_einsatz_03')
  # 4.2 ???
  # 4.3 Einsatzschwerpunkte
  data_init = do_checkbox_init_array(data_init, 'einsatz', n_faecher, schwerpunkt_opts)
  data_init = do_checkbox_init_array(data_init, 'einsatz_bf',
              n_berufsfelder, schwerpunkt_opts)
  # 4.4 Landeslizenzen
  data_init = do_init_array(data_init, 'landeslizenz', n_landeslizenzen,
                            'opt_landeslizenz_03')
  data_init['org_id'] = org_id
  data_init['hat_daten'] = False

  # --- Gibt es schon Daten dieser Schule?
  items = get_mediasurvey_by_org_id(org_id)
  if len(items) > 0:
    item = items[0]
    data_init['hat_daten'] = True
    # 1 eigene Computer
    data_init['eigene_com']       = item.eigene_com
    data_init['mit_com_pcraum']   = item.mit_com_pcraum
    data_init['mit_com_fachraum'] = item.mit_com_fachraum
    data_init['ohne_com_pcraum']  = item.ohne_com_pcraum
    data_init['ohne_com_fachraum']= item.ohne_com_fachraum
    data_init['anz_com_pcraum']   = item.anz_com_pcraum
    data_init['anz_com_fachraum'] = item.anz_com_fachraum
    data_init['nutzung_sch_com']  = item.nutzung_sch_com
    # 1.1 Raeume insgesamt
    data_init['raeume_gesamt']    = item.raeume_gesamt
    # 1.2 Hardware
    data_init['typ_1']            = item.typ_1
    data_init['typ_1_mobil']      = item.typ_1_mobil
    data_init['typ_2']            = item.typ_2
    data_init['typ_2_mobil']      = item.typ_2_mobil
    data_init['notebook']         = item.notebook
    data_init['notebook_klasse']  = item.notebook_klasse
    # 1.5 Lernplattform
    data_init['eigene_plattform'] = item.eigene_plattform
    # 2 Netz
    data_init['netz']             = item.netz
    data_init['netz_com']         = item.netz_com
    data_init['netz_wlan']        = item.netz_wlan
    data_init['netz_raum']        = item.netz_raum
    # 3 Internet
    data_init['internet']         = item.internet
    data_init['internet_anz']     = item.internet_anz
    # 4.2
    data_init['com_beruf']        = item.com_beruf
    data_init['com_foerder']      = item.com_foerder
    # 4.4
    data_init['int_website']      = item.int_website
    data_init['interaktion']      = []
    # 4.7
    data_init['nutzung']          = item.nutzung
    items = get_mediasurvey_items_by_org_id(org_id)
    for item in items:
      if item.option.option == 'opt_null':
        data_init[item.gruppe_form.gruppe.gruppe].append(item.gruppe_form.form)
      elif item.multi:
        data_init[item.gruppe_form.form].append(item.option.option)
      else:
        data_init[item.gruppe_form.form]=item.option.option
  return data_init

