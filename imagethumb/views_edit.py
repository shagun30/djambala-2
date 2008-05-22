# -*- coding: utf-8 -*-
"""
/dms/imagethumb/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften eines Minibildes
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit - Daten kommen aus Datenbank
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.roles          import require_permission
from dms.utils_form     import get_item_vars_edit

from dms.imagethumb.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def imagethumb_edit(request, item_container):
  """ Eigenschaften des Bildes aendern """

  def save_values(item_container, old, new, files):
    """ """
    if files != {}:
      filename = files['fname']['filename']
      # --- nur Bilder/Dateien gleichen Namens werden ersetzt!!!
      if filename == item_container.item.name:
        content = files['fname']['content']
        content_type = files['fname']['content-type']
        file_path = DOWNLOAD_PATH + my_folder.path
        file_name = file_path + filename
        f = open(file_name, 'wb')
        f.write(content)
        f.close()
        width, height = get_image_size(file_name)
        new['integer_1'] = width
        new['integer_2'] = height
    item_container.item.save_values(old, new)

  class DmsItemForm(forms.Form):
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    max_width   = forms.IntegerField(min_value=16, max_value=400,
                       widget=forms.TextInput(attrs={'size':5}) )
    max_height  = forms.IntegerField(min_value=10, max_value=600,
                       widget=forms.TextInput(attrs={'size':5}) )

  data_init = { 'max_width': item_container.item.integer_1,
                'max_height': item_container.item.integer_2,
              }

  app_name = 'imagethumb'
  my_title = _(u'Minibild ändern')
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ('tab_base',   [ 'max_width', 'max_height', ]),
           ('tab_update', [ 'fname', ]),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data, request.FILES)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
