# -*- coding: utf-8 -*-
"""
/dms/freemind/views_add.py

.. enthaelt den View zum Ergaenzen einer Informationsseite
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.02.2007  Beginn der Arbeit
0.02  27.02.2007  check_name
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices, check_name
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_add

from dms.queries        import save_item_values
from dms.queries        import exist_item

from dms.freemind.utils     import save_mindmap
from dms.freemind.help_form import help_form

from dms.views_error      import show_error_object_exist
from dms.views_error      import show_error

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def freemind_add(request, item_container):
  """ neuen Freemind-Player anlegen """

  def save_values(name, new, files, item_container):
    """ Freemind sichern """
    folder_name = name[:-3]
    save_mindmap(folder_name, name, files, item_container)
    # --- name ohne .zip
    name = folder_name
    community_id = 0
    schulverbund_id = 0
    new['url_more_extern'] = True
    save_item_values(request.user, 'dmsFreemind', name, new, item_container, True)

  class DmsItemForm ( forms.Form ) :
    """ Elemente des Eingabeformulars """
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    sub_title  = forms.CharField(required=False, max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False,
                       widget=forms.Textarea(
                                  attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    section    = forms.CharField(required=False,
                        widget=forms.Select(choices=
                                     get_section_choices(item_container.container.sections),
                                     attrs={'size':4, 'style':'width:40%'} ) )
    license         = forms.ChoiceField(choices=get_license_choices(item_container),
                                        widget=forms.RadioSelect() )

  app_name = 'freemind'
  my_title = _(u'Freemind-Player anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'license': 1,}
  f = DmsItemForm(data)
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  tabs = [ ('tab_base', [ 'fname', 'title', 'sub_title', 'text', 'section' ]),
           ('tab_license',    [ 'license', ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors :
    name = check_name(request.FILES['fname']['filename'], True)
    # --- handelt es sich um eine Freemind-Datei?
    if name.lower()[-3:] != '.mm':
      return show_error(request, item_container, _(u'Falsche Datei'), 
                        _(u'<p>Sie können nur Freemind-Datei verwenden!</p>'))
    elif not exist_item(item_container, name):
      save_values(name, f.data, request.FILES, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_item_vars_add(request, item_container, app_name, my_title,
                             content, show_errors)
    vars['text_intro'] = help_form['copyright']['help']
    return render_to_response ( 'app/freemind/manage_edit.html', vars )
