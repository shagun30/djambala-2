# -*- coding: utf-8 -*-
"""
/dms/usermanagement/views_reset_keyword.py

.. setzt das Kennwort zurueck
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.06.2007  Beginn der Arbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_older_user_not_active
from dms.queries        import get_site_url
from dms.queries        import get_org_by_username
from dms.queries        import delete_user

from dms.roles          import require_permission

from dms.utils_form     import get_base_vars

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user')
def usermanagement_members_delete(request, item_container):
  """ loescht Registrierungen, die aelter sind als 30 Tage """

  def delete_members(post_data):
    for data in post_data:
      if data.startswith('item_'):
        user_id = int(data[len('item_'):])
        user = delete_user(user_id)

  not_actives = get_older_user_not_active(30)
  objs = []
  for o in not_actives:
    p = {}
    p['id'] = o.id
    p['email'] = o.email
    p['date_joined'] = o.date_joined.strftime('%m/%d/%Y')
    p['name'] = o.get_full_name()
    org = get_org_by_username(o.username)
    if org != None:
      p['org'] = u'%s<br />%s<br />%s %s' % (org.organisation, org.street, org.zip, org.town)
    else:
      p['org'] = _(u'unbekannte Organisation')
    objs.append(p)

  app_name = 'usermanagement'
  my_title = _(u'Nicht-registrierte Community-Mitglieder löschen')
  if request.method == 'POST':
    post_data = request.POST.copy()
    delete_members(post_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage')
    v = { 'objs'  : objs,
          'title' : my_title,
          'action': '',
          'next'  : './user_management.html?op=members_delete',
          'submit': _(u'Nicht-registrierte Community-Mtglieder löschen ...')
        }
    vars.update(v)
    return render_to_response ( 'app/usermanagement/manage_members_accept.html', vars )
