# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_group_insert_user.py

.. loescht User mit dem entsprechenden User-Namen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.04.2008  Beginn der Arbeit
0.02  24.04.2008  E-Mail versenden
0.03  30.04.2008  target_group_ids
"""

import string
import datetime
import random

from django.db          import transaction
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.utils.safestring  import mark_safe
from django.template.loader import get_template
from django.template    import Context

from django.utils.translation import ugettext as _

from dms.auth.models    import User

from dms.queries        import get_site_url
from dms.queries        import delete_user_by_username
from dms.queries        import get_userfolder_org_id
from dms.queries        import delete_group_by_id
from dms.queries        import delete_users_in_group
from dms.queries        import get_users_by_org_id
from dms.queries        import get_users_by_group_id
from dms.queries        import get_group_by_id
from dms.queries        import get_user_by_email
from dms.queries        import set_user_org
from dms.queries        import set_user_group

from dms.roles          import require_permission
from dms.mail           import send_password
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.userregistration.utils       import get_username
from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.utils      import create_member
from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def create_members(org_id, group_id, target_group_ids, fcontent):
  """ legt mehrere User fuer org_id an und ordnet sie der group_id zu """
  lines = string.splitfields(fcontent)
  for line in lines:
    if line.find('@') > 0:
      line = line.replace('"', '')
      items = string.splitfields(line.strip(), ';')
      if len(items) == 4:
        sex = items[0].strip()
        first_name = items[1].strip()
        last_name = items[2].strip()
        email = items[3].strip()
        title = ''
      elif len(items) == 5:
        sex = items[0].strip()
        title = items[1].strip()
        first_name = items[2].strip()
        last_name = items[3].strip()
        email = items[4].strip()
      elif len(items) == 6:
        sex = items[1].strip()
        title = items[2].strip()
        first_name = items[3].strip()
        last_name = items[4].strip()
        email = items[5].strip()
      create_member(org_id, group_id, target_group_ids, sex, first_name, last_name, title_name, email)

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_group_insert_user(request, item_container):
  """ nimmt User in Comunity auf und ergaenzt sie bei einer Basisgruppe """

  org_id = get_userfolder_org_id(item_container)

  def get_group_list(org_id):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    tList = get_template('app/usermanagementorg/group_list.html')
    groups = get_groups(org_id, True)
    return tList.render(Context({ 'groups': groups, }))

  def get_group_names(org_id, primary_mode):
    """ liefert die vorhandenen Gruppen der Organisation org_id """
    groups = get_groups(org_id)
    ret = []
    for group in groups:
      if ( primary_mode and group['is_primary'] ) or \
         ( not primary_mode and not group['is_primary'] ) :
        ret.append((group['id'], group['description']))
    return ret

  group_items = get_group_list(org_id)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    group_names_primary = forms.ChoiceField(choices=get_group_names(org_id, True), widget=forms.RadioSelect() )
    group_names = forms.MultipleChoiceField(required=False, choices=get_group_names(org_id, False),
                            widget=forms.CheckboxSelectMultiple() )
    fname = forms.CharField(required=False, max_length=200,
                  widget=forms.FileInput(attrs={'size':40}) )

  app_name = 'usermanagementorg'
  my_title = _(u'Mitglieder aufnehmen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_group_user_insert', [ 'group_names_primary', 'group_names', 'fname' ]) ]
  if request.method == 'POST' and not f.errors:
    data = f.cleaned_data
    create_members(org_id, data['group_names_primary'], data['group_names'],
                   request.FILES['fname']['content'])
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else:
    content = get_tabbed_form(tabs, help_form, app_name, f)
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = './user_management.html?op=member_insert_group'
    vars['is_file_form'] = True
    return render_to_response('app/base_edit.html', vars)

