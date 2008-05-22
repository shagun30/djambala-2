# -*- coding: utf-8 -*-
"""
/dms/mediasurvey/views_show.py

.. zeigt den Inhalt eines Medien-Fragebogens (zum Aendern) an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.04.2007  Beginn der Arbeit
0.02  18.04.2007  Weiterfuehrung
0.03  19.04.2007  DynamiSierung der Formulare
0.04  23.04.2007  Speichern der Daten
0.05  07.05.2007  Sprachliche Korrekturen
0.06  20.02.2008  int_interaktion -> interaktion
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
def mediasurvey_show(request,item_container):
  """ zeigt den Medienfragenbogen zum Aendern an """
  n_faecher = get_mediasurvey_gruppe_form_count('fach')
  n_berufsfelder = get_mediasurvey_gruppe_form_count('berufsfeld')
  n_landeslizenzen = get_mediasurvey_gruppe_form_count('landeslizenz')
  schwerpunkt_opts = []
  for n in xrange(6):
    opt = 'opt_schwerpunkt_%02i' % n
    schwerpunkt_opts.append(opt)

  # -----------------------------------------------------
  #@transaction.commit_manually
  def save_values(org_id, new):
    """ speichert die Daten """

    def save_checkbox(org_id, checkbox_name, new, opt_null):
      """ speichert die Werte der Checkbox-Formularelemente """
      if new.has_key(checkbox_name):
        name = new[checkbox_name]
        names = new[checkbox_name]
        if type(names) == types.UnicodeType:
          names = [names]
        for name in names:
          item = get_mediasurvey_gruppe_form_item(name)
          my_checkbox = DmsMediaSurvey_items()
          my_checkbox.org_id = org_id
          my_checkbox.gruppe_form = item
          my_checkbox.option = opt_null
          my_checkbox.multi = False
          my_checkbox.save()

    def save_multi_checkbox(org_id, checkbox_name, new, opt_null):
      """ speichert die Werte der Checkbox-Formularelemente """
      if new.has_key(checkbox_name):
        group = get_mediasurvey_gruppe_form_item(checkbox_name)
        names = new[checkbox_name]
        if type(names) == types.UnicodeType:
          names = [names]
        for name in names:
          option = get_mediasurvey_option_item(name)
          my_checkbox = DmsMediaSurvey_items()
          my_checkbox.org_id = org_id
          my_checkbox.gruppe_form = group
          my_checkbox.option = option
          my_checkbox.multi = True
          my_checkbox.save()

    def save_radiobuttons(org_id, radiobutton_name, n_max, new, default):
      """ speichert den jeweiligen Wert des Radiobuttons """
      for n in xrange(n_max):
        name = radiobutton_name + '_%02i' % n
        if new[name] != default:
          item = get_mediasurvey_gruppe_form_item(name)
          option = get_mediasurvey_option_item(new[name])
          my_checkbox = DmsMediaSurvey_items()
          my_checkbox.org_id = org_id
          my_checkbox.gruppe_form = item
          my_checkbox.option = option
          my_checkbox.save()

    items = get_mediasurvey_by_org_id(org_id)
    if len(items) > 0:
      this_survey = items[0]
    else:
      this_survey = DmsMediaSurvey()
    DmsMediaSurvey.save_values(this_survey, org_id, new)
    # --- alle Checkbox und Radiobutton Werte loeschen
    items = get_mediasurvey_items_by_org_id(org_id)
    items.delete()
    # --- Checkboxen auswerten
    opt_null = get_mediasurvey_option_item('opt_null')
    save_checkbox(org_id, 'nutzung_raum_com', new, opt_null)
    save_checkbox(org_id, 'peripherie', new, opt_null)
    save_checkbox(org_id, 'software', new, opt_null)
    save_checkbox(org_id, 'lernplattform', new, opt_null)
    save_checkbox(org_id, 'netz_bs', new, opt_null)
    save_checkbox(org_id, 'internet_art', new, opt_null)
    save_checkbox(org_id, 'unterstuetzung', new, opt_null)
    save_checkbox(org_id, 'fortbildung', new, opt_null)
    save_checkbox(org_id, 'fortbildung_k', new, opt_null)
    save_checkbox(org_id, 'interaktion', new, opt_null)
    # --- Radiobuttons auswerten
    save_radiobuttons(org_id, 'com_einsatz', n_faecher, new, 'opt_einsatz_03')
    save_radiobuttons(org_id, 'com_einsatz_bf', n_berufsfelder, new, 'opt_einsatz_03')
    save_radiobuttons(org_id, 'int_einsatz', n_faecher, new, 'opt_einsatz_03')
    save_radiobuttons(org_id, 'int_einsatz_bf', n_berufsfelder, new, 'opt_einsatz_03')
    for i in xrange(n_faecher):
      name = 'einsatz_%02i' % i
      save_multi_checkbox(org_id, name, new, opt_null)
    for i in xrange(n_berufsfelder):
      name = 'einsatz_bf_%02i' % i
      save_multi_checkbox(org_id, name, new, opt_null)
    save_radiobuttons(org_id, 'landeslizenz', n_landeslizenzen, new, 'opt_landeslizenz_03')
    #transaction.commit()

  # -----------------------------------------------------
  def get_var_list(var_name, n_count):
    """ baut eine Liste mit Variablennamen zusammen """
    var_list = []
    for n in xrange(n_count):
      var_list.append(var_name + '_%02i' % n)
    return var_list

  # -----------------------------------------------------
  def get_var_checkbox_list(var_name, n_count, opts):
    """ baut eine Liste mit Variablennamen zusammen """
    var_list = []
    for n in xrange(n_count):
      var_list.append(var_name + '_%02i' % n)
    return var_list

  # -----------------------------------------------------
  def do_data_init(org_id):
    """ InitialiSierung der Daten """

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
    # --- Gibt es schon Daten dieser Schule?
    items = get_mediasurvey_by_org_id(org_id)
    if len(items) > 0:
      item = items[0]
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

  # -----------------------------------------------------
  def get_gruppe_form_list(gruppe):
    """ """
    items = get_mediasurvey_gruppe_form(gruppe)
    ret = []
    for item in items:
      ret.append( (item.form, item.title) )
    return ret

  # -----------------------------------------------------
  def get_option_list(gruppe):
    """ """
    items = get_mediasurvey_option(gruppe)
    ret = []
    for item in items:
      ret.append( (item.option, item.title) )
    return ret

  # -----------------------------------------------------
  def get_gruppe_items(gruppe):
    """ """
    return get_mediasurvey_gruppe_form(gruppe)

  # -----------------------------------------------------
  def get_ja_nein_choices(id=1):
    """ """
    ret = []
    ret.append( (1, 'ja') )
    ret.append( (0, 'nein') )
    return ret
  # -----------------------------------------------------
  def get_nutzung_choices():
    ret = []
    for i in xrange(5):
      ret.append( (i*25, smart_unicode(i*25)+ '%' ) )
    return ret

  # -----------------------------------------------------
  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """

    def __init__(self, *args, **kwargs):
      
      def array_init(item, name, items, default):
        """ """
        n = 0
        item['rows'] = []
        for i in items:
          item['rows'].append(i.title)
          v = name % n
          self.fields[v] = forms.ChoiceField(choices=get_option_list(default),
                                widget=forms.RadioSelect() )
          n += 1
        return n

      def checkbox_array_init(item, name, items, option_list_name):
        """ """
        g = get_option_list(option_list_name)
        n = 0
        item['rows'] = []
        for i in items:
          item['rows'].append(i.title)
          v = name % n
          self.fields[v] = forms.MultipleChoiceField(required=False, 
                                  choices=g, widget=forms.CheckboxSelectMultiple() )
          n += 1
        return n

      super(DmsItemForm, self).__init__(*args, **kwargs)
      faecher = get_gruppe_items('fach')
      berufsfelder = get_gruppe_items('berufsfeld')
      landeslizenzen = get_gruppe_items('landeslizenz')
      # 4.1 Computereinsatz: Liste der Faecher
      self.n_com_einsatz = array_init(com_einsatz, 'com_einsatz_%02i', faecher, 'opt_einsatz')
      self.n_com_einsatz_bf = array_init(com_einsatz_bf, 'com_einsatz_bf_%02i',
                                         berufsfelder, 'opt_einsatz')
      # 4.2 Interneteinsatz: Liste der Faecher
      self.n_int_einsatz = array_init(int_einsatz, 'int_einsatz_%02i', faecher, 'opt_einsatz')
      self.n_int_einsatz_bf = array_init(int_einsatz_bf, 'int_einsatz_bf_%02i',
                                         berufsfelder, 'opt_einsatz')
      # 4.4 Einsatzschwerpunkte: Liste der Faecher
      self.n_einsatz = checkbox_array_init(einsatz, 'einsatz_%02i', 
                                           faecher, 'opt_schwerpunkt')
      self.n_einsatz_bf = checkbox_array_init(einsatz_bf, 'einsatz_bf_%02i', 
                                              berufsfelder, 'opt_schwerpunkt')
      # 4.5 Landeslizenzen
      self.n_landeslizenz = array_init(landeslizenz, 'landeslizenz_%02i', 
                                       landeslizenzen, 'opt_landeslizenz')

    # -------------------------------------------------------------------
    #org_id          = forms.IntegerField(widget=forms.HiddenInput )
    # -------------------------------------------------------------------
    # 1 eigene Computer
    eigene_com      = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    # 1.1 Raeume insgesamt
    raeume_gesamt   = forms.IntegerField(min_value=1, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    nutzung_sch_com = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    nutzung_raum_com= forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('nutzung_raum_com'),
                        widget=forms.CheckboxSelectMultiple() )
    mit_com_pcraum   = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    mit_com_fachraum = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    ohne_com_pcraum  = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    ohne_com_fachraum= forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    anz_com_pcraum   = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    anz_com_fachraum = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    # 1.2 Hardware
    typ_1            = forms.IntegerField(min_value=0, max_value=1000,
                            widget=forms.TextInput(attrs={'size':5}) )
    typ_1_mobil      = forms.IntegerField(min_value=0, max_value=1000,
                            widget=forms.TextInput(attrs={'size':5}) )
    typ_2            = forms.IntegerField(min_value=0, max_value=1000,
                            widget=forms.TextInput(attrs={'size':5}) )
    typ_2_mobil      = forms.IntegerField(min_value=0, max_value=1000,
                            widget=forms.TextInput(attrs={'size':5}) )
    notebook         = forms.IntegerField(min_value=0, max_value=1000,
                            widget=forms.TextInput(attrs={'size':5}) )
    notebook_klasse  = forms.IntegerField(min_value=0, max_value=100,
                            widget=forms.TextInput(attrs={'size':5}) )
    # 1.3 Peripherie
    peripherie       = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('peripherie'),
                        widget=forms.CheckboxSelectMultiple() )
    # 1.4 Software
    software         = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('software'),
                        widget=forms.CheckboxSelectMultiple() )
    # 1.5 Lernplattform
    lernplattform    = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('lernplattform'),
                        widget=forms.CheckboxSelectMultiple() )
    eigene_plattform = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    # -------------------------------------------------------------------
    # 2 Vernetzung
    netz             = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    netz_bs          = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('netz_bs'),
                        widget=forms.CheckboxSelectMultiple() )
    netz_com         = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    netz_wlan        = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    netz_raum        = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    # -------------------------------------------------------------------
    # 3 Internet
    internet         = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    internet_art     = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('internet_art'),
                        widget=forms.CheckboxSelectMultiple() )
    internet_anz     = forms.IntegerField(min_value=0, max_value=500,
                            widget=forms.TextInput(attrs={'size':5}) )
    # -------------------------------------------------------------------
    # die folgenden Formularelemente werden dynamisch erzeugt
    # 4.1 Einsatz des Computers: __init__
    # 4.2 Weiterer Softwareeinsatz
    com_beruf      = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    com_foerder    = forms.ChoiceField(choices=get_ja_nein_choices(),
                            widget=forms.RadioSelect() )
    # 4.3 Einsatz des Internets: __init__
    # 4.4 Weitere Nutzung Internet:   __init__
    int_website    = forms.CharField(required=False, max_length=120,
                    widget=forms.TextInput(attrs={'size':60}) )
    interaktion= forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('interaktion'),
                        widget=forms.CheckboxSelectMultiple() )
    # 4.5 Einsatzschwerpunkte:   __init__
    # 4.6 Landeslizenzen:        __init__
    # 4.7 Unterstuetzungssysteme
    unterstuetzung  = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('unterstuetzung'),
                        widget=forms.CheckboxSelectMultiple() )
    # 4.8 Fortbildung
    fortbildung     = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('fortbildung'),
                        widget=forms.CheckboxSelectMultiple() )
    fortbildung_k   = forms.MultipleChoiceField(required=False, 
                        choices=get_gruppe_form_list('fortbildung_k'),
                        widget=forms.CheckboxSelectMultiple() )
    # 4.9 Nutzung
    nutzung         = forms.ChoiceField(choices=get_nutzung_choices(),
                            widget=forms.RadioSelect() )

  org_id = get_org_id(request.user.username)
  app_name = 'mediasurvey'
  if request.method == 'POST':
    data = request.POST.copy()
  else:
    data = do_data_init(org_id)
  f = DmsItemForm(data)

  max_cols = 4
  tab_cluster = {}
  # 1.1 Raeume insgesamt
  tab_cluster['raeume_gesamt'] = (  raeume_gesamt, [ 'raeume_gesamt' ] )
  tab_cluster['raeume_com'] = (  raeume_com,
                                 [ 'mit_com_pcraum', 'ohne_com_pcraum', 'anz_com_pcraum',
                                   'mit_com_fachraum', 'ohne_com_fachraum', 
                                   'anz_com_fachraum' ]
                               )
  tab_cluster['nutzung_sch_com'] = (  nutzung_sch_com, [ 'nutzung_sch_com' ] )
  tab_cluster['nutzung_raum_com'] = (  nutzung_raum_com, [ 'nutzung_raum_com' ] )

  # 1.2 Hardware
  tab_cluster['typ_com'] = (  typ_com, [ 'typ_1', 'typ_1_mobil', 'typ_2', 'typ_2_mobil' ] )
  tab_cluster['notebook'] = (  notebook, [ 'notebook', 'notebook_klasse' ] )

  # 1.3 Peripherie
  tab_cluster['peripherie'] = (  peripherie, [ 'peripherie' ] )

  # 1.4 Software
  tab_cluster['software'] = (  software, [ 'software' ] )

  # 1.5 Lernplattform
  tab_cluster['lernplattform'] = (  lernplattform, [ 'lernplattform' ] )
  tab_cluster['eigene_plattform'] = (  eigene_plattform, [ 'eigene_plattform' ] )

  # 2 Vernetzung
  tab_cluster['netz'] = (  netz, [ 'netz' ] )
  tab_cluster['netz_bs'] = (  netz_bs, [ 'netz_bs' ] )
  tab_cluster['netz_com'] = (  netz_com, [ 'netz_com' ] )
  tab_cluster['netz_wlan'] = (  netz_wlan, [ 'netz_wlan' ] )
  tab_cluster['netz_raum'] = (  netz_raum, [ 'netz_raum' ] )

  # 3 Internet
  tab_cluster['internet'] = (  internet, [ 'internet' ] )
  tab_cluster['internet_art'] = (  internet_art, [ 'internet_art' ] )
  tab_cluster['internet_anz'] = (  internet_anz, [ 'internet_anz' ] )

  # 4.1 Computereinsatz
  tab_cluster['com_einsatz'] = (  com_einsatz, get_var_list('com_einsatz', n_faecher) )
  tab_cluster['com_einsatz_bf'] = ( com_einsatz_bf, 
      get_var_list('com_einsatz_bf', n_berufsfelder) )
  # 4.2 Weiterer Computereinsatz
  tab_cluster['com_beruf'] = ( com_beruf, [ 'com_beruf' ] )
  tab_cluster['com_foerder'] = ( com_foerder, [ 'com_foerder' ] )
  # 4.3 Interneteinsatz
  tab_cluster['int_einsatz'] = (  int_einsatz, get_var_list('int_einsatz', n_faecher) )
  tab_cluster['int_einsatz_bf'] = ( int_einsatz_bf, 
      get_var_list('int_einsatz_bf', n_berufsfelder) )
  # 4.4 Weiterer Interneteinsatz
  tab_cluster['int_website'] = (  int_website, [ 'int_website' ] )
  tab_cluster['interaktion'] = (  interaktion, [ 'interaktion' ] )
  # 4.5 Einsatzschwerpunkte
  tab_cluster['einsatz'] = ( einsatz,
      get_var_checkbox_list('einsatz', n_faecher, schwerpunkt_opts) )
  tab_cluster['einsatz_bf'] = ( einsatz_bf, 
      get_var_checkbox_list('einsatz_bf', n_berufsfelder, schwerpunkt_opts) )
  # 4.6 Landeslizenzen
  tab_cluster['landeslizenz'] = (  landeslizenz,
      get_var_list('landeslizenz', n_landeslizenzen) )
  # 4.7 Unterstuetzung
  tab_cluster['unterstuetzung'] = (  unterstuetzung, [ 'unterstuetzung' ] )

  # 4.8 Fortbildung
  #tab_cluster['fortbildung'] = (  fortbildung, [ 'fortbildung', 'fortbildung_k' ] )
  tab_cluster['fortbildung'] = (  fortbildung, [ 'fortbildung' ] )
  tab_cluster['fortbildung_k'] = (  fortbildung_k, [ 'fortbildung_k' ] )

  # 4.9 Nutzung
  tab_cluster['nutzung'] = (  nutzung, [ 'nutzung' ] )

  tabs = [
          ( 'tab_1'   , [ 'eigene_com', ] ),
          ( 'tab_1_1' , [ 'raeume_gesamt', 'raeume_com', 'nutzung_sch_com',
                          'nutzung_raum_com' ] ),
          ( 'tab_1_2' , [ 'typ_com', 'notebook' ] ),
          ( 'tab_1_3' , [ 'peripherie' ] ),
          ( 'tab_1_4' , [ 'software' ] ),
          ( 'tab_1_5' , [ 'lernplattform', 'eigene_plattform' ] ),
          ( 'tab_2'   , [ 'netz', 'netz_bs', 'netz_com', 'netz_wlan', 'netz_raum' ] ),
          ( 'tab_3'   , [ 'internet', 'internet_art', 'internet_anz' ] ),
          ( 'tab_4_1' , [ 'com_einsatz', 'com_einsatz_bf' ] ),
          ( 'tab_4_2' , [ 'com_beruf', 'com_foerder' ] ),
          ( 'tab_4_3' , [ 'int_einsatz', 'int_einsatz_bf' ] ),
          ( 'tab_4_4' , [ 'int_website', 'interaktion', ] ),
          ( 'tab_4_5' , [ 'einsatz', 'einsatz_bf' ] ),
          ( 'tab_4_6' , [ 'landeslizenz' ] ),
          ( 'tab_4_7' , [ 'unterstuetzung' ] ),
          ( 'tab_4_8' , [ 'fortbildung', 'fortbildung_k' ] ),
          ( 'tab_4_9' , [ 'nutzung', ] ),
        ]

  if request.method == 'POST' and not f.errors :
    save_values(org_id, f.cleaned_data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  #elif org_id < 1000 or re.search('s_\d{4}', request.user.username) == None:
  #  return show_error(request, item_container, _(u'Nur für Schulen'), 
  #             _(u'Dieser Fragebogen darf nur von Schulen ausgefüllt werden: ' + \
  #               'Zugangsname = <tt>s_1234</tt>, wobei 1234 für die ' + \
  #               'Dienststellennummer steht.'))
  else :
    content = get_tabbed_form(tabs, help_form, app_name, f, True, tab_cluster, False, max_cols)
    content = content.replace('&amp;', '&')
    dont = {}
    user_perms = UserEditPerms(request.user.username,request.path)
    my_title = _(u'Inhalte des Medienfragebogens speichern bzw. zwischenspeichern')
    this_title = item_container.item.title
    if item_container.item.sub_title != '':
      this_title += ' / ' + item_container.item.sub_title
    vars = { 'content_div_style': 'frame-main-manage',
             'site'             : item_container.container.site,
             'action'           : get_item_actions(request, user_perms, 
                                                   item_container, app_name,
                                                   item_container.item.has_comments, dont),
             'breadcrumb'       : get_breadcrumb(item_container),
             'content'          : content,
             'title'            : my_title,
             'sub_title'        : this_title,
             'text'             : item_container.item.text,
             'is_wide'          : True,
             'errors'           : f.errors,
             'footer_email'     : get_footer_email(item_container),
             'last_modified'    : item_container.get_last_modified(),
             'submit'           : my_title,
             'authenticated'    : True,
             'base_site_url'    : get_base_site_url(),
             'url_path'         : get_site_url(item_container.get_parent(), 'index.html'),
             'no_top_main_navigation': True
            }
    return render_to_response ( 'app/base_edit.html', vars )
