# -*- coding: utf-8 -*-
"""
/dms/utitlies/info_manager.py

.. erlaubt Manipulationen der Info-Manager
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
0.02  02.10.2007  show_info_managers
0.03  23.10.2007  get_empty_folders
0.04  21.11.2007  find_items
"""

from django.utils.safestring  import SafeData, mark_safe, SafeUnicode
from django.utils.translation import ugettext as _

from django.utils.encoding  import smart_unicode
from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template    import Context
from django             import newforms as forms
from django.db          import transaction

from django.utils.translation import ugettext as _

from dms.roles          import UserEditPerms
from dms.text_icons     import LINK_ICON
from dms.utils_form     import get_item_vars_add
from dms.utils_form     import get_folderish_vars_edit
from dms.roles          import require_permission
from dms.queries        import get_item_container
from dms.queries        import get_user_by_username
from dms.queries        import get_site_url
from dms.queries        import get_item_container_children
from dms.queries        import get_app_list
from dms.queries        import get_distinct_info_mangers
from dms.queries        import count_user_items
from dms.queries        import get_user_item_containers
from dms.queries        import get_empty_folders
from dms.queries        import get_app_list
from dms.queries        import get_app_by_id
from dms.queries        import get_item_container_children_by_app_or_name
from dms.queries        import count_item_container_children_by_app_or_name

from dms.utils          import get_folderish_actions
from dms.utils          import get_tabbed_form
from dms.utils_base     import show_email
from dms.utils_base     import show_link
from dms.views_error    import show_error

from dms.utilities.help_form import help_form
from dms.encode_decode    import decode_html

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage')
def change_owner(request):
  """ aendert rekursiv die Eigentumsrechte """

  path = request.path
  item_container = get_item_container(path, '/change_owner/')

  @transaction.commit_manually
  def do_replace(item_container, user_old, user_new, edu_objects, complete_mode):
    """ ersetzt rekursiv den Besitzer """
    if complete_mode:
      children = get_item_container_children(item_container, True)
    else:
      children = [item_container]
    n = 0
    #assert False
    for child in children:
      if edu_objects != None and str(child.item.app.id) in edu_objects:
        if user_old == None or user_old == child.owner:
          child.item.owner = user_new
          child.item.save()
          child.owner = user_new
          child.save()
    if user_old == None or user_old == item_container.owner:
      item_container.item.owner = user_new
      item_container.item.save()
      item_container.owner = user_new
      item_container.save()
    transaction.commit()

  def get_edu_objects():
    """ liefert die Liste der IDs der moeglichen Lernresourcen """
    ret = []
    apps = get_app_list('description')
    for a in apps:
      #if a.name.find('Edu') > 0 or a.name == 'dmsRedirect':
      ret.append(a.id)
    return ret

  def get_edu_object_list():
    """ liefert die Liste der moeglichen Lernresourcen """
    ret = []
    apps = get_app_list('description')
    for a in apps:
      #if a.name.find('Edu') > 0 or a.name == 'dmsRedirect':
      ret.append((a.id, decode_html(a.description)))
    return ret

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    user_old = forms.CharField(required=False, max_length=40,
          widget=forms.TextInput(attrs={'size':40}) )
    user_new = forms.CharField(max_length=40,
          widget=forms.TextInput(attrs={'size':40}) )
    if item_container.item.app.is_folderish:
      complete_mode = forms.BooleanField(required=False)
      edu_object = forms.MultipleChoiceField(required=False, choices=get_edu_object_list(),
            widget=forms.CheckboxSelectMultiple() )

  app_name = 'info_manager'
  my_title = _('Info-Manager &auml;ndern')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else :
    data = { 'edu_object': get_edu_objects(), }
    if item_container.item.app.is_folderish:
      data['complete_mode'] = True
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)
  if item_container.item.app.is_folderish:
    tabs = [('tab_base',['edu_object', 'complete_mode', 'user_old','user_new']), ]
  else:
    tabs = [('tab_base',['user_old','user_new']), ]
  content = get_tabbed_form(tabs, help_form, app_name , f)

  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    if f.data['user_old'] == '':
      user_old = None
    else:
      user_old = get_user_by_username(f.data['user_old'])
    user_new = get_user_by_username(f.data['user_new'])
    if f.cleaned_data.has_key('edu_object'):
      edu_objects = f.cleaned_data['edu_object']
    else:
      edu_objects = None
    if f.cleaned_data.has_key('complete_mode'):
      complete_mode = f.cleaned_data['complete_mode']
    else:
      complete_mode = False
    if user_new != None:
      do_replace(item_container, user_old, user_new, edu_objects, complete_mode)
      return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
    else:
      return show_error(request, item_container, 'FEHLER', 'User unbekannt')

  vars = get_item_vars_add(request, item_container, app_name, my_title,
                            content, show_errors)
  vars['next'] = './'
  return render_to_response ( 'app/base_edit.html', vars )

# -----------------------------------------------------
# kann geloescht werden !!!!!!!!!!!!
@require_permission('perm_manage_site')
def show_info_managers_XX(request):
  """ zeigt die (aktiven) Patinnen und Paten des Bereichs """
  fSection = get_template('app/info_manager/info_managers.html')

  path = request.path #.replace('/index.html', '')
  item_container = get_item_container(path, '/info_managers/')
  users = get_distinct_info_mangers(item_container)
  links = []
  emails = []
  names_url = []
  main_url = get_site_url(item_container, 'index.html')
  for user in users:
    links.append(show_email(user.email, user.get_full_name()) + ' / ' + \
                 user.username)
    emails.append(user.email)
    url = main_url + '/resources/%s/' % user.username
    count = count_user_items(item_container, user)
    names_url.append(show_link(url, user.get_full_name()) + ' (%i)' % count)
  context = Context( { 'links': links,
                       'emails': emails,
                       'names_url': names_url } )
  content = fSection.render(context)
  app_name = 'info_manager'
  my_title = _('Patinnen und Paten')
  show_errors = False
  vars = get_item_vars_add(request, item_container, app_name, my_title,
                            content, show_errors)
  return render_to_response ( 'app/base_info.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage')
def show_resources(request, username):
  """ liefert die Ressourcen von <user> """
  path = request.path #.replace('/index.html', '')
  item_container = get_item_container(path, '/resources/%s/' % username)
  #item_containers = get_user_item_containers(item_container,
  #                                           get_user_by_username(username))

  def get_prev_next(offset, delta, count):
    show_prev = ''
    show_next = ''
    show_middle = ''
    n_start = 0
    if count > offset + 10*delta:
      show_next_more = True
      count = offset + 10*delta
    else:
      show_next_more = False
    if offset > 10*delta:
      show_prev_more = True
      n_start = offset - 10*delta
    else:
      show_prev_more = False
    n = n_start
    while n < count:
      if n < offset:
        show_prev += show_link(u'./?offset=%i' % n,
                               smart_unicode(n), url_class='navLink') + ' '
      elif n == offset:
        show_middle = '<b>%i</b> ' % n
      else:
        show_next += show_link(u'./?offset=%i' % \
                               n,
                               smart_unicode(n), url_class='navLink') + ' '
      n += delta
    if show_next_more:
      show_next += show_link(u'./?offset=%i' % \
                              n,
                              ' &raquo; Weiter', url_class='navLink')
    if show_prev_more:
      n_new = n_start-delta
      show_prev = show_link(u'./?offset=%i' % \
                              n_new,
                              'Zur&uuml;ck &laquo; ', url_class='navLink') + show_prev
    if count < delta:
      show_middle = ''
    return show_prev, show_middle, show_next

  def get_results(request):
    offset = 0
    delta  = 200
    count = -1
    if params.has_key('offset'):
      offset = int(params['offset'])
    item_containers = get_user_item_containers(item_container,
                                              get_user_by_username(username), 
                                              offset, delta)
    return item_containers, offset, delta

  app_name = 'user_resources'
  my_title = _('Ressourcen einer Patin/eines Paten')
  count = count_user_items(item_container, get_user_by_username(username))
  params = request.GET.copy()
  if params != {}:
    item_containers, offset, delta = get_results(request)
    show_prev, show_middle, show_next = \
         get_prev_next(offset, delta, count)
  else :
    item_containers, offset, delta = get_results(request)
    show_prev, show_middle, show_next = \
         get_prev_next(offset, delta, count)

  results = []
  for ic in item_containers:
    results.append(show_link(ic.get_absolute_url(), ic.item.title) + \
                   ' (%s)' % ic.item.app.name )
  content = ''
  vars = get_item_vars_add(request, item_container, app_name, my_title,
                           content, False)
  vars['username'] = username
  vars['results'] = results
  vars['count'] = count
  vars['show_prev'] = show_prev
  vars['show_middle'] = show_middle
  vars['show_next'] = show_next
  vars['no_top_main_navigation'] = True
  return render_to_response ( 'app/info_manager/resources.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage')
def show_info_managers(request):
  """ zeigt die (aktiven) Patinnen und Paten des Bereichs """
  fSection = get_template('app/info_manager/info_managers.html')

  path = request.path #.replace('/index.html', '')
  item_container = get_item_container(path, '/info_managers/')
  users = get_distinct_info_mangers(item_container)
  links = []
  emails = []
  names_url = []
  main_url = get_site_url(item_container, 'index.html')
  for user in users:
    links.append(show_email(user.email, user.get_full_name()) + ' / ' + \
                 user.username)
    emails.append(user.email)
    url = main_url + '/resources/%s/' % user.username
    count = count_user_items(item_container, user)
    names_url.append(show_link(url, user.get_full_name()) + ' (%i)' % count)
  context = Context( { 'links': links,
                       'emails': emails,
                       'names_url': names_url } )
  content = fSection.render(context)
  app_name = 'info_manager'
  my_title = _('Patinnen und Paten')
  show_errors = False
  vars = get_item_vars_add(request, item_container, app_name, my_title,
                            content, show_errors)
  return render_to_response ( 'app/base_info.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage')
def show_empty_folders(request):
  """ liefert eine Liste leerer Ordner """
  path = request.path.replace('/index.html', '')
  item_container = get_item_container(path, '/empty_folder/')

  def get_results(request):
    item_containers, total = get_empty_folders(item_container)
    return item_containers, total

  app_name = 'empty_folders'
  my_title = _('Leere Ordner')
  item_containers, total = get_results(request)

  results = []
  for ic in item_containers:
    results.append(show_link(ic.get_absolute_url(), ic.item.title) + \
                   ' (%s)' % ic.item.app.name )
  content = ''
  vars = get_item_vars_add(request, item_container, app_name, my_title,
                           content, False)
  vars['results'] = results
  vars['count'] = len(item_containers)
  vars['total'] = total
  vars['no_top_main_navigation'] = True
  return render_to_response ( 'app/info_manager/empty_folders.html', vars )

# -----------------------------------------------------
@require_permission('perm_manage')
def find_items(request):
  """ .. findet bestimmte Objekte """

  path = request.path
  item_container = get_item_container(path, '/find_items/')

  def get_prev_next_line(start, diff, count, app_id, app_name):
    """ Geschwisterseiten anzeigen """
    if count < diff:
      return ''
    from django.template.loader import get_template
    from django.template import Context
    t = get_template('app/userfolder/prev_next.html')
    n_min = start-diff
    if n_min < 0:
      n_min = 0
      prev_url = ''
      prev_info = ''
    else:
      prev_url = './?app_object=%i&name=%s&start=%i&diff=%i' % (app_id, app_name, n_min, diff)
      prev_info = _('vorhergehende Suchergebnisse (%(start_diff)i-%(start)i)' % \
                 {'start_diff': start-diff, 'start': start-1} )
    n_start = start + diff
    if n_start >= count:
      next_url = ''
      next_info = ''
    else:
      n_end = n_start + diff
      next_url = './?app_object=%i&name=%s&start=%i&diff=%i' % (app_id, app_name, n_start, diff)
      if n_end > count:
        n_end = count
      next_info = _('nachfolgende Suchergebnisse ') + '(%i-%i)' % \
                 (n_start, n_end)
    end = start + diff - 1
    if end > count:
      end = count
    c = Context( {'prev_url'     : prev_url,
                  'prev_info'    : prev_info,
                  'current_items': '&middot;&middot; %i-%i &middot;&middot;' % ( start, end ),
                  'next_url'     : next_url,
                  'next_info'    : next_info })
    return t.render(c)
  
  def get_app_choices():
    # liefert Liste der verfuegbaren Programme
    ret = []
    ret.append((-1, '---'))
    apps = get_app_list('description')
    for app in apps:
      t = '%s - <i>%s</i>' % (app.description, app.name)
      ret.append((app.id, mark_safe(t)))
    return ret

  def get_items(item_container, app_id, app_name, start, length):
    """ """
    f_item = get_template('utils/found_item.html')
    f_item_list = get_template('utils/find_results.html')
    #if app_id > -1:
    count = count_item_container_children_by_app_or_name(item_container, app_id, app_name)
    item_containers = get_item_container_children_by_app_or_name(item_container, 
                          app_id, app_name, start, length)
    #else:
    #  item_containers = find_item_containers_by_item_name(app_name)
    #  count = len(item_containers)
    prev_next = get_prev_next_line(start, diff, count, app_id, app_name)
    item_list = ''
    for ic in item_containers:
      if ic.item.app.is_folderish:
        url = get_site_url(ic, 'index.html')
      else:
        url = get_site_url(ic, ic.item.name)
      if ic.is_data_object:
        link_icon = ''
      else:
        link_icon = '&nbsp;&nbsp;' + LINK_ICON
      context = Context ( { 'folder_path': ic.container.path,
                            'item_url': url,
                            'item_name': ic.item.name,
                            'title': ic.item.title,
                            'data_object': link_icon,
                            'deleted': ic.is_deleted
                          } )
      item_list += f_item.render(context)
    prev_next = get_prev_next_line(start, diff, count, app_id, app_name)
    if app_id > -1:
      app_id_name = get_app_by_id(app_id).description
    else:
      app_id_name = ''
    context = Context( { 'app_id_name': app_id_name,
                         'app_name': app_name,
                         'count': count,
                         'item_list': item_list,
                         'prev_next': prev_next } )
    return f_item_list.render(context), count

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    app_object = forms.CharField(required=False, widget=forms.Select(choices=get_app_choices(),
                           attrs={'size':15, 'style':'width:80%'} ) )
    app_name   = forms.CharField(required=False,
                       max_length=240, widget=forms.TextInput(attrs={'size':60}) )

  app_name = 'find_items'
  my_title = _('Web-Ressource suchen')
  user_perms = UserEditPerms(request.user.username,request.path)
  if request.GET.has_key('start') :
    start = int(request.GET['start'])
    diff  = int(request.GET['diff'])
  else :
    start = 0
    diff  = 200
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if request.method == 'POST':
    data=request.POST.copy()
  else :
    data = {}
  # --- Formular mit Daten fuellen und zur Anzeige vorbereiten
  f = DmsItemForm(data)

  dont = { 'search_mode': False}
  # --- Wurde das Formular aufgerufen und gab es keine Fehler?
  if request.method=='POST' and not f.errors:
    data = f.cleaned_data
    if data.has_key('app_object') and data['app_object'] != '' and data['app_object'] != '-1':
      app_id = int(f.cleaned_data['app_object'])
    else:
      app_id = -1
    if data.has_key('app_name'):
      app_name = f.cleaned_data['app_name'].strip()
    else:
      app_name = ''
    if app_id == -1 and app_name == '':
      content = _(u'Bitte wählen Sie zumindest ein Suchfeld aus!')
      count = 0
    else:
      content, count = get_items(item_container, app_id, app_name, start, diff)
    vars = get_item_vars_add(request, item_container, app_name, my_title,
                              content, show_errors)
    vars['action'] = get_folderish_actions(request, user_perms,
                           item_container, app_name, False, dont)
    return render_to_response ( 'app/base_info.html', vars )
  elif request.method=='GET' and request.GET.has_key('app_object'):
    app_id = int(request.GET['app_object'])
    content, count = get_items(item_container, app_id, app_name, start, diff)
    vars = get_item_vars_add(request, item_container, app_name, my_title,
                              content, show_errors)
    vars['action'] = get_folderish_actions(request, user_perms,
                           item_container, app_name, False, dont)
    return render_to_response ( 'app/base_info.html', vars )
  else:
    tabs = [('tab_find_base',['app_name', 'app_object', ]), ]
    content = get_tabbed_form(tabs, help_form, app_name , f)
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, 
                            content, f, dont={}, ignore_own_breadcrumb=True)
    vars['action'] = get_folderish_actions(request, user_perms,
                           item_container, app_name, False, dont)
    vars['next'] = './'
    return render_to_response ( 'app/base_edit.html', vars )


