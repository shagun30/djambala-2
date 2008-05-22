#-*-coding: utf-8 -*-
"""
/dms/emailitem/views_edit.py

.. enthaelt den View zum Aendern der Frage
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.01.2008  Beginn der Arbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_parent_app
from dms.queries        import get_site_url
from dms.queries        import save_item
from dms.queries        import save_item_container
from dms.queries        import get_data_item_container

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import info_slot_to_header
from dms.utils          import get_parent_section_choices
from dms.utils          import get_license_choices
from dms.utils          import remove_link_icons
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import  decode_html

from dms.surveyitem.utils      import get_yes_no_choices
from dms.emailitem.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def emailitem_edit(request, item_container):
  """ Eigenschaften der Frage aendern """

  parent_app = get_parent_app(item_container)

  def save_values(item_container, old, new):
    if item_container.is_data_object:
      if new.has_key('text'):
        new['text'] = new['text'].replace('<p>', '').replace('</p>', '')
      else:
        new['text'] = ''
      save_item(item_container, old, new)
    else:
      save_item_container(item_container, old, new)

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    title           = forms.CharField(max_length=240,
                            widget=forms.TextInput(attrs={'size':60}) )
    sub_title       = forms.CharField(required=False, max_length=240,
                            widget=forms.TextInput(attrs={'size':60}) )
    text            = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':4, 'cols':60, 'style':'width:100%;'}) )
    text_more       = forms.CharField(required=False, widget=forms.Textarea(
                      attrs={'rows':4, 'cols':60, 'style':'width:100%;'}) )
    section         = forms.CharField(required=False,
                            widget=forms.Select(choices=get_parent_section_choices(item_container),
                                  attrs={'size':4, 'style':'width:40%'} ) )
    integer_1 = forms.ChoiceField(choices=get_yes_no_choices(), widget=forms.RadioSelect() )
    integer_2 = forms.IntegerField(required=False, min_value=1, max_value=200, widget=forms.TextInput(attrs={'size':5}) )
    integer_3 = forms.IntegerField(required=False, min_value=1, max_value=80, widget=forms.TextInput(attrs={'size':5}) )
    integer_4 = forms.IntegerField(required=False, min_value=20, max_value=60, widget=forms.TextInput(attrs={'size':5}) )
    integer_5 = forms.IntegerField(required=False, min_value=3, max_value=20, widget=forms.TextInput(attrs={'size':5}) )

  data_init = {
                'title'           : decode_html(item_container.item.title),
                'sub_title'       : decode_html(item_container.item.sub_title),
                'text'            : item_container.item.text.replace('<p>','').replace('</p>',''),
                'text:_more'      : item_container.item.text_more.replace('<p>','').replace('</p>',''),
                'section'         : item_container.section,
                'integer_1'       : item_container.item.integer_1,
                'integer_2'       : item_container.item.integer_2,
                'integer_3'       : item_container.item.integer_3,
                'integer_4'       : item_container.item.integer_4,
                'integer_5'       : item_container.item.integer_5,
              }
  app_name = u'emailitem'
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)
  my_title = _(u'Frage ändern')
  form_type = item_container.item.string_1
  if form_type == 'input':
    tabs = [ ('tab_base', [ 'title', 'sub_title', 'text_more', 
                            'integer_1', 'integer_2', 'integer_3', 'section', ]), ]
  elif form_type == 'text':
    tabs = [ ('tab_base', [ 'title', 'sub_title', 'text_more', 
                            'integer_1', 'integer_4', 'integer_5', 'section', ]), ]
  else:
    tabs = [ ('tab_base', [ 'title', 'sub_title', 'text', 'text_more',
                            'integer_1', 'section', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else:
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
