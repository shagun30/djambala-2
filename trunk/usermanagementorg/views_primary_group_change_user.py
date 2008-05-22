# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_primary_group_change_user.py

.. aendert die primaere Gruppenzugehoerigkeit
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.04.2008  Beginn der Arbeit
"""

import string
import types

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
from dms.queries        import get_users_by_org_id
from dms.queries        import get_users_by_group_id
from dms.queries        import get_group_by_id
from dms.queries        import delete_group_by_user_id
from dms.queries        import set_user_group
from dms.queries        import get_user_by_id
from dms.queries        import get_primary_group_by_user
from dms.queries        import delete_primary_group_by_user

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import clean_data
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_primary_group_change_user(request, item_container):
  """ aendert die Gruppenzugehoerigkeit von Usern """

  org_id = get_userfolder_org_id(item_container)

  def get_group_list(org_id):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    tList = get_template('app/usermanagementorg/group_list.html')
    groups = get_groups(org_id, True)
    return tList.render(Context({ 'groups': groups, }))

  def get_group_names(org_id, restricted):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    groups = get_groups(org_id)
    ret = []
    if restricted:
      ret.append((-1, _(u'Alle Mitglieder')))
    for group in groups:
      if (restricted and group['is_primary']) or (not restricted and not group['is_primary']):
        ret.append((group['id'], group['description']))
    return ret

  def get_group_names_selected(org_id):
    """ liefert die IDs der Gruppen der Organisation org_id """
    groups = get_groups(org_id)
    ret = []
    for group in groups:
      ret.append(group['id'])
    return ret

  group_items = get_group_list(org_id)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    group_names = forms.ChoiceField(choices=get_group_names(org_id, True), widget=forms.RadioSelect() )

  app_name = 'usermanagementorg'
  my_title = _(u'Primärgruppe ändern')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else:
    targets = {}
    for group in get_group_names(org_id, False):
      targets[0] = True
    data = { 'group_names_target': targets, }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_primary_group_user_change', [ 'group_names', ]) ]
  # --- Zuordnung wurde vorgenommen
  if request.method == 'POST' and request.POST.has_key('modus_change'):
    data = clean_data(f.data)
    keys = data.keys()
    user_group_ids = []
    for key in keys:
      if key.find('group_u') == 0:
        arr = string.splitfields(key, '_') # group_u_xxxx
        this_user_id = int(arr[1][1:])
        this_user = get_user_by_id(this_user_id)
        this_group_id = int(data['group_u%i' % this_user_id])
        this_group = get_group_by_id(this_group_id)
        user_group = get_primary_group_by_user(this_user)
        if user_group == None or user_group.group.id != this_group_id:
          if user_group != None:
            delete_primary_group_by_user(this_user)
          set_user_group(this_user, this_group)
    return HttpResponseRedirect(item_container.get_absolute_url())
  # --- Welche Gruppen werden ausgewaehlt?
  elif request.method == 'POST' and not f.errors:
    # --- Auswahl der Gruppen
    if request.POST.has_key('group_names'):
      data = clean_data(f.data)
      # --- Basisgruppe
      this_group = int(data['group_names'])
      if this_group == -1:
        group_name = _(u'alle Mitglieder')
        group_users = get_users_by_org_id(org_id)
      else:
        group_name = get_group_by_id(this_group).description
        group_users = get_users_by_group_id(this_group)
      # --- Zielgruppen
      target_groups = []
      g_target = get_group_names(org_id, True)
      for target_group in g_target:
        # welchen User befinden sich bereits in der Gruppe
        t_group = target_group[0]
        if t_group > 0:
          t_users = []
          for u in get_users_by_group_id(t_group):
            t_users.append(u.user)
          target = { 'id': int(t_group), 
                     'name': get_group_by_id(t_group).description,
                     'group_users': t_users }
          target_groups.append(target)
      users = []
      tInput = get_template('app/usermanagementorg/group_input_radio.html')
      for u in group_users:
        # bei welchen Users muss die Checkbox gesetzt werden?
        inputs = ''
        for target in target_groups:
          input = tInput.render( Context( { 'user_id': u.user.id,
                                            'group_id': target['id'],
                                            'checked': u.user in target['group_users']
                                          } )
                               )
          inputs += input
        users.append( {'name': u.user.get_standard_name(), 
                       'user_id': u.user.id,
                       'inputs': inputs } )
      tUsers = get_template('app/usermanagementorg/base_change.html')
      context = Context({ 'users': users,
                          'title': my_title,
                          'user_count': len(users),
                          'group_name': group_name,
                          'target_groups': target_groups,
                          'next': './user_management.html?op=member_change_primary_group' })
      content = tUsers.render(context)
      vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
      vars['submit'] = ''
      return render_to_response('app/base_edit.html', vars)
  else:
    content = get_tabbed_form(tabs, help_form, app_name, f)
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = './user_management.html?op=member_change_primary_group'
    return render_to_response('app/base_edit.html', vars)

