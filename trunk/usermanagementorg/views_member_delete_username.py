# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_delete_username.py

.. loescht User mit dem entsprechenden User-Namen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
0.02  02.05.2008  delete_member_username
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import delete_user_by_username
from dms.queries        import get_user_by_username
from dms.queries        import get_org_id
from dms.queries        import get_userfolder_org_id

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_member_delete_username(request, item_container):
  """ loescht Community-Mitglied ueber Usernamen """

  def delete_member_username(data):
    """ loescht das betreffende Community-Mitglied data['username'] """
    if data.has_key('username'):
      user_name = data['username']
      user = get_user_by_username(user_name)
      # --- Nur Mitglieder der eigenen Organisation duerfen geloescht werden
      if get_userfolder_org_id(item_container) == get_org_id(user):
        delete_user_by_username(user_name)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    username    = forms.CharField(max_length=40,
                       widget=forms.TextInput(attrs={'size':30}) )

  app_name = 'usermanagementorg'
  my_title = _(u'Community-Mitglied über Zugangsnamen löschen')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'username': '', }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_username', [ 'username', ]) ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  if request.method == 'POST':
    post_data = request.POST.copy()
    delete_member_username(post_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = './user_management.html?op=member_delete_username'
    return render_to_response('app/base_edit.html', vars)
