# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_group_new_name.py

.. loescht User mit dem entsprechenden User-Namen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
0.02  21.04.2008  Gruppenliste
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.utils.safestring  import mark_safe
from django.template.loader import get_template
from django.template    import Context

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import delete_user_by_username
from dms.queries        import get_userfolder_org_id
from dms.queries        import add_group

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_group_new_name(request, item_container):
  """ ergaenzt die Liste der vorhandenen Gruppen """

  def get_group_list(org_id):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    tList = get_template('app/usermanagementorg/group_list.html')
    groups = get_groups(org_id)
    return tList.render(Context({ 'groups': groups, }))

  def group_add_name(org_id, data):
    """ ergaenzt einen neuen Gruppennamen """
    if data.has_key('groupname'):
      groupname = data['groupname']
      add_group(org_id, groupname, False)

  org_id = get_userfolder_org_id(item_container)
  group_items = get_group_list(org_id)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    group_names  = forms.CharField(required=False,
                       widget=forms.HiddenInput(attrs={'value': mark_safe(group_items)}) )
    groupname    = forms.CharField(max_length=40,
                       widget=forms.TextInput(attrs={'size':30}) )

  app_name = 'usermanagementorg'
  my_title = _(u'Gruppenname für Institution ergänzen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'username': '', }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_group_name_add', [ 'group_names', 'groupname', ]) ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  if request.method == 'POST':
    group_add_name(org_id, f.cleaned_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    #assert False
    vars['next'] = './user_management.html?op=group_name_add'
    return render_to_response('app/base_edit.html', vars)
