# -*- coding: utf-8 -*-
"""
/dms/resource/views_manage.py

.. enthaelt den View fuer die Management-Ansicht
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  30.01.2008  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url

from dms.roles                import require_permission
from dms.roles                import UserEditPerms
#from dms.folder.views_manage  import do_manage
from dms.resource.utils       import get_dont

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_resource_actions(request, user_perms, item_container, app_name,
                          has_user_folder, dont={}):
  """ von get_folderish_actions """
  from django.template.loader import get_template
  from django.template import Context
  from dms.queries        import get_base_site_url
  import string
  if not request.user.is_authenticated():
    return ''
  t = get_template('app/resource/manage_options_resource.html')
  nPos = max ( string.rfind ( request.path, '/add/' ),
               string.rfind ( request.path, '/edit/' ),
               string.rfind ( request.path, '/navigation/' ),
               string.rfind ( request.path, '/navigation_left/' ),
               string.rfind ( request.path, '/navigation_top/' ),
               string.rfind ( request.path, '/manage/' ),
               string.rfind ( request.path, '/manage_browseable/' ),
               string.rfind ( request.path, '/manage_comments/' ),
               string.rfind ( request.path, '/import/' ),
               string.rfind ( request.path, '/export/' ),
               string.rfind ( request.path, '/manage_site/' ),
               string.rfind ( request.path, '/manage_user/' ),
               string.rfind ( request.path, '/sort/' ),
               string.rfind ( request.path, '/empty_folders/' ),
               string.rfind ( request.path, '/find_items/' ),
             )
  if nPos > -1 or dont != {}:
    path = request.path[:nPos]
    show_mode       =  not dont.has_key('show_mode') and user_perms.perm_read
    add_mode        = not dont.has_key('add_mode') and \
                      user_perms.perm_add and item_container.item.has_user_support
    edit_mode       = not dont.has_key('edit_mode') and \
                      user_perms.perm_edit
    # --- Stimmen diese Rechte bei ..own..??
    manage_mode     = not dont.has_key('manage_mode') and \
                      ( user_perms.perm_manage or user_perms.perm_edit_own \
                        or user_perms.perm_manage_own )
    import_mode     = not dont.has_key('import_mode') and \
                      user_perms.perm_manage_folderish
    export_mode     = not dont.has_key('export_mode') and \
                      user_perms.perm_manage_folderish
    browseable_mode = not dont.has_key('browseable_mode') and \
                      user_perms.perm_edit
    comment_mode    = not dont.has_key('comment_mode') and \
                      item_container.item.has_comments and \
                      user_perms.perm_edit
    user_mode       = not dont.has_key('user_mode') and \
                      user_perms.perm_manage_user and has_user_folder
    navigation_mode = not dont.has_key('navigation_mode') and \
                      user_perms.perm_manage_folderish
    navigation_top_mode  = not dont.has_key('navigation_top_mode') and \
                      user_perms.perm_manage_site and item_container.container.id == 1
    navigation_left_mode = not dont.has_key('navigation_left_mode') and \
                      user_perms.perm_manage_site and \
                      ( item_container.container.id == 1 or item_container.item.app.name == 'dmsEduWebquestItem' \
                                                         or item_container.item.app.name == 'dmsProjectgroup')
    sort_mode       = not dont.has_key('sort_mode') and \
                      user_perms.perm_manage
    empty_mode      = not dont.has_key('empty_mode') and \
                      user_perms.perm_manage
    search_mode     = not dont.has_key('search_mode') and \
                      user_perms.perm_add
  else :
    path = request.path
    show_mode        = False
    add_mode         = False
    edit_mode        = False
    manage_mode      = True
    import_mode      = False
    export_mode      = False
    browseable_mode  = False
    comment_mode     = False
    user_mode        = False
    navigation_mode  = False
    navigation_top_mode  = False
    navigation_left_mode = False
    sort_mode        = False
    empty_mode       = False
    search_mode      = False

  if string.find ( path, 'index.html' ) < 0 :
    path += 'index.html'
  if ( string.find(request.path, '/add/') >= 0 ):
    edit_mode = False
    import_mode = False
    export_mode = False
    browseable_mode = False
    comment_mode = False
    user_mode = False
    navigation_mode = False
    navigation_left_mode = False
    sort_mode = False
    empty_mode = False
    search_mode = False
  elif ( string.find(request.path, '/edit/') >= 0 ) :
    edit_mode = False
    user_mode = False
  elif ( string.find(request.path, '/manage/') >= 0 ) :
    manage_mode = False
  elif ( string.find(request.path, '/manage_browseable/') >= 0 ) :
    browseable_mode = False
  elif ( string.find(request.path, '/manage_comment/') >= 0 ) :
    import_mode = False
    export_mode = False
    comment_mode = False
    user_mode = False
    navigation_mode = False
    navigation_left_mode = False
    sort_mode = False
  elif ( string.find(request.path, '/sort/') >= 0 ) :
    user_mode = False
    sort_mode = False
  elif ( string.find(request.path, '/empty_folders/') >= 0 ):
    empty_mode = False
  elif ( string.find(request.path, '/navigation/') >= 0 ) :
    user_mode = False
    navigation_mode = False
  elif ( string.find(request.path, '/navigation_top/') >= 0 ) :
    user_mode = False
    navigation_top_mode = False
  elif ( string.find(request.path, '/navigation_left/') >= 0 ) :
    user_mode = False
    navigation_left_mode = False
  add_mode = False
  browseable_mode = False
  sort_mode = False
  search_mode = False
  empty_mode = False
  import_mode = False
  export_mode = False
  c = Context( {'authenticated'       : request.user.is_authenticated(),
                'app_name'            : app_name,
                'show_mode'           : show_mode,
                'add_mode'            : add_mode,
                'edit_mode'           : edit_mode,
                'manage_mode'         : manage_mode,
                'import_mode'         : import_mode,
                'export_mode'         : import_mode,
                'browseable_mode'     : browseable_mode,
                'comment_mode'        : comment_mode,
                'navigation_mode'     : navigation_mode,
                'navigation_top_mode' : navigation_top_mode,
                'navigation_left_mode': navigation_left_mode,
                'sort_mode'           : sort_mode,
                'empty_mode'          : empty_mode,
                'search_mode'         : search_mode,
                'user_mode'           : has_user_folder and user_mode,
                'path'                : get_site_url(item_container, 'index.html'),
                'user_path'           : get_site_url(item_container,
                                                     'acl_users/index.html'),
                'user_perms'          : user_perms,
                'user_name'           : request.user,
                'base_site_url'       : get_base_site_url(),
               } )
  return t.render(c).strip()

# -----------------------------------------------------
#@require_permission('perm_add')
def do_manage(request, item_container, user_perms, add_ons, app_name,
              my_title, my_title_own, dont={}, allow_copy=True):
  """ Pflegemodus der Ressourcenverwaltung """
  from dms.utils_form           import get_base_vars
  from dms.utils                import get_site_actions
  from django.shortcuts   import render_to_response
  has_user_folder = False
  vars, user_perms = get_base_vars(request, item_container, 'frame-main-manage', False,
                                   ignore_own_breadcrumb=True)
  for k in dont.items():
    vars[k] = ''
  v = { 'allow_copy'       : allow_copy,
        'title'            : my_title,
        'this_title'       : item_container.item.title,
        #'action'           : get_folderish_actions(request, user_perms, item_container,
        #                         app_name, has_user_folder, dont),
        'action'           : get_resource_actions(request, user_perms, item_container,
                                 app_name, has_user_folder, dont),
        'action_site'      : get_site_actions(request, user_perms, item_container),
        'add_mode'         : user_perms.perm_add,
        'add_ons_0'        : add_ons[0],
        'add_ons_1'        : add_ons[1],
        'add_ons_2'        : add_ons[2],
        'add_ons_3'        : add_ons[3],
        'ajax_url'         : get_site_url(item_container, 'index.html/ajax/'),
        'no_top_main_navigation': True
      }
  vars.update(v)
  return render_to_response ( 'app/base_manage.html', vars )


# -----------------------------------------------------
@require_permission('perm_add')
def resource_manage(request, item_container):
  """ Pflegemodus der Ressourcenverwaltung """

  user_perms = UserEditPerms(request.user.username, request.path)
  add_ons = {}
  #add_ons[0] = [ { 'url' : get_site_url(item_container, 'index.html/add/faqitem/'),
  #                 'info': _(u'Beitrag zur FAQ-Liste')}, ]
  #add_ons[1] = [ { 'url' : get_site_url(item_container, 'index.html/add/faqboard/'),
  #                 'info': _(u'FAQ-Liste')}, ]
  #add_ons[2] = [ { 'url' : get_site_url(item_container, 'index.html/add/userfolder/'),
  #                 'info': _(u'Community-Mitglieder eintragen, löschen, Rechte ändern ...')}, ]
  add_ons[0] = [{},]
  add_ons[1] = [{},]
  add_ons[2] = [{},]
  add_ons[3] = [{},]

  app_name = 'resource'
  my_title = _(u'Ressourcenverwaltung pflegen')
  my_title_own = ''

  return do_manage(request, item_container, user_perms, add_ons, app_name, my_title, 
                   my_title_own, get_dont())
