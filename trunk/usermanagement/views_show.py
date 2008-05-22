# -*- coding: utf-8 -*-
"""
/dms/usermanagement/views_show.py

.. zeigt den Inhalt der User-Verwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  06.02.2007  Beginn der Arbeit
0.02  21.06.2007  Wiederaufnahme der Arbeit
0.03  28.06.2007  Eingangsmenue
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show

from dms.roles          import UserEditPerms
from dms.roles          import require_permission

from dms.usermanagement.utils   import get_main_options
from dms.usermanagement.views_reset_keyword   import usermanagement_reset_keyword
from dms.usermanagement.views_members_accept  import usermanagement_members_accept
from dms.usermanagement.views_members_delete  import usermanagement_members_delete
from dms.usermanagement.views_member_new_email  import usermanagement_member_new_email
from dms.usermanagement.views_member_new_org    import usermanagement_member_new_org
from dms.usermanagement.views_member_new_name   import usermanagement_member_new_name
from dms.usermanagement.views_member_delete_username  import usermanagement_member_delete_username
from dms.usermanagement.views_member_delete_email     import usermanagement_member_delete_email

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagement_show(request, item_container):
  """ zeigt moegliche Optionen zur Community-Verwaltung """

  app_name = 'usermanagement'
  get_data = request.GET.copy()
  if get_data.has_key('op'):
    op = get_data['op']
    if op == 'password_reset':
      return usermanagement_reset_keyword(request, item_container)
    elif op == 'members_accept':
      return usermanagement_members_accept(request, item_container)
    elif op == 'members_delete':
      return usermanagement_members_delete(request, item_container)
    elif op == 'member_new_email':
      return usermanagement_member_new_email(request, item_container)
    elif op == 'member_new_org':
      return usermanagement_member_new_org(request, item_container)
    elif op == 'member_delete_username':
      return usermanagement_member_delete_username(request, item_container)
    elif op == 'member_delete_email':
      return usermanagement_member_delete_email(request, item_container)
    elif op == 'member_new_name':
      return usermanagement_member_new_name(request, item_container)
  else:
    user_perms = UserEditPerms(request.user.username, request.path)
    vars = get_item_vars_show(request, item_container, app_name)
    vars['text_more'] = get_main_options(item_container, user_perms.perm_manage_user_new and \
                                        item_container.container.site.org_id==0)
    return render_to_response ( 'base-full-width.html', vars )
