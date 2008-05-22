# -*- coding: utf-8 -*-
"""
/dms/exercisefile/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften einer Aufgabendatei
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  07.05.2008  Beginn der Arbeit
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

from dms.encode_decode  import decode_html

from dms.file.utils     import save_file
from dms.exercisefile.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def exercisefile_edit(request, item_container):
  """ Eigenschaften der Datei aendern """

  @transaction.commit_manually
  def save_values(item_container, old, new, files):
    """ """
    if files != {}:
      filename = files['fname']['filename']
      # --- Dateien gleichen Namens werden ersetzt
      if filename == item_container.item.name:
        save_file(filename, files, item_container)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

  class DmsItemForm(forms.Form):
    fname               = forms.CharField(required=False, max_length=200,
                                widget=forms.FileInput(attrs={'size':40}) )
    text                = forms.CharField(required=False, widget=forms.Textarea(
                                 attrs={'rows':10, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    visible_start       = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))
    visible_end         = forms.DateField(input_formats=['%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'size':10}))

  data_init = {
                'text'            : remove_link_icons(item_container.item.text),
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
              }
  app_name = 'file'
  my_title = _(u'Lösung ändern')
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsItemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [
           ( 'tab_base'      , [ 'text', ] ),
           ( 'tab_visibility', [ 'visible_start', 'visible_end' ] ),
         ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data, request.FILES)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['text_intro'] = help_form['one_file']['help']
    return render_to_response ( 'app/file/manage_edit.html', vars )
  """
  is_teacher = has_permission(request.user, item_container.container.path, 'perm_manage_folderish')
  if not is_teacher or item_container.owner == request.user:
    filename = DOWNLOAD_PROTECTED_PATH + item_container.container.path + item_container.item.name
    return send_file(filename, item_container.item.name)
  else:
    return show_error(request, item_container, _('Zugriffsrecht'),
                      _(u'<p>Nur die Lehrkraft darf alle Lösungen anschauen!</p>'))
  """