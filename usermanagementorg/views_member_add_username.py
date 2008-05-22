# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_member_add_username.py

.. erzeugt einen einzelnen User inerhalb der Instituution
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
"""

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
from dms.queries        import get_user_by_email
from dms.queries        import set_user_org

from dms.roles          import require_permission
from dms.mail           import send_password
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.userregistration.utils       import get_sex_choices
from dms.usermanagementorg.utils      import get_groups
from dms.usermanagementorg.utils      import generate_passwd
from dms.usermanagementorg.utils      import create_member

from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_member_add_username(request, item_container):
  """ nimmt User in Comunity auf und ergaenzt sie/ihn bei einer Basisgruppe """

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
    sex        = forms.ChoiceField(choices=get_sex_choices(), widget=forms.RadioSelect() )
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'size':30}) )
    last_name  = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'size':30}) )
    title_name = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={'size':10}) )
    email      = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':50}) )
    group_names_primary = forms.ChoiceField(choices=get_group_names(org_id, True), widget=forms.RadioSelect() )
    group_names = forms.MultipleChoiceField(required=False, choices=get_group_names(org_id, False),
                            widget=forms.CheckboxSelectMultiple() )

  app_name = 'usermanagementorg'
  my_title = _(u'Mitglied aufnehmen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_member_user_insert', [ 'sex', 'first_name', 'last_name', 'title_name', 'email', 
                                        'group_names_primary', 'group_names', ]) ]
  if request.method == 'POST' and not f.errors:
    data = f.cleaned_data
    create_member(org_id, data['group_names_primary'], data['group_names'],
                  data['sex'], data['first_name'], data['last_name'], data['title_name'],
                  data['email'])
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else:
    content = get_tabbed_form(tabs, help_form, app_name, f)
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = './user_management.html?op=member_add_username'
    vars['is_file_form'] = True
    return render_to_response('app/base_edit.html', vars)

