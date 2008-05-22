#-*-coding: utf-8 -*-
"""
/dms/mediasurvey/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften eines Medien-Fragebogens
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.04.2007  Beginn der Arbeit
0.02  18.04.2007  Korrektur der Eingabemoeglichkeiten
"""

import string, datetime

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_app
from dms.queries        import get_site_url

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html_dir
from dms.mail           import send_control_email

from dms.mediasurvey.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def mediasurvey_edit(request, item_container):
  """ Eigenschaften der Informationsseite aendern """

  parent_app = get_parent_app(item_container)

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ speichert die Daten """
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    title           = forms.CharField(max_length=240,
                            widget=forms.TextInput(attrs={'size':60}) )
    sub_title       = forms.CharField(required=False, max_length=240,
                            widget=forms.TextInput(attrs={'size':60}) )
    text            = forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':12, 'cols':60, 'id':'ta', 'style':'width:100%;'}) )
    info_slot_right = forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    section         = forms.CharField(required=False,
                            widget=forms.Select(choices=get_parent_section_choices(item_container),
                                   attrs={'size':4, 'style':'width:40%'} ) )
    is_browseable   = forms.BooleanField(required=False)
    visible_start   = forms.DateField(input_formats=['%d.%m.%Y'],
                            widget=forms.TextInput(attrs={'size':10}))
    visible_end     = forms.DateField(input_formats=['%d.%m.%Y'],
                            widget=forms.TextInput(attrs={'size':10}))

  data_init = {
                'title'           : decode_html(item_container.item.title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : remove_link_icons(item_container.item.text),
                'info_slot_right' : info_slot_to_header(item_container.item.info_slot_right),
                'section'         : item_container.section,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
              }
  app_name = 'mediasurvey'
  my_title = _(u'Medienfragebogen ändern')
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)
  tabs = [
          ( 'tab_base'      , [ 'title', 'sub_title', 'text', ] ),
          ( 'tab_frame'     , [ 'info_slot_right', ] ),
          ( 'tab_visibility', [ 'section', 'is_browseable', 'visible_start', 'visible_end', ] ),
        ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
