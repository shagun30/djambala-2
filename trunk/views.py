#-*-coding: utf-8 -*-
"""
/dms/views.py

.. enthaelt Hilfsfunktionen fuer alle dms-Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.01.2007  rename, delete, undo integriert
0.02  15.01.2007  Paste-Funktion
0.03  20.01.2007  Hilfsfunktionen nach utils.py
0.04  05.02.2007  Shreddern
0.05  28.02.2007  Auswertung von Dateien
0.06  02.03.2007  Formular fuer Kommentare
0.07  22.03.2007  dmsImage
0.08  27.03.2007  item_show_images
"""

import string

from django.utils.encoding  import smart_unicode
from django             import newforms as forms
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.queries        import get_folder_items
from dms.queries        import get_item_container
from dms.queries        import get_top_url
from dms.queries        import get_site_url

from dms.settings       import DOWNLOAD_PATH
from dms.utils          import get_footer_email

from dms.file.utils     import get_file_url

# -----------------------------------------------------
def login_view(request):
  """ """
  class DmsLoginForm(forms.Form):
    username = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'size':40}))
    password = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'size':20}))

  data_init = {'user_name' : '', 'password'  : '', }

  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = data_init
  f = DmsLoginForm(data)

  if request.method == 'POST' and not f.errors :
    username = request.POST['username']
    password = request.POST['password']
    user = dms.auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        dms.auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")
  else :
    vars = { 'content_div_style': 'frame-main-manage', 'form': f, }
    return render_to_response ( 'registration/login.html', vars )

# -----------------------------------------------------
def logout_view(request):
  """ """
  from dms.auth import logout

  logout(request)
  return HttpResponseRedirect(request['next'])

# -----------------------------------------------------
def get_my_item_container(request, op):
  # --- Gegebenenfalls wird index.html ergaenzt
  import string
  if op in ['login', 'password_change'] :
    return get_item_container ( '/', '' )
  path = request.path
  if op == '':
    item = get_item_container(path, op)
  else :
    item = get_item_container(path, '/' + op + '/')
  if item != None:
    return item
  if string.find ( path, '.html' ) < 0 :
    path += 'index.html'
  # --- Das Objekt wird gesucht
  if op == '':
    return get_item_container(path, op)
  else :
    return get_item_container(path, '/' + op + '/')

# -----------------------------------------------------
def get_file_path(item):
  return DOWNLOAD_PATH + item.container.path + item.name

# -----------------------------------------------------
# -----------------------------------------------------
def item_show_images(request, op):
  """ Bilderleiste """
  my_item_container = get_my_item_container(request, op)
  is_protected = my_item_container.container.is_protected()
  if not my_item_container.item.app.is_folderish and my_item_container.parent_item_id != -1:
    my_item_container = my_item_container.get_parent()
  app_name = 'folder'
  main_obj = {}
  main_obj['name'] = my_item_container.item.name
  main_obj['url']  = get_site_url(my_item_container,
                                  my_item_container.item.name + 'index.html')
  main_obj['app_name'] = my_item_container.item.app.name
  main_obj['is_sortable'] = True
  main_obj['top_url'] = get_top_url(my_item_container)
  main_obj['title'] = my_item_container.item.title
  main_obj['last_modified'] = my_item_container.last_modified.strftime('%d.%m.%Y %H:%M')
  objs = []
  if request.GET.has_key('sort') :
    order = request.GET['sort']
  else :
    order = ''
  items = get_folder_items(my_item_container, '')
  has_user_folder = False
  for item_container in items :
    if (item_container.item.app.is_folderish and not \
        item_container.item.app.is_userfolder ) or \
       ( item_container.item.app.name=='dmsImage' or \
         item_container.item.app.name=='dmsImagethumb' ):
      obj = {}
      obj['id'] = item_container.item.id
      obj['title'] = item_container.item.title
      obj['app_name'] = item_container.item.app.name
      obj['is_folderish'] = item_container.item.app.is_folderish
      if item_container.item.app.is_folderish :
        obj['url']  = get_site_url(item_container, 'index.html')
      else :
        obj['url']  = get_site_url(item_container, item_container.item.name)
      obj['name'] = item_container.item.name
      obj['app_description'] = item_container.item.app.description
      obj['last_modified'] = item_container.last_modified.strftime ( '%d.%m.%Y %H:%M' )
      obj['is_deleted'] = item_container.is_deleted
      if item_container.item.app.name=='dmsImage' or \
         item_container.item.app.name=='dmsImagethumb':
        obj['image_url'] = get_file_url(item_container, is_protected)
        obj['wh'] = ' / ' + smart_unicode(item_container.item.integer_1) +\
                    'x' + smart_unicode(item_container.item.integer_2)
      else:
        obj['image_url'] = ''
        obj['wh'] = ''
      objs.append ( obj )

  vars = { 'content_div_style': 'frame-util-images',
           'main_obj'         : main_obj,
           'objs'             : objs,
           'item'             : my_item_container.item,
           'site'             : my_item_container.container.site,
           'title'            : _('Bilderleiste'),
           'this_style'       : my_item_container.container.site.skin_style,
           'footer_email'     : get_footer_email(my_item_container.item),
           'last_modified'    : my_item_container.get_last_modified()
         }
  return render_to_response ( 'app/base_show_images.html', vars )
