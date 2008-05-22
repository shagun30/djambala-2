# -*- coding: utf-8 -*-
"""
/dms/user_folder/views_show.py

.. zeigt den Inhalt eines Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.02.2007  Beginn der Arbeit
0.02  14.02.2007  Rollenzuweisung aendern
0.05  22.02.2007  Gruppen in "eigene Institution"
0.06  19.12.2007  Aufnahme in LDAP-Gruppe
0.07  11.01.2008  CSV-Import
0.08  14.03.2008  get_possible_roles
"""

import string

from django.utils.translation import ugettext as _
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.auth.models      import User
from dms.settings         import LDAP_MODE

from dms.models           import DmsUserUrlRole
from dms.models           import DmsUserOrg
from dms.models           import DmsUserGroup
from dms.models           import DmsGroup
from dms.models           import DmsContainer
from dms.models           import DmsRoles

from dms.queries          import get_user_by_id
from dms.queries          import get_all_roles
from dms.queries          import get_item_container_by_path_and_name
from dms.queries          import get_item_container_by_path
from dms.queries          import get_item_container_by_item_id
from dms.queries          import get_role_by_id

from dms.queries          import get_container_by_id
from dms.queries          import get_item_container_by_id
from dms.queries          import get_role_by_name
from dms.queries          import get_user_by_username
from dms.queries          import get_item_by_id
from dms.queries          import get_role_by_user_path
from dms.queries          import get_userfolder_org_id

from dms.utils            import get_breadcrumb
from dms.utils            import get_footer_email
from dms.roles            import require_permission
from dms.utils_form       import get_folderish_vars_add

from dms.userfolder.utils import get_users
from dms.userfolder.utils import get_users_count
from dms.userfolder.utils import get_actions
from dms.userfolder.utils import get_prev_next_line
from dms.utils_base       import ACL_USERS
from dms.mail             import send_control_new_membership

from dms.encode_decode    import encode_html

# -----------------------------------------------------
@require_permission('perm_manage_user')
def userfolder_show(request, item_container):
  """ zeigt den Inhalt eines Ordners """

  def get_export_csv(users):
    """ liefert die entsprechende CSV-Datei der Mitglieder """
    t = get_template('app/userfolder/base_csv.html')
    parent_id = item_container.parent_item_id
    c = Context({ 'users': users, 'name': get_item_by_id(parent_id).name })
    return t.render(c)

  def do_import(files, container_id):
    """ Mitglieder aus der Datei <filename> importieren """
    content = files['fname']['content']
    lines = string.splitfields(content, '\n')
    for line in lines:
      line = line.strip()
      if line != '':
        username, role = string.splitfields(line, ';')
        try:
          user_id = get_user_by_username(username).id
          role_id = get_role_by_name(role).id
          items = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)
          if len(items) == 0:
            DmsUserUrlRole.save_user_url_role(DmsUserUrlRole(), user_id, container_id, role_id)
          else:
            item = items[0]
            item.role_id = role_id
            item.save()
        except:
          pass

  def delete_items(post, container_id):
    """ """
    keys = post.keys()
    delete_str = 'delete_'
    for k in keys:
      if string.find(k, delete_str) == 0:
        user_id = int(k[len(delete_str):])
        item = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)[0]
        item.delete()
        if LDAP_MODE and item_container.item.integer_1 == 1:
          from dms.auth.auth_ldap import ldap_user_class
          from dms.settings import LDAP_HOST
          from dms.settings import LDAP_PORT
          from dms.settings import LDAP_DN
          from dms.settings import LDAP_AUTH_USER
          from dms.settings import LDAP_AUTH_USER_PASSWORD
          my_ldap = ldap_user_class(LDAP_HOST, LDAP_PORT, LDAP_DN, LDAP_AUTH_USER, LDAP_AUTH_USER_PASSWORD)
          user = get_user_by_id(user_id)
          ic = item_container.get_parent()
          my_ldap.del_user_from_group(user.username, ic.container.path)

  def do_save_user_role(user_id, role_id, container_id, item_container):
    """ speichert die Werte - gegebenenfalls auch in LDAP """
    items = DmsUserUrlRole.objects.filter(user=user_id).filter(container=container_id)
    if len(items) == 0:
      DmsUserUrlRole.save_user_url_role(DmsUserUrlRole(), user_id, container_id, role_id)
    else:
      item = items[0]
      item.role_id = role_id
      item.save()
    # --- Info ueber neuen Bereich
    user = get_user_by_id(user_id)
    role = get_role_by_id(role_id)
    item_container = get_item_container_by_item_id(item_container.parent_item_id)
    send_control_new_membership(item_container, user, role)
    # Lese-Recht als Mindestvoraussetzung fuer den Zugriff auf geschuetzte Dateien
    if LDAP_MODE and item_container.item.integer_1 == 1 \
       and role_id <= get_role_by_name('worker_reader').id:
      from dms.auth.auth_ldap import ldap_user_class
      from dms.settings import LDAP_HOST
      from dms.settings import LDAP_PORT
      from dms.settings import LDAP_DN
      from dms.settings import LDAP_AUTH_USER
      from dms.settings import LDAP_AUTH_USER_PASSWORD
      my_ldap = ldap_user_class(LDAP_HOST, LDAP_PORT, LDAP_DN, LDAP_AUTH_USER, LDAP_AUTH_USER_PASSWORD)
      try:
        my_ldap.add_group(item_container.container.path)
        user = get_user_by_id(user_id)
        ic = item_container.get_parent()
        my_ldap.add_user_to_group(user.username, ic.container.path)
      except:
        pass

  def save_roles(post, container_id):
    """ speichert die entsprechende Rolle fuer den ausgewaehlten User """
    user_id = int(post['user_id'])
    role_id = int(post['role_id'])
    do_save_user_role(user_id, role_id, container_id, item_container)

  def save_user_roles(post, container_id):
    """ speichert die entsprechende Rolle fuer die ausgewaehlten User """
    keys = post.keys()
    user_str = 'user_'
    for k in keys:
      if string.find(k, user_str) == 0:
        user_id = int(k[len(user_str):])
        role_id = int(post['role_id'])
        do_save_user_role(user_id, role_id, container_id, item_container)

  def get_possible_roles(user_id):
    """ gibt die moeglichen Rollen zurueck """
    # --- Rechte des Verwalters
    my_role_id = get_role_by_user_path(request.user, item_container.container.path)
    roles_all = DmsRoles.objects.filter(id__gte=my_role_id)
    roles_all = DmsRoles.objects.filter(id__gte=my_role_id)
    # --- Rechte der betreffenden Person
    if user_id > -1:
      my_user_role = DmsUserUrlRole.objects.filter(user__id=user_id).\
                            filter(container__path=folder_path)
      if len(my_user_role) > 0:
        my_role_id = my_user_role[0].role.id
      else:
        my_role_id = 50
    else:
      my_role_id = 50
    roles = []
    for role in roles_all:
      roles.append({'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'checked': role.id == my_role_id})
    return roles

  def get_user_role_form(user_id, folder_path):
    """ bietet die verfuegbaren Rollen zur Auswahl an """
    roles = get_possible_roles(user_id)
    user = get_user_by_id(user_id)
    t = get_template('app/userfolder/user_role.html')
    user_name = user.get_full_name()
    c = Context({ 'user': user, 'user_name': user_name, 'folder_path': folder_path, 'roles': roles, })
    return t.render(c)

  def get_user_role_add_form(search_last_name, org_id, folder_path):
    """ """
    users = []
    if org_id == 0:
      users = DmsUserUrlRole.objects.select_related(). \
                             filter(user__is_active=True). \
                             filter(user__last_name__istartswith=search_last_name). \
                             exclude(container__path=folder_path). \
                             values('user'). \
                             distinct()
      if users != None and len(users) > 0:
        # Durch die Brust ins Auge
        ids = []
        for u in users:
          ids.append(u['user'])
        s = 'id IN (%s)' % str(ids)[1:-1]
        users = User.objects.extra(where=[s.replace('L','')]).\
                order_by('last_name', 'first_name')
    else:
      users = DmsUserUrlRole.objects.select_related(). \
                             filter(user__is_active=True). \
                             filter(user__last_name__istartswith=search_last_name). \
                             exclude(container__path=folder_path). \
                             extra(tables=['auth_user_org'], 
                                   where=['auth_user_org.user_id=auth_user_url_role.user_id',
                                          'auth_user_org.org_id=%i' % org_id]). \
                             order_by('user__last_name', 'user__first_name')
    user_id = request.user.id
    roles = get_possible_roles(-1)
    t = get_template('app/userfolder/user_role_add.html')
    c = Context({ 'users': users, 'roles': roles, })
    return t.render(c)

  def get_own_institution_form(request, org_id, folder_path):
    """ """
    if org_id == 0:
      return ''
    t = get_template('app/userfolder/manage_own_institution.html')
    groups = DmsGroup.objects.filter(org_id=org_id).order_by('description')
    c = Context({ 'org_id': org_id, 'groups': groups, })
    return t.render(c)

  def get_user_group_role_add_form(group_id, org_id, folder_path):
    """ """
    usergroups = []
    if group_id >= 0:
      usergroups = DmsUserGroup.objects.select_related().filter(group__id=group_id).\
                          order_by('user__last_name')
    else:
      usergroups = DmsUserOrg.objects.select_related().filter(org_id=org_id).\
                          order_by('user__last_name')
    roles_all = DmsRoles.objects.all()
    roles = []
    for role in roles_all:
      roles.append({'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'checked': 'no_rights' })
    t = get_template('app/userfolder/user_group_role_add.html')
    c = Context({ 'usergroups': usergroups, 'roles': roles, 'org_id': org_id, })
    return t.render(c)

  def get_all_members_form(org_id, folder_path):
    """ """
    t = get_template('app/userfolder/manage_all_members.html')
    c = Context()
    return t.render(c)

  def get_import_members_form(org_id, folder_path):
    """ """
    t = get_template('app/userfolder/manage_import_members.html')
    c = Context()
    return t.render(c)

  def get_export_members_form(org_id, folder_path):
    """ """
    t = get_template('app/userfolder/manage_export_members.html')
    c = Context()
    return t.render(c)

  def get_search_members_form(org_id, folder_path):
    """ """
    t = get_template('app/userfolder/manage_search_members.html')
    c = Context()
    return t.render(c)

  my_item = item_container.item
  app_name = 'userfolder'
  my_title = _(u'Zugangsberechtigungen für Community-Mitglieder')
  folder_path = item_container.container.path[:string.find(item_container.container.path,ACL_USERS)]
  container = DmsContainer.objects.filter(path=folder_path)[0]
  container_id = container.id
  try:
    user_perms = UserEditPerms(request.user.username,request.path)
  except:
    user_perms = []
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    order = 'last_name'
  if request.GET.has_key('start') :
    start = int(request.GET['start'])
    diff  = int(request.GET['diff'])
  else :
    start = 0
    diff  = 200
  count = get_users_count(item_container)
  users = get_users(item_container, order, start, diff)
  # --- Rollenzuweisung aendern
  if request.GET.has_key('edit_user'):
    user_id = int(request.GET['edit_user'])
    edit_user_role = get_user_role_form(user_id, folder_path)
  else :
    if request.POST.has_key('edit_user') and request.POST.has_key('submit'):
      save_roles(request.POST.copy(), container_id)
    edit_user_role = ''
  add_user_role = ''
  # --- gezielte Suche ueber Zugangsnamen
  if request.POST.has_key('search_name'):
    items = User.objects.filter(username=request.POST['search_name'])
    if len(items) > 0:
      user_id = items[0].id
      edit_user_role = get_user_role_form(user_id, folder_path)
  # --- komplette Community (via Nachname)
  if request.POST.has_key('search_last_name'):
    org_id = int(request.POST['org_id'])
    name = encode_html(request.POST['search_last_name'])
    add_user_role = get_user_role_add_form(name, org_id, folder_path)
    my_title = _(u'Community-Mitglieder in diesen Bereich eintragen')
  elif request.POST.has_key('mode'):
    if request.POST['mode'] == 'import':
      do_import(request.FILES, container_id)
    else:
      users = get_users(item_container, order, 0, 5000)
      add_user_role = get_export_csv(users)
  elif request.GET.has_key('org_id') and request.GET.has_key('inst_group'):
    org_id = int(request.GET['org_id'])
    group_id = int(request.GET['inst_group'])
    add_user_role = get_user_group_role_add_form(group_id, org_id, folder_path)
    if group_id >= 0:
      group = DmsGroup.objects.filter(id=group_id)[0]
      my_title = _(u"Community-Mitglieder der Gruppe '%s' in diesen Bereich eintragen") % \
                  group.description
    else:
      my_title = _(u"Community-Mitglieder in diesen Bereich eintragen")
  elif request.POST.has_key('edit_users') and request.POST.has_key('submit'):
      save_user_roles(request.POST.copy(), container_id)
      add_user_role = ''
  # --- Mitglieder loeschen
  elif request.has_key('modus_delete'):
    delete_items(request.POST.copy(), container_id)
  prev_next = get_prev_next_line(item_container, start, diff, count)
  userfolder_org_id = get_userfolder_org_id(item_container)
  vars = { 'content_div_style': 'frame-main-manage',
           'users'            : users,
           'user_count'       : count,
           'prev_next'        : prev_next,
           'site'             : item_container.container.site,
           'title'            : my_title,
           'slot_right_info'  : my_item.info_slot_right,
           'action'           : get_actions(request, user_perms, item_container),
           'breadcrumb'       : get_breadcrumb(item_container),
           'path'             : item_container.container.path,
           'edit_user_role'   : edit_user_role,
           'own_institution'  : get_own_institution_form(request, userfolder_org_id,
                                        item_container.container.path),
           'all_members'      : get_all_members_form(userfolder_org_id, item_container.container.path),
           'import_members'   : get_import_members_form(userfolder_org_id, item_container.container.path),
           'export_members'   : get_export_members_form(userfolder_org_id, item_container.container.path),
           'search_members'   : get_search_members_form(userfolder_org_id, item_container.container.path),
           'add_user_role'    : add_user_role,
           'footer_email'     : get_footer_email(my_item),
           'no_top_main_navigation': True,
           'last_modified'    : item_container.get_last_modified(),
         }
  return render_to_response('app/userfolder/base.html', vars)