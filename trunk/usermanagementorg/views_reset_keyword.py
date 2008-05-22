# -*- coding: utf-8 -*-
"""
/dms/usermanagementorg/views_reset_keyword.py

.. setzt das Kennwort zurueck
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.auth.models    import User

from dms.roles          import require_permission
from dms.queries        import get_user_by_username

from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_add

from dms.usermanagementorg.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_reset_keyword(request, item_container):
  """ setzt das Kennwort zurueck """

  def reset_password(data):
    """ setzt fuer das Community-Mitglied data['username'] ein neues Kennwort """
    if data.has_key('username'):
      user = get_user_by_username(data['username'])
      if user != None:
        # PROBLEM: Schueler oder Community-Mitglieder ohne E-Mail-Adresse
        if user.email != '':
          # neues Kennwort erzeugen
          new_password = User.objects.make_random_password()
          user.set_password(new_password)
          user.save()
          # neues Kennwort per E-Mail versenden

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    username    = forms.CharField(max_length=40,
                       widget=forms.TextInput(attrs={'size':30}) )

  app_name = 'usermanagementorg'
  my_title = _(u'Kennwort eines Community-Mitglieds ändern')
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
    reset_password(post_data)
    return HttpResponseRedirect(item_container.get_absolute_url())
    #return HttpResponseRedirect(get_site_url(item_container, 'user_management.html'))
  else:
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['next'] = item_container.get_absolute_url() + '?op=password_reset'
    return render_to_response('app/base_edit.html', vars)
