# -*- coding: utf-8 -*-
"""
/dms/usermanagement/views_member_new_org.py

.. weist den entsprechenden User einer neuen Organisation zu
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.06.2007  Beginn der Arbeit
0.02  06.12.2007  Weiterarbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.template.loader import get_template
from django.template import Context

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.queries        import get_site_url
from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.usermanagement.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagement_member_new_org(request, item_container):
  """ legt neue Dienststelle fest """

  def change_org(data):
    """ setzt fuer das Community-Mitglied data['username'] ein neues Kennwort """
    if data.has_key('username'):
      dummy = 1

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    username    = forms.CharField(max_length=40,
                       widget=forms.TextInput(attrs={'size':30}) )
    org_name    = forms.CharField(max_length=80,
                       widget=forms.TextInput(attrs={'size':50}) )

  app_name = 'usermanagement'
  my_title = _(u'Dienststelle eines Community-Mitglieds ändern')
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'username': '', }
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_username', [ 'username', 'org_name']) ]
  content = get_tabbed_form(tabs, help_form, app_name, f)
  if request.method == 'POST':
    post_data = request.POST.copy()
    change_org(post_data)
    return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = item_container.get_absolute_url() + '?op=member_new_org'
    ajax_url = get_site_url(item_container, item_container.item.name + '/ajax/usermanagement_ajax_get_org/')
    t_org = get_template('app/usermanagement/ajax_get_org.html')
    vars['ajax'] = t_org.render(Context({ 'ajax_url': ajax_url, }))
    return render_to_response('app/base_edit.html', vars)
