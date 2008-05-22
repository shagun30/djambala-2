# -*- coding: utf-8 -*-
"""
/dms/imagethumb/views_add.py

.. enthaelt den View zum Ergaenzen eines Minibildes
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  22.03.2007  Beginn der Arbeit
"""

import os

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.settings       import DOWNLOAD_PATH
from dms.utils          import get_tabbed_form
from dms.utils          import check_name
from dms.utils          import check_name
from dms.utils_form     import get_item_vars_add

from dms.queries        import exist_item
from dms.queries        import save_item_values

from dms.imagethumb.utils     import do_resize
from dms.image.utils          import get_image_size
from dms.imagethumb.help_form import help_form

from dms.views_error    import show_error_object_exist
from dms.views_error    import show_error_object_exist

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_add')
def imagethumb_add(request, item_container):
  """ neue Infoseite anlegen """

  def save_values(new, files, my_folder, name):
    """ """
    content = files['fname']['content']
    content_type = files['fname']['content-type']
    content = do_resize(content, content_type, new['max_width'], new['max_height'])
    filename = files['fname']['filename']
    file_path = DOWNLOAD_PATH + my_folder.container.path
    file_name = file_path + name
    try:
      os.makedirs(file_path)
    except:
      pass
    os.chmod(file_path, 0750)
    f = open(file_name, 'wb')
    f.write(content)
    f.close()
    os.chmod(file_name, 0660)
    width, height = get_image_size(file_name)
    new['title'] = name
    new['is_browseable'] = False
    new['integer_1'] = width
    new['integer_2'] = height
    new['section'] = ''
    save_item_values(request.user, 'dmsImagethumb', name, new, my_folder, new['is_browseable'])

  class DmsItemForm ( forms.Form ) :
    fname       = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    if request.method == 'GET' and request.GET.has_key('max_width'):
      max_width   = forms.IntegerField(min_value=30, max_value=400,
                        widget=forms.HiddenInput() )
    else :
      max_width   = forms.IntegerField(min_value=30, max_value=400,
                        widget=forms.TextInput(attrs={'size':5}) )
    if request.method == 'GET' and request.GET.has_key('max_height'):
      max_height  = forms.IntegerField(min_value=30, max_value=600,
                        widget=forms.HiddenInput() )
    else :
      max_height  = forms.IntegerField(min_value=30, max_value=600,
                        widget=forms.TextInput(attrs={'size':5}) )

  app_name = 'imagethumb'
  my_title = _(u'Minibild anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  elif request.method == 'GET' and request.GET.has_key('max_width') and request.GET.has_key('max_height'):
    data = { 'max_width': request.GET['max_width'], 'max_height': request.GET['max_height'], }
  else :
    data = { 'max_width': 120, 'max_height': 40, }
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [ ('tab_base', [ 'fname', 'max_width', 'max_height', ]), ]

  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    # --- Umlaute aus Namen entfernen
    name = check_name(request.FILES['fname']['filename'], True)
    if not exist_item(item_container, name):
      save_values(f.data, request.FILES, item_container, name)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else :
      return show_error_object_exist(request, item_container, name)
  else :
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    return render_to_response ( 'app/file/manage_edit.html', vars )
