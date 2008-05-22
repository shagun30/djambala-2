# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/schools.py

.. zeigt die Inhalte der Fortbildungsdatenbank an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.02.2008  Beginn der Arbeit
0.05  27.02.2008  Auswahl der Schule
"""

from django.template.loader import get_template
from django.template    import Context
from django             import newforms as forms
from django.shortcuts   import render_to_response
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.utils          import get_tabbed_form

from dms.hessen.schooldb.queries      import get_schulen_by_ort
from dms.hessen.trainingdb.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def views_schulen(request, item_container, op):
  """ waehlt die entsprechende Schule aus """

  def get_schulen(app_name):
    """ Suchformular fuer Auswahl der Schule """
    class dms_itemForm(forms.Form):
      """ Elemente des Eingabeformulars """
      school_ort = forms.CharField(max_length=60,
                            widget=forms.TextInput(attrs={'size':40}) )
    data_init = {}
    data = data_init
    f = dms_itemForm(data)
    tabs = [('tab_schule2' , ['school_ort', ]),]
    return get_tabbed_form(tabs, help_form, app_name, f)

  app_name = 'training_db'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['content_div_style'] = 'frame-util-images'
  vars['no_breadcrumb'] = True
  if request.POST.has_key('school_ort') and request.POST['school_ort'] != '':
    schools = get_schulen_by_ort(request.POST['school_ort'])
    schulen = []
    for school in schools:
      schulen.append({ 'name': school[1].NameSchule, 'no': school[1].Schul_Nr,
                       'ort': school[0].Ort, 'telefon': school[0].Tel1 })
    vars['schulen'] = schulen
  else:
    vars['schul_form'] = get_schulen(app_name)
  vars['submit'] = _(u'Schule auswählen')
  return render_to_response ( 'app/hessen/trainingdb/select_schule.html', vars )

