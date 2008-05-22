# -*- coding: utf-8 -*-
"""
/dms/userchangemanagement/views_show.py

.. zeigt den Inhalt der User-Verwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  21.06.2007  Beginn der Arbeit
0.02  23.06.2007  Integration der Formulare
"""

from dms.auth.decorators    import login_required
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.newforms.util import ValidationError

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils_form     import get_item_vars_edit

from dms.userchangemanagement.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@login_required
def userchangemanagement_show(request, item_container):
  """ zeigt die moeglichen Optionen zur Community-Verwaltung """
  def save_values(new, user):
    user.email = new['email']
    password = new['password1']
    if password != '':
      user.set_password(password)
    user.save()

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    email      = forms.EmailField(
                       widget=forms.TextInput(attrs={'size':60}) )
    password1  = forms.CharField(required=False,
                       widget=forms.PasswordInput(attrs={'size':30}) )
    password2  = forms.CharField(required=False,
                       widget=forms.PasswordInput(attrs={'size':30}) )
    def clean_password2(self):
      if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise ValidationError(_(u'Die beiden eingegebenen Kennwörter stimmen nicht überein!'))
      elif self.cleaned_data['password1'] != '' and len(self.cleaned_data['password2']) < 6:
        raise ValidationError(_(u'Das Kennwort muss mindestens sechs Zeichen lang sein!'))
      else:
        return self.cleaned_data['password2']

  app_name = 'userchangemanagement'
  my_title = _(u'Eigene Daten ändern')
  user = request.user
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else :
    data = {'email': user.email, 'password1': '', 'password2': ''}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  tabs = [ ('tab_email', [ 'email', ]),
           ('tab_password', [ 'password1', 'password2' ])
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method == 'POST' and not f.errors:
    save_values(f.data, user)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response('app/base_edit.html', vars)
