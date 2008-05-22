#-*-coding: utf-8 -*-
"""
/dms/folder/views_manage_site.py

.. enthaelt den View zum Aendern der Domaine
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  25.04.2007  Beginn der Arbeit
"""

from django.http          import HttpResponse, HttpResponseRedirect
from django.shortcuts     import render_to_response
from django               import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles            import require_permission
from dms.roles            import UserEditPerms
from dms.roles            import get_user_roles
from dms.queries          import get_site_by_id
from dms.queries          import get_site_url
from dms.queries          import get_sites

from dms.utils            import get_tabbed_form
from dms.utils            import get_folderish_actions
from dms.utils_form       import get_base_vars

from dms.folder.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def folder_manage_site(request, item_container):
  """ Eigenschaften des Ordners aendern """

  def save_site(item_container, old, new):
    """ Abspeichern der Domaine """
    item_container.container.site.sub_title = new['site_sub_title']
    item_container.container.site.right_logo = new['site_right_logo']
    item_container.container.site.right_logo_url = new['site_right_logo_url']
    item_container.container.site.right_logo_width = new['site_right_logo_width']
    item_container.container.site.right_logo_height = new['site_right_logo_height']
    if new.has_key('site_url'):
      item_container.container.site.url = new['site_url']
      item_container.container.site.base_folder = new['site_base_folder']
      item_container.container.site.name = new['site_name']
      item_container.container.site.title = new['site_title']
      item_container.container.site.title_class = new['site_title_class']
      item_container.container.site.logo = new['site_logo']
      item_container.container.site.logo_url = new['site_logo_url']
      item_container.container.site.logo_width = new['site_logo_width']
      item_container.container.site.logo_height = new['site_logo_height']
      item_container.container.site.left_image_url = new['site_left_image_url']
      item_container.container.site.left_image_width = new['site_left_image_width']
      item_container.container.site.left_image_height = new['site_left_image_height']
    item_container.container.site.save()

  def get_choices():
    """ """
    items = get_sites('name')
    ret = []
    for item in items:
      ret.append( (item.id, u'%s :: %s ::%s' % (item.name, item.url, item.base_folder)) )
    return ret

  class dms_itemForm(forms.Form):
    site_url = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_base_folder = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_name = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_title = forms.CharField(max_length=60,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_sub_title = forms.CharField(required=False, max_length=60,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_title_class = forms.CharField(required=False, max_length=40,
                           widget=forms.TextInput(attrs={'size':40}) )
    site_logo = forms.CharField(required=False, max_length=120,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_logo_url = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_logo_width = forms.IntegerField(required=False, min_value=0, max_value=200,
                            widget=forms.TextInput(attrs={'size':5}) )
    site_logo_height = forms.IntegerField(required=False, min_value=0, max_value=400,
                            widget=forms.TextInput(attrs={'size':5}) )
    site_right_logo = forms.CharField(required=False, max_length=120,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_right_logo_url = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_right_logo_width = forms.IntegerField(required=False, min_value=0, max_value=200,
                            widget=forms.TextInput(attrs={'size':5}) )
    site_right_logo_height = forms.IntegerField(required=False, min_value=0, max_value=400,
                            widget=forms.TextInput(attrs={'size':5}) )
    site_left_image_url = forms.CharField(required=False, max_length=200,
                           widget=forms.TextInput(attrs={'size':60}) )
    site_left_image_width = forms.IntegerField(required=False, min_value=0, max_value=200,
                            widget=forms.TextInput(attrs={'size':5}) )
    site_left_image_height = forms.IntegerField(required=False, min_value=0, max_value=400,
                            widget=forms.TextInput(attrs={'size':5}) )

  app_name = u'folder'
  my_title = _(u'Domaine verwalten')
  my_role = get_user_roles(request.user.username, item_container.container.path)

  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  data_init = {'site_url': item_container.container.site.url,
          'site_base_folder': item_container.container.site.base_folder,
          'site_name': item_container.container.site.name,
          'site_title_class': item_container.container.site.title_class,
          'site_title': item_container.container.site.title,
          'site_sub_title': item_container.container.site.sub_title,
          'site_logo': item_container.container.site.logo,
          'site_logo_url': item_container.container.site.logo_url,
          'site_logo_width': item_container.container.site.logo_width,
          'site_logo_height': item_container.container.site.logo_height,
          'site_right_logo': item_container.container.site.right_logo,
          'site_right_logo_url': item_container.container.site.right_logo_url,
          'site_right_logo_width': item_container.container.site.right_logo_width,
          'site_right_logo_height': item_container.container.site.right_logo_height,
          'site_left_image_url': item_container.container.site.left_image_url,
          'site_left_image_width': item_container.container.site.left_image_width,
          'site_left_image_height': item_container.container.site.left_image_height,
          'domain': item_container.container.site.id,
          }
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = dms_itemForm(data)
  tabs = [('tab_site_title', ['site_sub_title', 'site_right_logo', 'site_right_logo_url',
                              'site_right_logo_width', 'site_right_logo_height' ]),
         ]
  if u'the_manager' in my_role:
    tabs = tabs + [('tab_site_extended', ['site_name', 'site_title', 'site_title_class',
                                          'site_logo', 'site_logo_url',
                                          'site_logo_width', 'site_logo_height',
                                          'site_left_image_url',
                                          'site_left_image_width', 'site_left_image_height',
                                          'site_url', 'site_base_folder', ]),]
  content=get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors:
    save_site(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    user_perms = UserEditPerms(request.user.username, request.path)
    vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage')
    v = { 'action'    : get_folderish_actions(request,user_perms, item_container, app_name, False),
          'errors'    : f.errors,
          'content'   : content,
          'title'     : my_title,
          'submit'    : my_title,
          'sub_title' : item_container.item.title
        }
    vars.update(v)
    vars['text'] = ''
    vars['text_more'] = ''
    return render_to_response ( 'app/base_edit.html', vars )
