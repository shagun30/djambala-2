# -*- coding: utf-8 -*-
"""
/dms/resource/views_resources.py

.. Ressourcen einer Ressourcenverwaltung loeschen und neu anlegen
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.05.2008  Beginn der Arbeit
"""


from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from django             import newforms as forms

from dms.queries              import get_userfolder_org_id

from dms.utils          import clean_data
from dms.utils          import get_tabbed_form

from dms.utils_form     import get_folderish_vars_add
from dms.utils_form     import get_folderish_vars_show

from dms.resource.queries     import append_resource
from dms.resource.queries     import delete_type

from dms.resource.utils       import get_app_name
from dms.resource.utils       import get_type_res_list
from dms.resource.utils       import feedback_vars

from dms.resource.help_form   import help_form

# -----------------------------------------------------
def get_app_name():
  """ liefert ressource """
  return 'resource'

# -----------------------------------------------------
def resource_resource_new(request, item_container):
  """ neue Ressource anlegen """
  app_name   = get_app_name()
  org_id = get_userfolder_org_id(item_container)
  my_type_list = get_type_res_list(org_id)
  my_types = []
  for t in my_type_list:
    my_types.append( (t[0].id, t[0].description) )

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    res_type_id     = forms.ChoiceField(choices=my_types,
                                        widget=forms.RadioSelect())
    res_description = forms.CharField(max_length=240,
                                        widget=forms.TextInput(attrs={'size':30}) )
    res_descr_more  = forms.CharField(required=False, widget=forms.Textarea(
                         attrs={'rows':8, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    res_url         = forms.URLField(required=False, max_length=240,
                                        widget=forms.TextInput(attrs={'size':60}) )

  if (request.method == 'POST'):
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [
          ( 'tab_new_res'   , [ 'res_type_id', 'res_description', 'res_descr_more', 'res_url',], ),
        ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  my_title = _(u'Anlegen einer neuen Ressource')
  vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, True)
  if request.method=='POST' and not f.errors:
    # checken, ob der Name bereits existiert
    new_is_ok = True
    if new_is_ok:
      append_resource(f.data['res_type_id'], f.data['res_description'], f.data['res_descr_more'], f.data['res_url'])
      vars = feedback_vars(request, item_container, app_name, _(u"Die Ressource wurde neu angelegt."), '')
      vars['next'] = item_container.get_absolute_url() + '/resource_new/'
      return render_to_response('app/resource/feedback.html', vars)
    else:
      vars = feedback_vars(request, item_container, app_name, _(u"Der Name ist bereits vergeben."), '')
      vars['next'] = item_container.get_absolute_url() + '/resource_new/'
      return render_to_response('app/resource/feedback.html', vars)
  else:
    vars['next'] = item_container.get_absolute_url() + '/resource_new/'
    return render_to_response ( 'app/base_edit.html', vars )

# -----------------------------------------------------
def resource_resources_del(request, item_container):
  """ Ressourcen loeschen """
  if get.has_key('res_id'):
    res_id     = int(get['res_id'])
  else:
    res_id     = int(clean_post['res_id'])
  my_res     = get_resource(res_id)
  res_unused = resource_unused(res_id)
  #res_type, dummy     = get_type_of_resource(res_id)
  res_type   = my_res.res_type.id
  my_res_list = get_resource_list(res_type)
  my_choices = []
  for r in my_res_list:
    if r.id!=res_id:
      my_choices += [(r.id, r.description)]
  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    res_description = forms.CharField(max_length=240,
                  widget=forms.TextInput(attrs={'size':30}) )
    res_descr_more  = forms.CharField(required=False, widget=forms.Textarea(
                          attrs={'rows':5, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    res_url         = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'size':60}) )
    if len(my_res_list)>0:
      if len(my_res_list)>10:
        showchoices = 10
      else:
        showchoices = len(my_res_list)
      existing_res    = forms.CharField(required=False, widget=forms.Select(choices=my_choices, attrs={'size':showchoices, 'style':'width:40%'} ) )
    else:
      existing_res    = forms.CharField(required=False, widget=forms.Select(choices=[(0, ' - keine -')], attrs={'size':1, 'style':'width:40%'} ) )
    if res_unused:
      delete_res      = forms.BooleanField(required=False)
  # --- Sind Daten vorhanden oder muessen sie initialisiert werden?
  if (request.method == 'POST'): # ??????????????????????????????????????????????????????????????
    data = request.POST.copy()
  else :
    data = { 'res_description' : my_res.description,
              'res_descr_more'  : my_res.description_more,
              'res_url'         : my_res.url }
  """
    if len(my_res_list)>0:
      data = {}
    else:
      data = {'existing_res' : " - keine -"}
  """
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  show_errors = (f.errors!={})   # ??????????????????????????????????????????????????????????????
  if res_unused:
    tabs = [
          ( 'tab_edit_res'   , [ 'res_description', 'res_descr_more', 'res_url', 'existing_res'], ),
          ( 'tab_del_res'    , [ 'delete_res']),
        ]
  else:
    tabs = [
          ( 'tab_edit0_res'  , [ 'res_description', 'res_descr_more', 'res_url', 'existing_res'], ),
        ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  
  my_title = _(u'Ressourcenverwaltung: Bearbeiten oder Löschen der Ressource ' + my_res.description)
  vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
  
  if request.method=='POST' and not f.errors:
    # checken, ob der Name bereits existiert
    new_res_descr = clean_post['res_description'].strip()
    new_is_ok = True
    for c in my_choices:
      if new_res_descr == c[1].strip():
        new_is_ok = False
        break
  else :
    vars['submit']   = _(u"Ressource bearbeiten")
    vars['next']     = item_container.container.path + "index.html?step=24"
    vars['res_type'] = res_type
    return render_to_response ( 'app/resource/my_base_edit.html', vars )
