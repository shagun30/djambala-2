# -*- coding: utf-8 -*-
"""
/dms/folderfs/views_show.py

.. zeigt den Inhalt eines FS-Ordners an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  08.01.2008  Beginn der Arbeit
0.02  10.01.2008  Umstellung auf Ajax
0.03  10.04.2008  Klemmbrett-Operationen
0.04  14.04.2008  get_quota
"""

import os
import shutil
import datetime
from stat import *

from django.shortcuts   import render_to_response
from django.http              import HttpResponse, HttpResponseRedirect
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.settings       import DOWNLOAD_URL
#from dms.settings       import DOWNLOAD_PROTECTED_PATH

from dms.roles          import UserEditPerms
from dms.queries        import get_site_url
from dms.queries        import get_quota
from dms.queries        import set_quota

from dms.utils          import check_name
from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_base_vars

from dms.file.utils     import get_file_size
from dms.file.utils     import get_file_modification_date
from dms.file.utils     import get_file_url
from dms.file.utils     import get_file_path
from dms.file.utils     import get_file_name
from dms.file.utils     import get_folder_name
from dms.folderfs.utils import get_user_support
from dms.folderfs.utils import calculate_quota
from dms.file.views_download  import send_file

from dms.utils          import get_item_actions# get_folderish_actions
from dms.utils          import show_link

from dms_ext.extension  import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def folderfs_add_file(request, item_container):
  """ ergaenzt eine Datei im FS-Ordner """
  files = request.FILES
  content = files['fname']['content']
  length = len(content)
  quota = get_quota(request.user.username)
  new_value = quota.value + length
  #if new_value < quota.max:
  set_quota(request.user.username, new_value)
  content_type = files['fname']['content-type']
  filename = files['fname']['filename']
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  name = check_name(files['fname']['filename'], True)
  file_name = base_path + request.POST['rel_path'] + name
  f = open(file_name, 'wb')
  f.write(content)
  f.close()
  os.chmod(file_name, 0660)
  return HttpResponseRedirect(get_site_url(item_container, 'index.html?rel_path=' + request.POST['rel_path']))

# -----------------------------------------------------
def folderfs_add_folder(request, item_container):
  """ ergaenzt einen Ordner im FS-Ordner """
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  path = base_path + new['rel_path'] + name
  try:
    os.mkdir(path)
    os.chmod(path, 0660)
  except:
    pass
  return HttpResponseRedirect(get_site_url(item_container, 'index.html?rel_path=' + request.POST['rel_path']))

# -----------------------------------------------------
def get_objs(request, item_container, mode=''):
  """ liefert die Inhalte des betreffenden Ordners """

  def get_file_url(item_container, rel_path, file_name, is_protected, is_file):
    """ liefert die entsprechende URL """
    if is_file:
      url = '%s/download/?file_path=/%s%s' % (get_site_url(item_container, 'index.html'), rel_path, file_name)
      return url, ''
    else:
      ajax_path_raw = '/ajax/folderfs_ajax_get_file_table/'
      ajax_path = '?rel_path=' + rel_path + file_name + '/'
      if file_name == '':
        return get_site_url(item_container, 'index.html' + ajax_path_raw), ajax_path
      else:
        return get_site_url(item_container, 'index.html' + ajax_path_raw + ajax_path), ajax_path

  def get_folder_items(item_container, rel_path):
    """ liefert Liste der im Dateisystem vorhandenen Dateien """
    protected = item_container.container.is_protected()
    base_path = get_folder_name(item_container, protected)
    path = base_path + rel_path
    # --- warum ???? Fehler in Python/Django ????
    stat = os.stat(path)
    fs_objs = os.listdir(path)
    objs = []
    for fs in fs_objs:
      stat = os.stat(path+fs)
      mode = stat[ST_MODE]
      #is_dir = S_ISDIR(mode)
      is_file = S_ISREG(mode)
      url, param = get_file_url(item_container, rel_path, fs, protected, is_file)
      m_time = stat[ST_MTIME]
      m_time_date = datetime.datetime.fromtimestamp(m_time)  
      m_time_str = m_time_date.strftime('%m/%d/%Y') #('%d.%m.%Y %H:%M')
      objs.append ( { 'id'      : fs,
                      'name'    : fs,
                      'is_file' : is_file,
                      'url'     : url,
                      'rel_path': param,
                      'size'    : stat[ST_SIZE],
                      'last_modified' : m_time_str } )
    if rel_path != '':
      n_pos = rel_path[:-1].rfind('/')
      if n_pos <= 0:
        add_path = ''
      else:
        add_path = rel_path[:n_pos] + '/'
      parent_path = add_path #get_file_url(item_container, '', add_path, protected, False)
      stat = os.stat(base_path+add_path)
      mode = stat[ST_MODE]
      m_time = stat[ST_MTIME]
      m_time_date = datetime.datetime.fromtimestamp(m_time)  
      parent_m_time = m_time_date.strftime('%m/%d/%Y') #('%d.%m.%Y %H:%M')
    else:
      parent_path = ''
      parent_m_time = ''
    return objs, parent_path, parent_m_time

  my_item_container = item_container
  main_obj = {}
  main_obj['url']  = get_site_url(my_item_container, 'index.html')
  user_perms = UserEditPerms(request.user.username,request.path)
  # .replace('..', '') verhindert den Zugriff auf uebergeordnete Dateien
  if request.GET.has_key('rel_path'):
    rel_path = request.GET['rel_path'].strip().replace('..', '')
  else:
    rel_path = ''
  if mode == 'del':
    del_id = request.GET['obj'].strip().replace('..', '')
    protected = item_container.container.is_protected()
    base_path = get_folder_name(item_container, protected)
    del_path = base_path + rel_path + del_id
    try:
      shutil.rmtree(del_path)
    except:
      os.unlink(del_path)
    total = calculate_quota(request.user)
  objs, parent_path, parent_m_time = get_folder_items(my_item_container, rel_path)
  if rel_path != '':
    main_obj['parent_path'] = '?rel_path=' + parent_path
    main_obj['last_modified'] = parent_m_time
  main_obj['rel_path'] = rel_path
  main_obj['base_url'] = item_container.get_absolute_url()
  main_obj['add_file_url'] = item_container.get_absolute_url() + '/add_file/'
  fi = item_container.get_absolute_url() + '/add_file/folderfs/'
  main_obj['add_folder_url'] = item_container.get_absolute_url() + '/add_folder/'
  if rel_path != '':
    main_obj['add_file_url'] = main_obj['add_file_url'] + '?rel_path=' + rel_path
    main_obj['add_folder_url'] = main_obj['add_folder_url'] + '?rel_path=' + rel_path
  main_obj['paste_mode'] = (('dms_cut_fs_id' in request.session) or ('dms_copy_fs_id' in request.session))
  quota = get_quota(request.user.username)
  main_obj['space'] = '%4.1f' % (100.0 * quota.value / quota.max)
  if quota.value < quota.max:
    main_obj['space_available'] = True
  return objs, main_obj

# -----------------------------------------------------
def folderfs_show(request, item_container):
  """ zeigt den Inhalt eines FS-Ordners """
  objs, main_obj = get_objs(request, item_container)
  app_name = 'folderfs'
  if request.method == 'POST':
    return HttpResponseRedirect(
               get_site_url(item_container, 'index.html'))
  else:
    vars, user_perms = get_base_vars(request, item_container, 'frame-main')
    v = { 'main_obj'  : main_obj,
          'objs'      : objs,
          'id'        : item_container.item.id,
          'title'     : _(u'Dateien/Ordner verwalten'),
          'sub_sub_title' : item_container.item.title,
          'action'    : get_item_actions(request, user_perms, item_container, app_name, False,
                                         { 'edit_mode': True, }),
          'add_mode'  : user_perms.perm_add,
          'next'      : get_site_url(item_container, 'index.html/manage_browseable/'),
          'ajax_url'  : get_site_url(item_container, 'index.html/ajax/'),
        }
    vars.update(v)
    vars['image_url'] = ''
    return render_to_response ( 'app/folderfs/show_files.html', vars )

# -----------------------------------------------------
def do_paste(request, item_container):
  """ """
  if request.GET.has_key('rel_path'):
    rel_path = request.GET['rel_path'].strip().replace('..', '')
  else:
    rel_path = ''
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  dest = base_path + rel_path
  if 'dms_cut_fs_id' in request.session:
    src = request.session['dms_cut_fs_id']
    name = src[src.rfind('/'):]
    shutil.move(src, dest + name)
    del request.session['dms_cut_fs_id']
  elif 'dms_copy_fs_id' in request.session:
    src = request.session['dms_copy_fs_id']
    name = src[src.rfind('/'):]
    shutil.copyfile(src, dest+name)
  total = calculate_quota(request.user)
  return request

# -----------------------------------------------------
def set_session(request, item_container, op, del_op):
  """ """
  if request.GET.has_key('rel_path'):
    rel_path = request.GET['rel_path'].strip().replace('..', '')
  else:
    rel_path = ''
  obj_id = request.GET['obj'].strip().replace('..', '')
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  ins_key = 'dms_%s_fs_id' % op
  request.session[ins_key] = base_path + rel_path + obj_id
  del_key = 'dms_%s_fs_id' % del_op
  if del_op in request.session:
    del request.session[del_op]
  return request

# -----------------------------------------------------
def create_folder(name, new, item_container):
  """ Raw-Ordner anlegen """
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  path = base_path + new['rel_path'] + name
  os.mkdir(path)

# -----------------------------------------------------
def create_file(request, name, new, files, item_container):
  """ Raw-Datei anlegen """
  content = files['fname']['content']
  length = len(content)
  #quota = get_quota(request.username)
  #new_value = quota.value + length
  #if new_value < quota.max:
  set_quota(request.username, new_value)
  content_type = files['fname']['content-type']
  filename = files['fname']['filename']
  protected = item_container.container.is_protected()
  base_path = get_folder_name(item_container, protected)
  file_name = base_path + new['rel_path'] + name
  f = open(file_name, 'wb')
  f.write(content)
  f.close()
  os.chmod(file_name, 0660)

# -----------------------------------------------------
def folderfs_ajax_get_file_table(request, item_container):
  """ liefert die Tabelle der Dateiobjekte """
  t_table = get_template('app/folderfs/file_table.html')
  mode = request.GET['mode']
  if mode == 'show':
    objs, main_obj = get_objs(request, item_container)
  elif mode == 'del':
    objs, main_obj = get_objs(request, item_container, mode)
  elif mode == 'cut':
    request = set_session(request, item_container, 'cut', 'copy')
    objs, main_obj = get_objs(request, item_container, mode)
  elif mode == 'copy':
    request = set_session(request, item_container, 'copy', 'cut')
    objs, main_obj = get_objs(request, item_container, mode)
  elif mode == 'paste':
    request = do_paste(request, item_container)
    objs, main_obj = get_objs(request, item_container, mode)
  elif mode == 'add_folder':
    name = check_name(request.POST['name'], True)
    if name != '':
      create_folder(name, request.POST, item_container)
    objs, main_obj = get_objs(request, item_container, mode)
  elif mode == 'add_file':
    try:
      name = check_name(request.FILES['fname']['filename'], True)
      create_file(request, name, request.POST, request.FILES, item_container)
    except:
      pass
    objs, main_obj = get_objs(request, item_container, mode)
  res = t_table.render(Context({'objs': objs, 'main_obj': main_obj}))
  return HttpResponse(res, mimetype="text/html; charset=utf-8")

# -----------------------------------------------------
def folderfs_download(request, item_container):
  """ bietet das betreffende Dateiobjekt zum Download an """
  # Problem: Home-Verzeichnis
  file_path = get_file_path(item_container)
  if request.GET.has_key('file_path'):
    fname = request.GET['file_path'].replace('..', '')
  else:
    fname += ''
  return send_file(file_path + fname, fname)
