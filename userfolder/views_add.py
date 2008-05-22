# -*- coding: utf-8 -*-
"""
/dms/user_folder/views_add.py

.. enthaelt den View zurm Ergaenzen eines Ordners
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.01.2007  Beginn der Arbeit
0.02  23.01.2007  ACL_USERS
0.03  18.12.2007  new['integer_1'] = ...
"""

from django.db              import transaction
from django.http            import HttpResponse, HttpResponseRedirect
from django                 import newforms as forms

from django.utils.translation import ugettext as _

from.dms.settings           import LDAP_MODE
from dms.queries            import exist_item
from dms.queries            import get_site_url
from dms.queries            import save_container_values
from dms.queries            import do_protect_folder

from dms.views_error        import show_error_object_exist
from dms.roles              import require_permission

from dms.utils_base         import ACL_USERS

# -----------------------------------------------------
@require_permission('perm_manage_user')
def userfolder_add(request, item_container):
  """ neuen User-Folder anlegen """

  @transaction.commit_manually
  def save_values(item_container):
    """ """
    new = {}
    new['title'] = _(u'User-Verwaltung')
    new['nav_title'] = _(u'Zugänge')
    new['is_browseable'] = False
    new['min_role_id'] = 2000  # muss immer abgefragt werden koennen
    acl_item_container = save_container_values(request.user, 'dmsUserFolder', ACL_USERS,
                                               new, item_container)
    do_protect_folder(item_container, acl_item_container, False)
    transaction.commit()

  if not exist_item(item_container, ACL_USERS):
    save_values(item_container)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html/manage/'))
  else :
    return show_error_object_exist(request, item_container, ACL_USERS)
