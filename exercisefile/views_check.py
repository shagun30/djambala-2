# -*- coding: utf-8 -*-
"""
/dms/exercisefile/views_check.py

.. enthaelt den View zur Bewertung der Loesung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.05.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import *
from dms.models         import DmsItem
from dms.queries        import get_site_url

from dms.settings       import DOWNLOAD_PATH
from dms.utils          import get_tabbed_form
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils          import get_license_choices
from dms.utils_form     import get_item_vars_edit

from dms.exercise.utils import get_points, get_points_min_max

from dms.file.utils     import save_file
from dms.exercisefile.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def exercisefile_check(request, item_container):
  """ Bewertung der Loesung vornehmen """

  def get_top_of_page(item_container):
    """ erzeugt den Notenspiegel """
    from django.template.loader import get_template
    from django.template import Context
    tPoints = get_template('app/exercise/points.html')
    headers = [1,2,3,4,5,6]
    points = get_points(item_container.get_parent())
    points = get_points_min_max(points)
    return tPoints.render(Context ({'headers': headers,
                                    'points': points,
                                    'max_points': item_container.get_parent().item.integer_1 }))

  @transaction.commit_manually
  def save_values(item_container, old, new, files):
    """ """
    new['integer_1'] = int(100.0*float(new['integer_1']))
    if not new.has_key('text'):
      new['text'] = item_container.item.text
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

  class DmsItemForm(forms.Form):
    text      = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    text_more = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':10, 'cols':60, 'id':'ta1', 'style':'width:100%;'}) )
    integer_1 = forms.FloatField(min_value=0.0, max_value=item_container.get_parent().item.integer_1,
                      widget=forms.TextInput(attrs={'size':5}) )

  data_init = {
                'text': remove_link_icons(item_container.item.text),
                'text_more': remove_link_icons(item_container.item.text_more),
                'integer_1': item_container.item.integer_1/100.0,
              }
  app_name = 'file'
  my_title = _(u'Lösung bewerten')
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  if item_container.item.text.strip() != '':
    tabs = [ ( 'tab_check'    , [ 'text', 'text_more', 'integer_1' ] ), ]
  else:
    tabs = [ ( 'tab_check'    , [ 'text_more', 'integer_1' ] ), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data, request.FILES)
    return HttpResponseRedirect(item_container.get_parent().get_absolute_url())
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text_intro'] = get_top_of_page(item_container)
    return render_to_response ( 'app/file/manage_edit.html', vars )
