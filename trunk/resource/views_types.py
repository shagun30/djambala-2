# -*- coding: utf-8 -*-
"""
/dms/resource/views_types.py

.. Kategorien einer Ressourcenverwaltung loeschen und neu anlegen
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.05.2008  Uebernahme von views_show
"""


from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from django             import newforms as forms

from dms.utils          import clean_data
from dms.utils          import get_tabbed_form

from dms.utils_form     import get_folderish_vars_add
from dms.utils_form     import get_folderish_vars_show

from dms.queries        import get_userfolder_org_id

from dms.resource.queries     import delete_type

from dms.resource.utils       import get_app_name
from dms.resource.utils       import get_type_res_list

from dms.resource.help_form   import help_form

# -----------------------------------------------------
def feedback_vars(request, item_container, app_name, info, arg_str=''):
  """
  erzeugt die vars fuer die Feedback-Seite
  arg_str ohne "?"
  """
  vars = get_folderish_vars_show(request, item_container, app_name, '', 
                                False)
  vars['next'] = item_container.get_absolute_url() + '?' + arg_str
  vars['feedback'] = info
  return vars


# -----------------------------------------------------
def get_types_list_no_resource(request, item_container):
  """ Liste der Kategorien, in denen keine Ressourcen definiert sind """
  from dms.queries              import get_userfolder_org_id
  org_id          = get_userfolder_org_id(item_container)
  my_type_list = get_type_res_list(org_id)
  empty_types = []
  for t in my_type_list:
    if t[2]>0:
      empty_types += [ [ t[0].id, t[0].description ] ]
  return empty_types
  
# -----------------------------------------------------
def resource_types_del(request, item_container):
  """ """
  org_id = get_userfolder_org_id(item_container)
  my_choices = get_types_list_no_resource(request, item_container)
  if clean_post.has_key('del_type'):
    del_list = clean_post['del_type']
    if  type(del_list)!=type([]):
      del_list = [del_list]
    for i in del_list:
      delete_type( int(i))
    vars = feedback_vars(request, item_container, app_name, _(u"Die markierten Kategorien wurden frei gegeben."), '')
  else:
    vars = feedback_vars(request, item_container, app_name, _(u"Es waren keine Kategorien zur Freigabe markiert."), '')
  return render_to_response('app/resource/feedback.html', vars)

# -----------------------------------------------------
def resource_types_do_del(request, item_container):
  """ ausgewaehlte Kategorien loeschen """
  app_name   = get_app_name()
  org_id = get_userfolder_org_id(item_container)
  my_type_list = get_type_res_list(org_id)
  clean_post   = clean_data( request.POST.copy() )
  if clean_post.has_key('del_type'):                     # loeschen
    del_list = clean_post['del_type']
    if type(del_list) != type([]):
      del_list = [del_list]
    for i in del_list:
      pass #delete_type( int(i))
    vars = feedback_vars(request, item_container, app_name, _(u"Die markierten Kategorien wurden frei gegeben."), '')
  else:                                                 # nichts ausgewaehlt
    vars = feedback_vars(request, item_container, app_name, _(u"Es waren keine Kategorien zum Löschen ausgewählt."), '') 
  return render_to_response('app/resource/feedback.html', vars)
  
# -----------------------------------------------------
def resource_type_new(request, item_container):
  """ neue Kategorie anlegen """
  app_name   = get_app_name()
  org_id = get_userfolder_org_id(item_container)
  my_type_list = get_type_res_list(org_id)
  my_choices = []
  for t in my_type_list:
    my_choices += [(t[0].id, t[0].description)]

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    type_description = forms.CharField(required=True, max_length=240,
                  widget=forms.TextInput(attrs={'size':30}) )

  if (request.method == 'POST'):
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [
          ( 'tab_new_type'   , [ 'type_description', ], ),
        ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  my_title = _(u'Anlegen einer neuen Kategorie')
  vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, True)
  if request.method=='POST' and not f.errors:
    # checken, ob der Name bereits existiert
    new_type_descr = clean_post['type_description'].strip()
    new_is_ok = True
    for c in my_choices:
      if new_type_descr == c[1].strip():
        new_is_ok = False
        break
    if new_is_ok:
      append_type(org_id, new_type_descr)
      #vars['next'] = item_container.container.path + "index.html?step=20"
      """
      my_types = []
      for t in my_type_list:
        if t[2]>0: is_empty = False
        else     : is_empty = True
        my_types += [ [ is_empty, t[0], t[1] ] ]
      #vars['my_types'] = my_types
      """
      vars = feedback_vars(request, item_container, app_name, _(u"Die Kategorie wurde neu angelegt."), '')
      vars['next'] = item_container.get_absolute_url()
      return render_to_response('app/resource/feedback.html', vars)
    else:
      vars = feedback_vars(request, item_container, app_name, _(u"Der Name ist bereits vergeben."), '')
      vars['next'] = item_container.get_absolute_url()
      return render_to_response('app/resource/feedback.html', vars)
  else:
    vars['next'] = item_container.get_absolute_url()
    return render_to_response ( 'app/base_edit.html', vars )
