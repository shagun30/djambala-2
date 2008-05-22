# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_show.py

.. zeigt den Inhalt der User-Verwaltung fuer Organisationen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
0.02  21.04.2008  usermanagementorg_group_delete_user
0.03  30.04.2008  usermanagementorg_primary_group_change_user
0.04  02.05.2008  usermanagementorg_member_add_username
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show

from dms.roles          import UserEditPerms
from dms.roles          import require_permission

from dms.usermanagementorg.utils   import get_main_options
from dms.usermanagementorg.views_reset_keyword   import usermanagementorg_reset_keyword
from dms.usermanagementorg.views_members_delete  import usermanagementorg_members_delete
from dms.usermanagementorg.views_member_add_username     import usermanagementorg_member_add_username
from dms.usermanagementorg.views_member_delete_username  import usermanagementorg_member_delete_username
from dms.usermanagementorg.views_member_delete_email     import usermanagementorg_member_delete_email
from dms.usermanagementorg.views_group_new_name          import usermanagementorg_group_new_name
from dms.usermanagementorg.views_group_delete_name       import usermanagementorg_group_delete_name
from dms.usermanagementorg.views_group_insert_user       import usermanagementorg_group_insert_user
from dms.usermanagementorg.views_group_change_user       import usermanagementorg_group_change_user
from dms.usermanagementorg.views_group_delete_user       import usermanagementorg_group_delete_user
from dms.usermanagementorg.views_primary_group_change_user import usermanagementorg_primary_group_change_user

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_show(request, item_container):
  """ zeigt moegliche Optionen zur Community-Verwaltung der Institution """

  app_name = 'usermanagementorg'
  get_data = request.GET.copy()
  if get_data.has_key('op'):
    op = get_data['op']
    if op == 'password_reset':
      return usermanagementorg_reset_keyword(request, item_container)
    elif op == 'member_insert_group':
      return usermanagementorg_group_insert_user(request, item_container)
    elif op == 'member_change_group':
      return usermanagementorg_group_change_user(request, item_container)
    elif op == 'member_delete_user_by_group':
      return usermanagementorg_group_delete_user(request, item_container)
    elif op == 'member_change_primary_group':
      return usermanagementorg_primary_group_change_user(request, item_container)
    elif op == 'members_delete':
      return usermanagementorg_members_delete(request, item_container)
    elif op == 'member_add_username':
      return usermanagementorg_member_add_username(request, item_container)
    elif op == 'member_delete_username':
      return usermanagementorg_member_delete_username(request, item_container)
    elif op == 'member_delete_email':
      return usermanagementorg_member_delete_email(request, item_container)
    elif op == 'member_new_name':
      return usermanagementorg_member_new_name(request, item_container)
    elif op == 'group_name_add':
      return usermanagementorg_group_new_name(request, item_container)
    elif op == 'group_name_delete':
      return usermanagementorg_group_delete_name(request, item_container)

  else:
    user_perms = UserEditPerms(request.user.username, request.path)
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text_more'] = get_main_options(item_container, user_perms.perm_manage_user_new)
    return render_to_response ( 'base-full-width.html', vars )
