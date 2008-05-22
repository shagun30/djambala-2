# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_group_delete_user.py

.. loescht User mit dem entsprechenden User-Namen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.04.2008  Beginn der Arbeit
0.02  24.04.2008  Liste der geloeschten User anzeigen
0.03  30.04.2008  delete_user
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
from dms.queries        import get_users_by_org_id
from dms.queries        import get_users_by_group_id
from dms.queries        import get_group_by_id
from dms.queries        import get_user_by_id
from dms.queries        import delete_user

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import clean_data
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_group_delete_user(request, item_container):
  """ loescht User einer Gruppe """

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
    ret.append((-1, _(u'Alle Mitglieder')))
    for group in groups:
      ret.append((group['id'], group['description']))
    return ret

  group_items = get_group_list(org_id)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    group_names = forms.ChoiceField(choices=get_group_names(org_id), widget=forms.RadioSelect() )

  app_name = 'usermanagementorg'
  my_title = _(u'Mitglieder löschen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_group_user_delete', [ 'group_names', ]) ]
  if request.method == 'POST':
    # --- User zum Loeschen anbieten
    if request.POST.has_key('group_names'):
      this_group = int(request.POST['group_names'])
      if this_group == -1:
        group_name = _(u'alle Mitglieder')
        group_users = get_users_by_org_id(org_id)
      else:
        group_name = get_group_by_id(this_group).description
        group_users = get_users_by_group_id(this_group)
      users = []
      for u in group_users:
        users.append( {'name': u.user.get_standard_name(), 'username': u.user.username,
                       'email': u.user.email, 'id': u.user.id} )
      tUsers = get_template('app/usermanagementorg/base_delete.html')
      context = Context({ 'users': users, 'title': my_title, 
                          'user_count': len(users), 'group_name': group_name,
                          'next': './user_management.html?op=member_delete_user_by_group' })
      content = tUsers.render(context)
      vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
      vars['submit'] = ''
      return render_to_response('app/base_edit.html', vars)
    else:
      data = clean_data(f.data)
      users = []
      if data.has_key('delete_id'):
        ids = data['delete_id']
        for id in ids:
          user = get_user_by_id(id)
          users.append({'name': user.get_standard_name(),})
          delete_user(id)
      tUsers = get_template('app/usermanagementorg/deleted_users.html')
      context = Context({ 'users': users,
                          'next': './user_management.html?op=member_delete_user_by_group' })
      content = tUsers.render(context)
      vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
      vars['submit'] = ''
      return render_to_response('app/base_edit.html', vars)
      return HttpResponseRedirect(get_site_url(item_container, 'user_management.html?op=member_delete_user_by_group'))
  else:
    content = get_tabbed_form(tabs, help_form, app_name, f)
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = './user_management.html?op=member_delete_user_by_group'
    return render_to_response('app/base_edit.html', vars)

