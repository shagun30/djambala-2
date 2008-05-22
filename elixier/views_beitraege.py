# -*- coding: utf-8 -*-
"""
/dms/elixier/views_beitraege.py

.. schafft den fachlichen Zugang zu den Daten der Elixier-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.07.2007  Beginn der Arbeit
0.03  12.10.2007  views_select_dest
0.04  19.10.2007  get_item_containers_by_url_more
0.05  06.02.2008  Umstellung auf Ajax
0.06  07.04.2008  Status-Aenderungen werden vollzogen
"""

import string
import types

from django.template.loader import get_template
from django.http            import HttpResponse
from django.template    import Context
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.utils.safestring  import SafeData, mark_safe, SafeUnicode
from django.utils.encoding  import smart_unicode

from django.utils.translation import ugettext as _

from dms.settings       import EDUFOLDER_BASE_PATH
from dms.roles          import require_permission
from dms.queries        import get_folder_filtered_items
from dms.queries        import get_item_container_by_path
from dms.queries        import get_item_containers_by_url_more
from dms.queries              import get_site_url

from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_folderish_vars_edit
from dms.utils          import show_link
from dms.utils          import get_tabbed_form

from dms.elixier.queries  import get_elixier_table_items
from dms.elixier.queries  import get_elixier_item
from dms.elixier.queries  import get_elixier_filtered_items
from dms.elixier.queries  import change_elixier_item_status
from dms.elixier.queries  import set_elixier_item_status

from dms.elixier.utils    import views_select_dest
from dms.elixier.utils    import do_check

from dms.elixier.help_form   import help_form

# -----------------------------------------------------
def get_back_raw(request, item_container):
  """ liefert die "nackte" URL der Ruecksprungadresse """
  return item_container.get_absolute_url() + '?elixier_op=fach_beitraege'

# -----------------------------------------------------
def get_data(data, name, is_string):
  if data.has_key(name):
    return data[name]
  else:
    if is_string:
      return ''
    else:
      return None

# -----------------------------------------------------
def clean_data(data):
  """ Mehrfacheingaben werden in Listen umgewandelt """
  cleaned_data = {}
  keys = data.keys()
  for key in keys:
    this_item = data.getlist(key)
    if len(this_item) == 1:
      cleaned_data[key] = this_item[0]
    else:
      cleaned_data[key] = this_item
  return cleaned_data

# -----------------------------------------------------
def get_param(bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort):
  """ liefert die entsprechenden Parameter """
  param = ''
  if bildungsebene != None:
    param += u'&bildungsebene=' + smart_unicode(bildungsebene)
  if fach_sachgebiet != None:
    param += u'&fach_sachgebiet=' + smart_unicode(fach_sachgebiet)
  if medienformat != None:
    param += u'&medienformat=' + smart_unicode(medienformat)
  if quelle != None:
    param += u'&quelle=' + smart_unicode(quelle)
  if schlagwort != None:
    param += u'&schlagwort=' + smart_unicode(schlagwort)
  return param

# -----------------------------------------------------
def get_back_url(request, item_container, bildungsebene, fach_sachgebiet,
                          medienformat, quelle, schlagwort):
  """ liefert die URL der Ruecksprungadresse """
  back_url = get_back_raw(request, item_container) + \
             get_param(bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort)
  return back_url

# -----------------------------------------------------
def get_back_link(back_url):
  """ liefert den Verweis der Ruecksprungadresse """
  return show_link(back_url, _(u'Zurück zur Übersicht ...'))

# -----------------------------------------------------
@require_permission('perm_add')
def get_ajax_data(request, item_container, is_string=False):
  data = clean_data(request.GET)
  data_post = clean_data(request.POST)
  if data_post != {}:
    for key in data_post.keys():
      data[key] = data_post[key]
  bildungsebene = get_data(data, 'bildungsebene', is_string)
  fach_sachgebiet = data['fach_sachgebiet']
  medienformat = get_data(data, 'medienformat', is_string)
  quelle = get_data(data, 'quelle', is_string)
  if data.has_key('schlagwort'):
    schlagwort = data['schlagwort']
  else:
    schlagwort = ''
  if data.has_key('do_reject') and data.has_key('reject_id'):
    reject_ids = data['reject_id']
    for reject_id in reject_ids:
      change_elixier_item_status(reject_id, -1)
  if data.has_key('do_unknown') and data.has_key('unknown_id'):
    reject_ids = data['unknown_id']
    for reject_id in reject_ids:
      change_elixier_item_status(reject_id, 0)
  return bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort

# -----------------------------------------------------
@require_permission('perm_add')
def views_beitraege(request,item_container, op):
  """ schafft den fachlichen Zugang zu den Daten der Elixier-Datenbank an """

  def get_elixier_list(table_name):
    """ """
    items = get_elixier_table_items(table_name)
    ret = []
    for item in items:
      ret.append( (item.id, mark_safe(item.name)) )
    return ret

  class dms_itemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    bildungsebene  = forms.ChoiceField(required=False,
                           choices=get_elixier_list('bildungsebene'),
                                widget=forms.RadioSelect() )
    fach_sachgebiet= forms.ChoiceField(choices=get_elixier_list('fach_sachgebiet'),
                                widget=forms.RadioSelect() )
    medienformat   = forms.ChoiceField(required=False,
                           choices=get_elixier_list('medienformat'),
                                widget=forms.RadioSelect() )
    quelle         = forms.ChoiceField(required=False, choices=get_elixier_list('quelle'),
                                widget=forms.RadioSelect() )
    schlagwort     = forms.CharField(required= False, max_length=60,
                                widget=forms.TextInput(attrs={'size':40}) )

  app_name = 'elixier'
  my_title = _(u'Beiträge auswählen')
  data_init = {}

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  if request.method == 'POST':
    data = request.POST.copy ()
  elif request.method == 'GET':
    data = request.GET.copy ()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm(data)
  tabs = [
            ('tab_fach_sachgebiet' , ['fach_sachgebiet', ]),
            ('tab_quelle' , ['quelle', ]),
            ('tab_bildungsebene' , ['bildungsebene', ]),
            ('tab_schlagwort' , ['schlagwort', ]),
            ('tab_medienformat' , ['medienformat', ]),
          ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  get = request.GET.copy()
  if get.has_key('item_id'):
    return views_show_item(request, item_container, get['item_id'])
  elif request.method == 'POST' and (not f.errors and request.POST.has_key('do_reject')):
    ids = clean_data(request.POST)['reject_id']
    if type(ids) == types.ListType:
      for id in ids:
        change_elixier_item_status(id, -1)
    else:
      change_elixier_item_status(ids, -1)
    return views_show_summary(request, item_container, f.data)
  elif request.method == 'POST' and (not f.errors and request.POST.has_key('do_unknown')):
    ids = clean_data(request.POST)['unknown_id']
    if type(ids) == types.ListType:
      for id in ids:
        change_elixier_item_status(id, 0)
    else:
      change_elixier_item_status(ids, 0)
    return views_show_summary(request, item_container, f.data)
  elif request.GET.has_key('show_list') or data.has_key('fach_sachgebiet'):
    my_data = request.GET.copy()
    return views_show_summary(request, item_container, my_data)
  else:
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text'] = _(u'<p>Hier beschreiben Sie die Suchparameter der gewünschten Beiträge')
    return render_to_response ( 'app/base_edit.html', vars )

  BACK_URL = get_back_link(item_container.get_absolute_url())

  def get_fach_items(op):
    title = _(u'Fachlicher Zugang zu den Daten der Elixier-Datenbank')
    items = []
    return title, items

  def get_fach_infos(op):
    """ zeigt statistische Informationen der Elixier-Datenbank """
    t_statistik = get_template('app/elixier/base_beitraege.html')
    title, items = get_fach_items(op)
    statistik_context = Context (  { 'title': title, 'items': items, 'next': BACK_URL } )
    return t_statistik.render(statistik_context)

  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = _(u'<p>Hier beschreiben Sie das Suchmuster der gewünschten Beiträge')
  vars['text_more'] = ''
  vars['content'] = get_fach_infos(op)
  return render_to_response ( 'app/base_folderish.html', vars )

# -----------------------------------------------------
@require_permission('perm_add')
def views_show_summary(request,item_container, data):
  """ zeigt die Ueberschriften der ausgewaehlten Beitraege der Elixier-Datenbank an """
  bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort = get_ajax_data(request, item_container)
  t_beitraege = get_template('app/elixier/base_beitraege.html')
  BACK_URL = get_back_link(get_back_url(request, item_container, bildungsebene, fach_sachgebiet,
                                        medienformat, quelle, schlagwort))
  ajax_param = '?elixier_op=fach_beitraege' + get_param(bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort)
  beitraege_context = Context (  { 'title': _(u'Ausgewählte Beiträge'),
                                   'fach_sachgebiet': fach_sachgebiet,
                                   'bildungsebene' :bildungsebene,
                                   'fach_sachgebiet': fach_sachgebiet,
                                   'medienformat': medienformat,
                                   'quelle': quelle,
                                   'schlagwort': schlagwort,
                                   'ajax_url': get_site_url(item_container, 'elixier.html/ajax/'),
                                   'ajax_param': ajax_param,
                                   'next': BACK_URL } )
  content = t_beitraege.render(beitraege_context)
  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = ''
  vars['text_more'] = ''
  vars['content'] = content
  return render_to_response ( 'app/base_folderish.html', vars )

# -----------------------------------------------------
@require_permission('perm_add')
def views_show_item(request, item_container, item_id):
  """ zeigt ein einzelnen Elixier-Item """

  def get_status_choices():
    """ """
    ret = []
    ret.append(( 1, _(u'übernehmen / übernommen')))
    ret.append(( 0, _(u'unbearbeitet lassen')))
    ret.append((-1, _(u'ablehnen / abgelehnt')))
    return ret

  def get_data(data, name):
    if data.has_key(name):
      return data[name]
    else:
      return None

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    dest_folder = forms.CharField(required=False,
         widget=forms.TextInput(attrs={'size':50, 'max_length':120}) )
    status = forms.CharField(required=False, widget=forms.Select(choices=
         get_status_choices(), attrs={'size':3, 'style':'width:60%'} ) )

  t_beitraege = get_template('app/elixier/base_beitrag.html')
  item_org, item = get_elixier_item(item_id)
  my_title = _(u'Elixierbeitrag zuordnen')
  app_name = 'elixier'
  # --- Sind Daten vorhanden oder muessen Sie initialisiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else:
    if not request.COOKIES.has_key('elixier_dest_folder'):
      request.COOKIES['elixier_dest_folder'] = '/'
    data = {'status': item.status,
            'dest_folder': request.COOKIES['elixier_dest_folder'], }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_status', [ 'dest_folder', 'status',] ), ]
  form_status = get_tabbed_form(tabs, help_form, app_name, f)

  if request.GET.has_key('do_import'):
    # --- Status aendern
    new_status = int(f.data['status'])
    if item.status != new_status:
      do_check(request, item, item_org, new_status, f.data['dest_folder'])
  data = request.GET.copy()
  fach_sachgebiet = get_data(data,'fach_sachgebiet')
  bildungsebene = get_data(data, 'bildungsebene')
  fach_sachgebiet = get_data(data, 'fach_sachgebiet')
  medienformat = get_data(data, 'medienformat')
  quelle = get_data(data, 'quelle')
  schlagwort = get_data(data, 'schlagwort')
  BACK_RAW = item_container.get_absolute_url() + '?' + request.META['QUERY_STRING']
  BACK_LINK = get_back_link(get_back_url(request, item_container, bildungsebene, fach_sachgebiet,
                                         medienformat, quelle, schlagwort)+'&show_list=1')
  select_dest = show_link('javascript:select_dest_url(document.form_input.dest_folder)',
                          _(u'Zielordner festlegen ...'), url_extern="_extern")
  dest_url = item_container.get_absolute_url() + '?elixier_op=select_dest'
  does_exist = get_item_containers_by_url_more(item_org.url_ressource)
  # wurde der Beitrag schon vorher eingegeben?
  if does_exist:
    if item.status != 1:
      set_elixier_item_status(item, 1)
      form_status = ''
  beitraege_context = Context ( { 'does_exist': does_exist,
                                  'item': item_org,
                                  'form_status': form_status,
                                  'action': BACK_RAW + '&do_import=1',
                                  'submit': my_title,
                                  'select_dest': select_dest,
                                  'fach_sachgebiet': fach_sachgebiet,
                                  'bildungsebene': bildungsebene,
                                  'fach_sachgebiet': fach_sachgebiet,
                                  'medienformat': medienformat,
                                  'quelle': quelle,
                                  'schlagwort': schlagwort,
                                  'dest_url': dest_url,
                                  'next': BACK_LINK } )
  content = t_beitraege.render(beitraege_context)
  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = ''
  vars['text_more'] = ''
  vars['content'] = content
  # --- Formular anzeigen
  return render_to_response ( 'app/base_folderish.html', vars )

# -----------------------------------------------------
@require_permission('perm_add')
def elixier_ajax_get_unknown(request, item_container):
  """ liefert die unbearbeiteten Beitraege """
  bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort = \
      get_ajax_data(request, item_container, True)
  items_unknown = get_elixier_filtered_items(bildungsebene, fach_sachgebiet,
                                     medienformat, quelle, schlagwort,0)
  t_section = get_template('app/elixier/section_unknown_beitraege.html')
  context = Context({ 'items': items_unknown,
                      'params': get_param(bildungsebene, fach_sachgebiet, medienformat, 
                                          quelle, schlagwort),
                      'fach_sachgebiet': fach_sachgebiet,
                      'bildungsebene' :bildungsebene,
                      'medienformat': medienformat,
                      'quelle': quelle,
                      'schlagwort': schlagwort,
                      'item_count': len(items_unknown),
                    })
  return HttpResponse(t_section.render(context), mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def elixier_ajax_get_ok(request, item_container):
  """ liefert die angenommenen Beitraege """
  bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort = \
      get_ajax_data(request, item_container, True)
  items_ok = get_elixier_filtered_items(bildungsebene, fach_sachgebiet,
                                     medienformat, quelle, schlagwort,1)
  t_section = get_template('app/elixier/section_ok_beitraege.html')
  context = Context({ 'items': items_ok, 
                      'params': get_param(bildungsebene, fach_sachgebiet, medienformat, 
                                          quelle, schlagwort),
                      'fach_sachgebiet': fach_sachgebiet,
                      'bildungsebene' :bildungsebene,
                      'medienformat': medienformat,
                      'quelle': quelle,
                      'schlagwort': schlagwort,
                      'item_count': len(items_ok),
                    })
  return HttpResponse(t_section.render(context), mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
@require_permission('perm_add')
def elixier_ajax_get_rejected(request, item_container):
  """ liefert die abgelehnten Beitraege """
  bildungsebene, fach_sachgebiet, medienformat, quelle, schlagwort = \
    get_ajax_data(request, item_container, True)
  items_rejected = get_elixier_filtered_items(bildungsebene, fach_sachgebiet,
                                     medienformat, quelle, schlagwort,-1)
  t_section = get_template('app/elixier/section_beitraege.html')
  context = Context({ 'items': items_rejected,
                      'params': get_param(bildungsebene, fach_sachgebiet, medienformat, 
                                          quelle, schlagwort),
                      'fach_sachgebiet': fach_sachgebiet,
                      'bildungsebene' :bildungsebene,
                      'medienformat': medienformat,
                      'quelle': quelle,
                      'schlagwort': schlagwort,
                      'item_count': len(items_rejected),
                    })
  return HttpResponse(t_section.render(context), mimetype="text/html; charset=utf-8")

#http://dms.bildung.hessen.de/wir_ueber_uns/intern/elixier/elixier.html/ajax/elixier_ajax_get_rejected/?elixier_op=fach_beitraege&fach_sachgebiet=175

