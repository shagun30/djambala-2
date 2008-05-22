# -*- coding: utf-8 -*-
"""
/dms/usermanagement/views_members_accept.py

.. schaltet die/den entsprechenden User frei
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

from dms.queries        import get_user_not_active
from dms.queries        import get_site_url
from dms.queries        import get_org_by_username
from dms.queries        import set_user_active

from dms.roles          import require_permission

from dms.utils_form     import get_base_vars

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagement_members_accept(request, item_container):
  """ schaltet Personen fuer Community frei """

  def save_members_accept_values(post_data):
    for data in post_data:
      if data.startswith('item_'):
        user_id = int(data[len('item_'):])
        user = set_user_active(user_id, True)

  not_actives = get_user_not_active()
  objs = []
  for o in not_actives:
    p = {}
    p['id'] = o.id
    p['email'] = o.email
    p['date_joined'] = o.date_joined.strftime('%m/%d/%Y')
    p['name'] = o.get_standard_name()
    org = get_org_by_username(o.username)
    if org != None:
      p['org'] = u'%s<br />%s<br />%s %s' % (org.organisation, org.street, org.zip, org.town)
    else:
      p['org'] = _(u'unbekannte Organisation')
    objs.append(p)

  app_name = 'usermanagement'
  my_title = _(u'Community-Mitglieder freischalten')
  if request.method == 'POST':
    post_data = request.POST.copy()
    save_members_accept_values(post_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html?op=members_accept'))
  else:
    vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage')
    v = { 'objs'  : objs,
          'title' : my_title,
          'action': '',
          'next'  : './user_management.html?op=members_accept',
          'submit': _(u'Community-Mitglieder freischalten ...')
        }
    vars.update(v)
    return render_to_response ( 'app/usermanagement/manage_members_accept.html', vars )
