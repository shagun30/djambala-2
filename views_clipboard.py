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
0.09  17.04.2007  get__parent__item__container
0.10  19.06.2007  delete_menuitem_navmenu_left
0.11  19.09.2007  is_changeable
0.12  24.09.2007  item_link_multiple
0.13  23.10.2007  item_container_id wird beim Loeschen uebergeben
0.14  30.10.2007  get_photo_names
0.15  05.11.2007  item_container_id
0.16  14.11.2007  rmdir_fs
0.17  19.12.2007  Umstellung auf get_parent
0.18  24.03.2008  os.system(command) mv ..
0.19  08.04.2008  the_manager darf auch mit is:changeable-Objekte loeschen
0.20  26.04.2008  get_parent bei Rename
"""

import string, os, types, datetime

from django.utils.translation import ugettext as _

from django             import newforms as forms
from django.http        import HttpResponse, HttpResponseRedirect
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.models         import DmsItem
from dms.models         import DmsItemContainer

from dms.queries        import get_user
from dms.queries        import app_is_allowed
from dms.queries        import get_item_container_by_id
from dms.queries        import get_item_containers_by_item_container_id
from dms.queries        import get_item_container_by_parent_item_id
from dms.queries        import exist_item
from dms.queries        import is_file_by_item_container
from dms.queries        import get_site_url
from dms.queries        import change_container_path
from dms.queries        import get_item_container_by_id
from dms.queries        import get_new_container_with_data
from dms.queries        import move_containers
from dms.queries        import delete_menuitem_navmenu_left
from dms.queries        import get_item_container_children
from dms.queries        import delete_feed_by_name
from dms.queries        import delete_total_feed_by_name
from dms.queries        import undo_feed_by_name
from dms.queries        import get_feed_name
from dms.queries        import rmdir_fs
from dms.queries        import get_role_by_user_path

from dms.feeds          import get_feed_by_name

from dms.views          import get_my_item_container
from dms.utils          import check_name

from dms.file.utils     import get_file_path

from dms.views_error    import show_error_object_exist

# -----------------------------------------------------
def is_file_type(app_name):
  """ Objekte mit Datei-Eigenschaften liefern True, siehe queries is_file_by_item_container """
  return ( app_name in ['dmsFile', 'dmsExerciseFile',
                        'dmsImage', 'dmsImagethumb',
                        'dmsEduFileItem', 'dmsEduScormItem',
                        'dmsFreemind'] )

# -----------------------------------------------------
def get_photo_names(file_name):
  """ ..liefert die Namen der verkleinerten Bilder """
  # --- siehe dms.photos.views_add
  ext_pos = file_name.rfind('.')
  file_name_small = file_name[:ext_pos] + '_small' + file_name[ext_pos:]
  file_name_middle = file_name[:ext_pos] + '_middle' + file_name[ext_pos:]
  return file_name_small, file_name_middle

# -----------------------------------------------------
@transaction.commit_manually
def item_rename(request, op):
  """ Namen des Objektes aendern """
  item_container = get_my_item_container(request, op)
  if item_container.is_changeable:
    if request.GET.has_key('new_name') :
      is_folderish = item_container.item.app.is_folderish
      app_name = item_container.item.app.name
      # --- muss eventuell .html ergaenzt werden?
      check_this_name = is_folderish or is_file_type(app_name)
      new_name = check_name(request.GET['new_name'], check_this_name)
      # --- Gibt es schon in Objekt mit dem gewuenschten Namen?
      parent = item_container.get_parent()
      if parent != None and exist_item(parent, new_name):
        transaction.commit()
        return show_error_object_exist(request, item_container, new_name)
      if is_file_type(app_name):
        old_path = get_file_path(item_container)
        new_path = old_path[:string.rfind(old_path,'/')+1] + new_name
        os.rename(old_path, new_path)
      # --- Aenderungen vornehmen
      if is_folderish:
        n_pos = 1 + string.rfind(item_container.container.path[:-1], '/')
        new_path = item_container.container.path[:n_pos] + new_name +'/'
        old_path = item_container.container.path
        change_container_path(old_path, new_path)
      item_container.item.name = new_name
      item_container.item.save()
  transaction.commit()
  parent = item_container.get_parent()
  path = get_site_url(parent, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def do_delete_item(this_item_container, my_role):
  # --- Hauptebene kann nicht geloescht werden
  if this_item_container.parent_item_id != -1 and (this_item_container.is_changeable or my_role<=10):
    this_item_container.is_deleted = True
    this_item_container.save()

def do_delete(this_item_container, my_role):
  """ Objekte gegebenenfalls rekursiv loeschen """
  is_folderish = this_item_container.item.app.is_folderish
  if is_folderish and this_item_container.is_data_object:
    item_containers = get_item_container_by_parent_item_id(this_item_container.item_id)
    for item_container in item_containers:
      if item_container.id != this_item_container.id:
        do_delete(item_container, my_role)
  do_delete_item(this_item_container, my_role)

# -----------------------------------------------------
def do_delete_total_file(this_item_container, my_role):
  if this_item_container.is_data_object and (this_item_container.is_changeable or my_role<=10):
    app_name = this_item_container.item.app.name
    # --- muss Datei aus dem Filesystem entfernt werden?
    if is_file_type(app_name):
      file_name = get_file_path(this_item_container)
      try:
        os.unlink(file_name)
      except:
        pass
      # --- Sonderfall Photos
      if app_name == 'dmsPhoto':
        ext_pos = file_name.rfind('.')
        file_name_small, file_name_middle = get_photo_names(file_name)
        try:
          os.unlink(file_name_small)
        except:
          pass
        try:
          os.unlink(file_name_middle)
        except:
          pass
    elif this_item_container.item.app.is_folderish:
      rmdir_fs(this_item_container)
    # --- item wird indirekt in do_delete_total geloescht
    #this_item_container.item.delete()

def do_delete_total(request, this_item_container, first=True):
  """ Objekte werden gegebenenfalls rekursiv geloescht """
  if first and request.GET.has_key('item_container_id'):
    ic_id = request.GET['item_container_id']
    this_item_container = get_item_container_by_id(ic_id)
  # --- gegebenenfalls Klemmbrett loeschen
  if 'dms_cut_id' in request.session \
     and request.session['dms_cut_id'] == this_item_container:
    del request.session['dms_cut_id']
  if 'dms_copy_id' in request.session \
     and request.session['dms_copy_id'] == this_item_container:
    del request.session['dms_copy_id']
  if 'dms_link_copy_id' in request.session \
     and request.session['dms_link_copy_id'] == this_item_container:
    del request.session['dms_link_copy_id']
  # hier beginnt die Loeschroutine
  my_role = get_role_by_user_path(request.user, this_item_container.container.path)
  if this_item_container.item.app.is_folderish and this_item_container.is_data_object:
    item_containers = get_item_container_children(this_item_container, True)
    for item_container in item_containers:
      if item_container.id != this_item_container.id \
      and item_container.item.app.is_folderish:
        do_delete_total(request, item_container, False)
      else:
        do_delete_total_file(item_container, my_role)
        # --- bei Einblendungen: nur den Verweis loeschen
        if item_container.is_data_object:
          item_container.item.delete()
        else:
          item_container.delete()
  do_delete_total_file(this_item_container, my_role)
  if this_item_container.item.app.is_folderish and this_item_container.is_data_object:
    if this_item_container.item.app.name == 'dmsProjectgroup':
      delete_menuitem_navmenu_left(this_item_container.container.menu_left_id)
    this_item_container.container.delete()
  # --- bei Einblendungen: nur den Verweis loeschen
  if this_item_container.is_data_object:
    this_item_container.item.delete()
  this_item_container.delete()

# -----------------------------------------------------
def item_delete(request, op):
  """ Objekt loeschen, indem is_deleted auf True gesetzt wird """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  if item_container != None:
    my_role = get_role_by_user_path(request.user, item_container.container.path)
    if item_container.parent_item_id != -1:
      do_delete(item_container, my_role)
    parent = item_container.get_parent()
    ret_path = get_site_url(parent, 'index.html/manage/')
  else:
    # --- Sonderfall: RSS-Feed
    name, ret_path = get_feed_name(request, op)
    feed = get_feed_by_name(name)
    if feed != None:
      delete_feed_by_name(name)
  return HttpResponseRedirect(ret_path)

# -----------------------------------------------------
#@transaction.commit_manually
def item_delete_total(request, op):
  """ Objekt schreddern """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  parent = item_container.get_parent()
  ret_path = get_site_url(parent, 'index.html/manage/')
  if item_container.parent_item_id != -1:
    do_delete_total(request, item_container)
  else:
    name, ret_path = get_feed_name(request, op)
    feed = get_feed_by_name(name)
    if feed != None:
      delete_total_feed_by_name(name)
  return HttpResponseRedirect(ret_path)

# -----------------------------------------------------
def do_undo_item(this_item_container):
  # --- Objekt wiederherstellen
  this_item_container.is_deleted = False
  this_item_container.save()

def do_undo(this_item_container):
  """ Objekte gegebenenfalls rekursiv wiederherstellen """
  do_undo_item(this_item_container)
  is_folderish = this_item_container.item.app.is_folderish
  if is_folderish:
    item_containers = get_item_container_by_parent_item_id(this_item_container.item_id)
    for item_container in item_containers:
      if item_container.id != this_item_container.id:
        if item_container.item.app.is_folderish:
          do_undo(item_container)
        else:
          do_undo_item(item_container)

# -----------------------------------------------------
def item_undo(request, op):
  """ Objekt wiederherstellen, indem is_deleted auf False gesetzt wird """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  if item_container != None:
    do_undo(item_container)
    parent = item_container.get_parent()
    ret_path = get_site_url(parent, 'index.html/manage/')
  else:
    # --- Sonderfall: RSS-Feed
    name, ret_path = get_feed_name(request, op)
    feed = get_feed_by_name(name)
    if feed != None:
      undo_feed_by_name(name)
  return HttpResponseRedirect(ret_path)

# -----------------------------------------------------
def item_cut(request, op):
  """ Objekt zum Ausschneiden markieren """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  if item_container.parent_item_id != -1 and item_container.is_changeable:
    request.session['dms_cut_id'] = item_container.id
    if 'dms_copy_id' in request.session:
      del request.session['dms_copy_id']
    elif 'dms_link_copy_id' in request.session:
      del request.session['dms_link_copy_id']
  parent = item_container.get_parent()
  path = get_site_url(parent, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_copy(request, op):
  """ Objekt zum Ausschneiden markieren """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  if item_container.parent_item_id != -1:
    #hr request.session['dms_copy_id'] = item_container.item.id
    request.session['dms_copy_id'] = item_container.id
    if 'dms_cut_id' in request.session:
      del request.session['dms_cut_id']
    if 'dms_link_copy_id' in request.session:
      del request.session['dms_link_copy_id']
  parent = item_container.get_parent()
  path = get_site_url(parent, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_link_copy(request, op):
  """ Objekt zum Einblenden markieren """
  if request.GET.has_key('id'):
    item_container = get_item_container_by_id(request.GET['id'])
  else:
    item_container = get_my_item_container(request, op)
  if item_container.parent_item_id != -1:
    #request.session['dms_link_copy_id'] = item_container.item.id
    request.session['dms_link_copy_id'] = item_container.id
    if 'dms_cut_id' in request.session:
      del request.session['dms_cut_id']
    elif 'dms_copy_id' in request.session:
      del request.session['dms_copy_id']
  if request.GET.has_key('base_url'):
    path = request.GET['base_url'] + '/manage/'
  else:
    parent = item_container.get_parent()
    path = get_site_url(parent, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_link_multiple(request, op):
  my_item_container = get_my_item_container(request, op)
  data = request.POST.copy ()
  keys = data.keys()
  this_key = 'link_'
  link_ids = []
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      link_ids.append(id)
  if link_ids != []:
    request.session['dms_link_copy_id'] = link_ids
    if 'dms_cut_id' in request.session:
      del request.session['dms_cut_id']
    elif 'dms_copy_id' in request.session:
      del request.session['dms_copy_id']
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def do_cut(paste_item_container, item_container):
  if paste_item_container.item.app.is_folderish:
    old_path = get_file_path(paste_item_container)
    #old_path = old_path[:1+old_path[:-1].rfind('/')]
    new_path = get_file_path(item_container)
    try:
      command = 'mv %s %s' % (old_path, new_path)
      os.system(command)
      #os.renames(old_path, new_path)
    except:
      pass
    # --- Pfade anpassen
    new_container = move_containers(paste_item_container, item_container)
    # --- Objekt an den neuen Ort anpassen
    paste_item_container.container = new_container
  else:
    if is_file_by_item_container(paste_item_container):
      copy_move_file(paste_item_container, item_container, True)
    # --- Objekt an den neuen Ort anpassen
    paste_item_container.container = item_container.container
  paste_item_container.parent_item_id = item_container.item.id
  paste_item_container.part_of_id = item_container.part_of_id
  paste_item_container.save()

# -----------------------------------------------------
def do_copy(paste_item_container, item_container, recursion=True):
  is_file = is_file_by_item_container(paste_item_container)
  if is_file:
    copy_move_file(paste_item_container, item_container, False)
  container = item_container.container
  if paste_item_container.item.app.is_folderish:
    container = get_new_container_with_data(paste_item_container.item.name,
                                            item_container,
                                            paste_item_container.container)
    container.save()
  item_container_old_id = paste_item_container.id
  new_item = paste_item_container.item.copy()
  new_item_container = DmsItemContainer()
  new_item_container.copy(paste_item_container, container, new_item, item_container.item.id)
  if recursion and paste_item_container.item.app.is_folderish:
    item_container_old = get_item_container_by_id(item_container_old_id)
    item_containers = get_item_container_by_parent_item_id(item_container_old.item.id)
    for i in item_containers:
      do_copy(i, paste_item_container)

# -----------------------------------------------------
def do_link_copy(request, paste_item_container, item_container):
  """ Einblendungen vornehmen """
  new_item_container = DmsItemContainer()
  new_item_container.container      = item_container.container
  new_item_container.item           = paste_item_container.item
  new_item_container.owner          = get_user(request.user.username)
  new_item_container.is_deleted     = paste_item_container.is_deleted
  new_item_container.parent_item_id = item_container.item.id
  new_item_container.section        = paste_item_container.section
  new_item_container.order_by       = paste_item_container.order_by
  new_item_container.part_of_id     = paste_item_container.part_of_id
  new_item_container.is_browseable  = paste_item_container.is_browseable
  new_item_container.is_data_object = 0
  new_item_container.is_changeable  = paste_item_container.is_changeable
  new_item_container.visible_start  = paste_item_container.visible_start
  new_item_container.visible_end    = paste_item_container.visible_end
  new_item_container.last_modified  = datetime.datetime.now()
  new_item_container.save()
  return new_item_container

# -----------------------------------------------------
def copy_file(source_file, name, new_path):
  """ Datei soeichern """
  file_name = new_path + name
  try:
    os.makedirs(new_path)
  except:
    pass
  os.chmod(new_path, 0750)
  try:
    r = open(source_file, 'rb')
    f = open(file_name, 'wb')
    content = r.read()
    f.write(content)
    f.close()
    r.close()
    os.chmod(file_name, 0660)
  except:
    pass
  return file_name

# -----------------------------------------------------
def copy_move_file(file_item_container, target_item_container, move_mode=False):
  """ verschiebt Datei synchron im Dateisystem """
  old_path = get_file_path(file_item_container)
  new_path = get_file_path(target_item_container) #[:string.rfind(old_path,'/')+1]
  copy_file(old_path, file_item_container.item.name, new_path)
  if move_mode:
    try:
      os.unlink(old_path)
    except:
      pass

# -----------------------------------------------------
def item_paste(request, op):
  """ Objekt einfuegen """
  item_container = get_my_item_container(request, op)
  if 'dms_cut_id' in request.session :
    paste_ids = request.session['dms_cut_id']
    mode = 'cut'
  elif 'dms_copy_id' in request.session :
    paste_ids = request.session['dms_copy_id']
    mode = 'copy'
  elif 'dms_link_copy_id' in request.session :
    paste_ids = request.session['dms_link_copy_id']
    mode = 'link_copy'
  else:
    paste_ids = -1
    mode = 'unknown'
  # --- muss nur ein Objekt eingefuegt/verschoben werden?
  if type(paste_ids) != types.ListType:
    paste_ids = [ paste_ids ]
  # --- Staubsauger in Yellow Submarine
  do_it = True
  if mode == 'cut':
    temp_item_container = item_container
    do_it = not (temp_item_container.id in paste_ids)
    while do_it and temp_item_container.parent_item_id != -1:
      temp_item_container = temp_item_container.get_parent()
      do_it = not (temp_item_container.id in paste_ids)
  if do_it:
    owner = get_user(request.user.username)
    for paste_id in paste_ids:
      paste_item_container = get_item_container_by_id(paste_id)
      if paste_item_container != None:
        if mode == 'cut':
          do_cut(paste_item_container, item_container)
        elif mode == 'link_copy':
          do_link_copy(request, paste_item_container, item_container)
        elif mode == 'copy':
          do_copy(paste_item_container, item_container)
    if mode == 'cut':
      del request.session['dms_cut_id']
  path = get_site_url(item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def get_paste_obj(request, item_container):
  """ """
  paste_id = -1
  if 'dms_cut_id' in request.session:
    paste_id = request.session['dms_cut_id']
    if type(paste_id) == types.ListType:
      mode = _('wurden ausgeschnitten')
    else:
      mode = _('Wurde ausgeschnitten')
    mode_short = _('a')
  elif 'dms_copy_id' in request.session:
    paste_id = request.session['dms_copy_id']
    if type(paste_id) == types.ListType:
      mode = _('wurden kopiert')
    else:
      mode = _('Wurde kopiert')
    mode_short = _('k')
  elif 'dms_link_copy_id' in request.session :
    paste_id = request.session['dms_link_copy_id']
    mode = _('k&ouml;nnen eingeblendet werden')
    mode_short = _('e')
  else :
    return ''
  # 
  if type(paste_id) != types.ListType:
    paste_id = [paste_id]
  # --- Staubsauger in Yellow submarine!
  if 'dms_cut_id' in request.session:
    for p in paste_id:
      if p == item_container.id:
        return ''
  if len(paste_id) > 1:
    return _(u'Mehrere Objekte %s') % mode
  else:
    item_containers = get_item_containers_by_item_container_id(paste_id[0])
    if len(item_containers) < 1 \
    or ( not app_is_allowed(item_container, item_containers[0]) ):
      return ''
    return u'<a href="%s" title="%s">%s</a> <i>[%s]</i>' % \
          (item_containers[0].get_absolute_url(), mode,
           item_containers[0].item.title, mode_short)

# -----------------------------------------------------
def get_paste_app_name(request):
  """ """
  paste_id = -1
  if 'dms_cut_id' in request.session :
    paste_id = request.session['dms_cut_id']
  elif 'dms_copy_id' in request.session :
    paste_id = request.session['dms_copy_id']
  else :
    return ''
  if type(paste_id) == types.ListType:
    return ''
  else:
    item_container = get_item_container_by_id(paste_id)
    if item_container == None:
      return ''
    return item_container.item.app.name

# -----------------------------------------------------
def item_delete_multiple(request, op):
  """ Objekte loeschen, indem is_deleted auf True gesetzt wird """
  my_item_container = get_my_item_container(request, op)
  my_role = get_role_by_user_path(request.user, my_item_container.container.path)
  keys = request.POST.keys()
  this_key = 'delete_'
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      item_container = get_item_container_by_id(id)
      # the_manager darf auch geschuetzte Objekte loeschen
      if item_container != None and (item_container.is_changeable or my_role <=10):
        do_delete(item_container, my_role)
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_undo_multiple(request, op):
  """ geloeschte Objekte wieder sichtbar machen = is_deleted auf True setzen """
  my_item_container = get_my_item_container(request, op)
  data = request.POST.copy ()
  keys = data.keys()
  this_key = 'undo_'
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      item_container = get_item_container_by_id(id)
      if item_container != None:
        item_container.is_deleted = False
        item_container.save()
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_delete_total_multiple(request, op):
  my_item_container = get_my_item_container(request, op)
  data = request.POST.copy ()
  keys = data.keys()
  this_key = 'delete_total_'
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      item_container = get_item_container_by_id(id)
      if item_container != None:
        do_delete_total(request, item_container)
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_cut_multiple(request, op):
  my_item_container = get_my_item_container(request, op)
  data = request.POST.copy ()
  keys = data.keys()
  this_key = 'cut_'
  cut_ids = []
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      cut_ids.append(id)
  if cut_ids != []:
    request.session['dms_cut_id'] = cut_ids
    if 'dms_copy_id' in request.session:
      del request.session['dms_copy_id']
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)

# -----------------------------------------------------
def item_copy_multiple(request, op):
  my_item_container = get_my_item_container(request, op)
  data = request.POST.copy ()
  keys = data.keys()
  this_key = 'copy_'
  copy_ids = []
  for key in keys:
    if key.startswith(this_key):
      id = int(key[len(this_key):])
      item_container = my_item_container.get_parent()
      if item_container != None and item_container.parent_item_id != -1:
        copy_ids.append(id)
  if copy_ids != []:
    request.session['dms_copy_id'] = copy_ids
    if 'dms_cut_id' in request.session:
      del request.session['dms_cut_id']
  path = get_site_url(my_item_container, 'index.html/manage/')
  return HttpResponseRedirect(path)
