# -*- coding: utf-8 -*-
"""
/dms/hessen/schooldb/views_show.py

.. zeigt die Inhalte der Schul-Datenbank an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.02.2008  Beginn der Arbeit
0.02  13.02.2008  Anzeige der Schulen
0.03  14.02.2008  Anzeige der Schuldaten
0.04  24.04.2008  CSV-Datei des Medienfragebogens (integer_1 auf 2008 setzen !!!)
"""

from django.template.loader import get_template
from django.template    import Context
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.shortcuts   import render_to_response
from django.http        import HttpResponse
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.utils_base     import show_link
from dms.utils          import get_tabbed_form
from dms.utils          import encode_email

from dms.hessen.schooldb.queries    import get_bes_einrichtung_all
from dms.hessen.schooldb.queries    import get_rechtsstellung_all
from dms.hessen.schooldb.queries    import get_schulamt_all
from dms.hessen.schooldb.queries    import get_schultraeger_all
from dms.hessen.schooldb.queries    import get_schultyp_all
from dms.hessen.schooldb.queries    import get_sformangebot_all
from dms.hessen.schooldb.queries    import get_sprachenfolge_all
from dms.hessen.schooldb.queries    import get_voraussetzung_all
from dms.hessen.schooldb.queries    import get_schulen_by_filter
from dms.hessen.schooldb.queries    import get_schule_by_schul_nr
from dms.hessen.schooldb.queries    import get_sprachenfolge_by_stelle_id
from dms.hessen.schooldb.queries    import get_bes_einrichtung_by_stelle_id
from dms.hessen.schooldb.queries    import get_sformangebot_by_stelle_id
from dms.hessen.schooldb.queries    import get_schulbasisdaten_by_schul_nr
from dms.hessen.schooldb.queries    import get_regionschulen_by_region

from dms.hessen.schooldb.utils_media_survey   import show_media_survey_csv
from dms.hessen.schooldb.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_schul_daten(vars, schul_nr):
  """ """
  my_title = ''
  #try:
  schul_objs = get_schule_by_schul_nr(schul_nr)
  objs = []
  if len(schul_objs) >= 1:
    my_title = schul_objs[0][1].NameSchule
    for obj in schul_objs:
      data = {}
      if my_title.find(obj[0].NameStelle) == 0:
        data['schul_name'] = my_title
      else:
        data['schul_name'] = obj[0].NameStelle
      data['schul_plz'] = obj[0].PLZ
      data['schul_ort'] = obj[0].Ort
      data['schul_strasse'] = obj[0].Str_Nr
      data['schul_tel'] = obj[0].Tel1
      data['schul_fax'] = obj[0].Fax
      data['schul_email'] = encode_email(obj[0].E_Mail, obj[0].E_Mail)
      data['schul_nr'] = obj[1].Schul_Nr
      if len(schul_objs) > 1:
        if objs == []:
          data['header'] = _(u'Stammschule')
        else:
          data['header'] = _(u'Außenstandort')
      objs.append(data)
    vars['objs'] = objs
    vars['schul_typ'] = obj[1].rel_schultyp.TextKey
    vars['schul_rechtsstellung'] = obj[1].rel_rechtsstellung.TextKey
    vars['schul_nr'] = obj[1].Schul_Nr
    vars['schul_amt'] = obj[1].rel_schulamt.TextKey
    vars['schul_traeger'] = obj[1].rel_schultraeger.TextKey
    stelle_id = schul_objs[0][0].ID
    sprachen = []
    for s in get_sprachenfolge_by_stelle_id(stelle_id):
      sprachen.append(s[1].TextKey)
    vars['schul_sprfolge'] = sprachen
    sform = []
    for s in get_sformangebot_by_stelle_id(stelle_id):
      sform.append(s[1].TextKey)
    vars['schul_sformangebot'] = sform
    bes = []
    for b in get_bes_einrichtung_by_stelle_id(stelle_id):
      bes.append(b[1].TextKey)
    vars['schul_bes_einrichtung'] = bes
    vars['schul_profil'] = mark_safe(obj[2].Profil)
    vars['schul_homepage'] = mark_safe(show_link(obj[2].Homepage))
    vars['schul_homepage2'] = mark_safe(show_link(obj[2].Homepage2))
  else:
    vars['title'] = _(u'Unbekannte Schulnummer')
  #except:
  #  vars['title'] = _(u'Keine Schulnummer')
  return vars, my_title, my_title

# -----------------------------------------------------
def schooldb_show(request,item_container):
  """ zeigt Suchformular für Schul-Datenbank """

  def has_search_items(data):
    """ wurden Einträge in Formular vorgenommen? """
    has_data = False
    if data == {}:
      return has_data
    has_data = has_data or (data.has_key('schul_name') and data['schul_name']!='')
    has_data = has_data or (data.has_key('schul_ort') and data['schul_ort']!='')
    has_data = has_data or (data.has_key('schul_plz') and data['schul_plz']!='')
    has_data = has_data or (data.has_key('schul_nr') and data['schul_nr']!='')
    has_data = has_data or (data.has_key('schul_bes_einricht'))
    has_data = has_data or (data.has_key('schul_rechtsstellung'))
    has_data = has_data or (data.has_key('schul_amt'))
    has_data = has_data or (data.has_key('schul_traeger'))
    has_data = has_data or (data.has_key('schul_typ'))
    has_data = has_data or (data.has_key('schul_sformangebot'))
    has_data = has_data or (data.has_key('schul_sprache'))
    has_data = has_data or (data.has_key('region'))
    return has_data

  def get_form_list(items):
    """ """
    ret = []
    ret.append( (-1, u'---') )
    for item in items:
      ret.append( (item.CodeKey, item.TextKey) )
    return ret

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    schul_name = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':40, 'max_length':120}) )
    schul_ort = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':30, 'max_length':120}) )
    schul_plz = forms.IntegerField(required=False, min_value=10000, max_value=99999,
         widget=forms.TextInput(attrs={'size':10, 'max_length':100, }) )
    schul_nr = forms.IntegerField(required=False, min_value=1000, max_value=9999,
         widget=forms.TextInput(attrs={'size':10, 'max_length':100, }) )
    schul_beseinr = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_bes_einrichtung_all()),
                        widget=forms.SelectMultiple(attrs={'size':20, 'style':'width:100%'}) )
    schul_rechtsstellung = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_rechtsstellung_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_amt = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_schulamt_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_traeger = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_schultraeger_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_typ = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_schultyp_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_sformangebot = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_sformangebot_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_sprache = forms.MultipleChoiceField(required=False, 
                        choices=get_form_list(get_sprachenfolge_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )
    schul_voraussetzung = forms.MultipleChoiceField(required=False,
                        choices=get_form_list(get_voraussetzung_all()),
                        widget=forms.SelectMultiple(attrs={'size':10, 'style':'width:100%'}) )

  app_name = u'schooldb'
  # --- Sind Daten vorhanden?
  show_errors = (request.method=='POST')
  if show_errors:
    data = request.POST.copy()
  else:
    data = {}
  get = request.GET.copy()
  for g in get:
    data[g] = get[g]
  vars = get_item_vars_show(request, item_container, app_name)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_standard', [ 'schul_name', 'schul_ort', 'schul_plz', 'schul_nr', ] ),
            ('tab_typ',     [ 'schul_typ', 'schul_sformangebot'] ),
            ('tab_beseinr',  [ 'schul_beseinr', ] ),
            ('tab_sprache', [ 'schul_sprache', 'schul_voraussetzung'] ),
            ('tab_org',      [ 'schul_amt', 'schul_traeger'] ),
            ('tab_rechtsstellung',  [ 'schul_rechtsstellung', ] ),
          ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  vars['submit'] = _(u'Suche starten')
  vars['content'] = content
  if request.GET.has_key('show_school'):
    schul_nr = int(request.GET['show_school'])
    vars, vars['title'], vars['header_title'] = get_schul_daten(vars, schul_nr)
    return render_to_response ( 'app/hessen/schooldb/show_schule.html', vars )
  elif item_container.item.string_1 != '' or has_search_items(data):
    # --- Grundfilterung
    if item_container.item.string_1 != '':
      tmp = eval(item_container.item.string_1)
      for k in tmp.keys():
        data[k] = tmp[k]
    schools = get_schulen_by_filter(data)
    # falls nur eine Schul vorhanden ist, wird diese sogleich angezeigt
    # mehrere Schulen werden zur Auswahl abgeboten
    ret = []
    # --- Auswertung des Fragebogens zur Medienausstattung
    if item_container.item.integer_1 == 2008:
      return show_media_survey_csv(request, item_container, schools)
    else:
      for item in schools:
        ret.append({'schul_nr': item[0].Schul_Nr, 
                    'schul_name': item[0].NameSchule, 
                    'schul_ort': item[1].Ort, 
                    'schul_typ': item[0].rel_schultyp.TextKey})
      vars['objs'] = ret
      vars['base_url'] = item_container.get_absolute_url()
      vars['count'] = len(ret)
      vars['title'] = _(u'Suchergebnisse in der hessischen Schuldatenbank')
      if len(ret) == 1:
        schul_nr = int(schools[0][0].Schul_Nr)
        vars, vars['title'], vars['header_title'] = get_schul_daten(vars, schul_nr)
        return render_to_response ( 'app/hessen/schooldb/show_schule.html', vars )
      else:
        return render_to_response ( 'app/hessen/schooldb/schulen.html', vars )
  else:
    vars['show_frame_left'] = True
    # --- Formular anzeigen
    return render_to_response ( 'app/base_edit.html', vars )

def schooldb_slot_get_regionschulen(request, item_container, region):
  """ """
  if region == '':
    return _(u'<p>Bitte geben Sie eine Bildungsregion an!</p>')
  #if request.GET.has_key('show_school'):
  #  app_name = u'schooldb'
  #  schul_nr = int(request.GET['show_school'])
  #  vars = get_item_vars_show(request, item_container, app_name)
  #  vars, vars['title'], vars['header_title'] = get_schul_daten(vars, schul_nr)
  #  return render_to_response ( 'app/hessen/schooldb/show_schule.html', vars )
  response = ''
  t_schools = get_template('app/hessen/schooldb/regionschulen.html')
  #data = { 'schul_amt': region,}
  #items = get_schulen_by_filter(data)
  items = get_regionschulen_by_region(region)
  ret = []
  for item in items:
    ret.append({'schul_nr': item.Schul_Nr, 
                'schul_name': item.NameSchule, 
                'schul_ort': item.Ort, 
                'schul_typ': item.TextKey})
  vars = {'objs': ret,
          'base_url': item_container.get_absolute_url(),
          'count': len(ret),
          'title': _(u'Schulen der Bildungsregion')
         }
  return t_schools.render(Context(vars))
