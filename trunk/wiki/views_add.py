# -*- coding: utf-8 -*-
"""
/dms/wiki/views_add.py

.. enthaelt den View zum Ergaenzen eines Wikis
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.02.2008  Beginn der Arbeit
0.02  17.03.2008  erste Integration der Wiki-Seiten
0.03  18.03.2008  get_role_choices
"""

from django.db          import transaction
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission

from dms.queries        import get_site_url
from dms.queries        import get_parent_app
from dms.queries        import get_org_by_username
from dms.queries        import get_role_by_user_path
from dms.queries        import save_container_values
from dms.queries        import save_item_values
from dms.queries        import exist_item

from dms.views_error    import show_error_object_exist
from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils_form     import get_folderish_vars_add

from dms.projectgroup.utils       import get_role_choices
from dms.wiki.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add_folderish')
def wiki_add(request, item_container):
  """ neues Wiki anlegen """

  parent_app = get_parent_app(item_container)
  my_role = get_role_by_user_path(request.user, item_container.container.path)

  @ transaction.commit_manually
  def save_values(name, new, item_container):
    """ Wiki inkl. Startseite speichern """
    new['integer_1'] = new['role_id']
    new['integer_2'] = False
    new['has_user_support'] = True
    new['has_comments'] = True
    new['is_moderated'] = False
    if not new.has_key('section'):
      new['section'] = ''
    wiki_item_container = save_container_values(request.user, 'dmsWiki', name, new, item_container)
    new = {}
    new['title'] = _(u'Startseite')
    new['text'] = _(u'<p>Der Text dieser Startseite muss geändert werden ...</p>')
    new['name'] = name = _(u'start.html')
    save_item_values(request.user, 'dmsWikiItem', name, new, wiki_item_container, 
                     not wiki_item_container.item.is_moderated,
                     send_email=True)
    transaction.commit()

  class DmsItemForm(forms.Form):
    name      =forms.CharField(max_length=60,
                      widget=forms.TextInput(attrs={'size':20}) )
    title     =forms.CharField(max_length=240,
                      widget=forms.TextInput(attrs={'size':60}) )
    nav_title = forms.CharField(required=False, max_length=60,
                      widget=forms.TextInput(attrs={'size':30}) )
    section   = forms.CharField(required=False,
                      widget=forms.Select(choices=get_section_choices(item_container.container.sections),
                                          attrs={'size':4, 'style':'width:40%'} ) )
    role_id   = forms.CharField(required=True,
                        widget=forms.Select(choices=get_role_choices(my_role),
                                            attrs={'size':6, 'style':'width:100%'} ) )

  app_name = 'wiki'
  my_title = _(u'Wiki anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else:
    # role_id = 60 worker_reader (Schueler)
    data = { 'role_id': 60 }
  f = DmsItemForm(data)
  # --- Reihenfolge, Ueberschriften, Hilfetexte
  options = ['name','title', 'nav_title', 'role_id' ]
  if item_container.item.app.name != 'dmsWiki':
    options. append('section')
  tabs = [('tab_base', options ),]
  # --- Formular zusammenbauen
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    # --- Umlaute aus Namen entfernen
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response ( 'app/base_edit.html', vars )
