# -*- coding: utf-8 -*-
"""
/dms/survey/views_reset.py

.. enthaelt den View zum Loeschen aller Daten des Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.01.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.utils.translation import ugettext as _

from dms.roles            import *

from dms.queries          import get_site_url
from dms.utils            import get_tabbed_form
from dms.utils_form       import get_folderish_vars_edit

from dms.survey.queries   import delete_complete

from dms.survey.help_form import help_form
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def survey_reset(request, item_container):
  """ Ergebnisse des Fragebogens komplett loeschen """

  def get_delete_choices():
    """ """
    ret = []
    ret.append( (1, _(u'Bisherige Eingaben wirklich löschen')) )
    ret.append( (0, _(u'Eingabedaten unverändert lassen')) )
    return ret

  def save_values(item_container, new):
    """ Daten komplett loeschen """
    if new['integer_3'] == u'1':
      delete_complete(item_container)

  class dms_itemForm(forms.Form):
    integer_3 = forms.ChoiceField(required=False, choices=get_delete_choices(), widget=forms.RadioSelect() )

  app_name = 'survey'
  my_title = _(u'Fragebogendaten komplett löschen')

  if request.method == 'POST':
    data = request.POST.copy ()
  else :
    data = { 'integer_3': 0, }
  f = dms_itemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte // Sonderfall: Startseite
  tabs = [ ('tab_reset', ['integer_3', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else:
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
