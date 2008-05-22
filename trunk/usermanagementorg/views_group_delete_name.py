# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_group_delete_name.py

.. loescht User mit dem entsprechenden User-Namen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.04.2008  Beginn der Arbeit
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
from dms.queries        import delete_group_by_id
from dms.queries        import delete_users_in_group

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_group_delete_name(request, item_container):
  """ loescht Gruppe aus der Liste der vorhandenen Gruppen """

  org_id = get_userfolder_org_id(item_container)

  def get_group_list(org_id):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    tList = get_template('app/usermanagementorg/group_list.html')
    groups = get_groups(org_id, True)
    return tList.render(Context({ 'groups': groups, }))

  def get_group_names(org_id):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    groups = get_groups(org_id)
    ret = []
    for group in groups:
      if not group['is_primary']:
        ret.append((group['id'], group['description']))
    return ret

  def group_delete_name(data):
    """ loescht die entsprechenden Gruppen """
    if data.has_key('group_names_del'):
      for group in data['group_names_del']:
        delete_users_in_group(group)
        delete_group_by_id(group)

  group_items = get_group_list(org_id)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    group_names_primary = forms.CharField(required=False,
                       widget=forms.HiddenInput(attrs={'value': mark_safe(group_items)}) )
    group_names_del = forms.MultipleChoiceField(required=False, choices=get_group_names(org_id),
                            widget=forms.CheckboxSelectMultiple() )

  app_name = 'usermanagementorg'
  my_title = _(u'Gruppen der Institution löschen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_group_name_delete', [ 'group_names_primary', 'group_names_del', ]) ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  if request.method == 'POST':
    group_delete_name(f.cleaned_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    #assert False
    vars['next'] = './user_management.html?op=group_name_delete'
    return render_to_response('app/base_edit.html', vars)
