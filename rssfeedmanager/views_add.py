# -*- coding: utf-8 -*-
"""
/dms/rssfeedmanager/views_add.py

.. enthaelt den View zum Ergaenzen einer Verwaltungsseite fuer RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  24.03.2007  Beginn der Arbeit
0.02  09.05.2007  get_folderish_vars
0.03  04.07.2007  Umstellung auf Folder
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import *
from dms.views_error    import show_error_object_exist

from dms.queries        import save_container_values
from dms.queries        import exist_item
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices, check_name
from dms.utils_form     import get_folderish_vars_add

from dms.rssfeedmanager.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def rssfeedmanager_add(request, item_container):
  """ neue Verwaltungsseite anlegen """

  @transaction.commit_manually
  def save_values(name, new, item_container):
    """ """
    save_container_values(request.user, 'dmsRssFeedManager', name, new, item_container)

  class DmsItemForm ( forms.Form ) :
    name       = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':20}) )
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    nav_title  = forms.CharField(required=False, max_length=60,
                       widget=forms.TextInput(attrs={'size':30}) )
    section    = forms.CharField(required=False,
                        widget=forms.Select(choices=
                                     get_section_choices(item_container.container.sections),
                                     attrs={'size':4, 'style':'width:40%'} ) )

  app_name = 'rssfeedmanager'
  my_title = _(u'Verwaltungsseite für RSS-Feeds anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = { 'name' : 'rss_feeds',
             'title': 'Verwaltung von RSS-Feeds',
           }
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [ ('tab_base', [ 'name', 'title', 'nav_title', 'section', ]), ]

  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    name = check_name(f.data['name'], True)
    if not exist_item(item_container, name):
      save_values(name, f.data, item_container)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item, name)
  else:
    vars = get_folderish_vars_add(request, item_container, app_name, my_title, content, show_errors)
    #vars['action'] = get_actions(request, user_perms, item)
    return render_to_response ( 'app/base_edit.html', vars )
