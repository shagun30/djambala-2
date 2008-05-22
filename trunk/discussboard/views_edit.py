# -*- coding: utf-8 -*-
"""
/dms/discussboard/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften des Diskussionsforums
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.02  21.05.2008  get_role_choices
0.01  12.07.2007  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles          import *
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import remove_link_icons
from dms.utils          import get_choices_new_protected
from dms.utils_form     import get_folderish_vars_edit

from dms.encode_decode  import decode_html

from dms.discussboard.utils      import get_dont
from dms.discussboard.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit_folderish')
def discussboard_edit(request, item_container):
  """ Eigenschaften des Ordners aendern """

  params = request.GET.copy()
  profi_mode = params.has_key('profi')

  @transaction.commit_manually
  def save_values(item_container, old, new):
    """ Abspeichern der geaenderten Werte """
    item_container.container.save_values(old, new)
    item_container.item.save_values(old, new)
    item_container.save_modified_values(old, new)
    transaction.commit()

  class dms_itemForm ( forms.Form ) :
    title             = forms.CharField(max_length=240,
                              widget=forms.TextInput(attrs={'size':60}) )
    nav_title         = forms.CharField(max_length=60,
                              widget=forms.TextInput(attrs={'size':30}) )
    sub_title         = forms.CharField(required=False, max_length=240,
                              widget=forms.TextInput(attrs={'size':60}) )
    text              = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows':5, 'cols':60, 'id':'ta',
                                      'style':'width:100%;'}) )
    text_more         = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows':10, 'cols':60, 'id':'ta1',
                                      'style':'width:100%;'}) )
    image_url         = forms.CharField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
    image_url_url     = forms.URLField(required=False, max_length=200,
                              widget=forms.TextInput(attrs={'size':60}) )
    image_extern      = forms.BooleanField(required=False)
    is_wide           = forms.BooleanField(required=False)
    is_important      = forms.BooleanField(required=False)
    if profi_mode:
      info_slot_right= forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'style':'width:100%;'}) )
    else:
      info_slot_right= forms.CharField(required=False, widget=forms.Textarea(
                            attrs={'rows':10, 'cols':60, 'id':'ta2', 'style':'width:100%;'}) )
    section           = forms.CharField(required=False,
                              widget=forms.Select(choices=get_parent_section_choices(item_container),
                                      attrs={'size':4, 'style':'width:40%'} ) )
    has_user_support  = forms.BooleanField(required=False)
    has_comments      = forms.BooleanField(required=False)
    is_moderated      = forms.BooleanField(required=False)
    is_browseable     = forms.BooleanField(required=False)
    visible_start     = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':10}))
    visible_end       = forms.DateField(input_formats=['%d.%m.%Y'],
                             widget=forms.TextInput(attrs={'size':10}))
    show_next         = forms.BooleanField(required=False)
    integer_4   = forms.ChoiceField(choices=get_choices_new_protected(), widget=forms.RadioSelect() )

  app_name = 'discussboard'
  my_title = _(u'Diskussionsforum ändern')
  data_init = {
                'title'           : decode_html(item_container.item.title),
                'nav_title'       : decode_html(item_container.container.nav_title),
                'sub_title'       : item_container.item.sub_title,
                'text'            : remove_link_icons(item_container.item.text),
                'text_more'       : remove_link_icons(item_container.item.text_more),
                'image_url'       : item_container.item.image_url,
                'image_url_url'   : item_container.item.image_url_url,
                'image_extern'    : item_container.item.image_extern,
                'is_wide'         : item_container.item.is_wide,
                'is_important'    : item_container.item.is_important,
                'info_slot_right' : info_slot_to_header(item_container.item.info_slot_right),
                'section'         : decode_html(item_container.section),
                'has_comments'    : item_container.item.has_comments,
                'has_user_support': item_container.item.has_user_support,
                'is_moderated'    : item_container.item.is_moderated,
                'is_browseable'   : item_container.is_browseable,
                'visible_start'   : item_container.visible_start,
                'visible_end'     : item_container.visible_end,
                'integer_4'       : item_container.item.integer_4
              }

  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = dms_itemForm ( data )

  # --- Reihenfolge, Ueberschriften, Hilfetexte // Sonderfall: Startseite
  tabs = [
          ('tab_base'      , ['title', 'sub_title', 'nav_title', 'section', ]),
          ('tab_intro'     , ['text', 'text_more', 'image_url', 'image_url_url', 'image_extern',
                              'is_wide', 'is_important']),
          ('tab_user_support', ['has_user_support', 'integer_4', 'is_moderated', 'has_comments']),
          ('tab_frame'     , ['info_slot_right',]),
          ('tab_visibility', ['is_browseable', 'visible_start', 'visible_end',]),
          ]
  content = get_tabbed_form(tabs, help_form, app_name ,f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f, get_dont())
    return render_to_response ( 'app/base_edit.html', vars )
