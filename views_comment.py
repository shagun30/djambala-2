#-*-coding: utf-8 -*-
"""
/dms/views_comment.py

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
0.07  13.11.2007  Verschluesselung der E-Mail-Adresse
0.08  14.03.2008  Sofortige Anzeige des Kommentars
"""

from django.utils.safestring import SafeData, mark_safe, SafeUnicode
from django.utils.encoding  import smart_unicode
from django             import newforms as forms
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django.template.loader import get_template
from django.template    import Context

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.models         import DmsItem
from dms.models         import DmsComment
from dms.queries        import get_visible_comments
from dms.queries        import get_all_comments
from dms.queries        import get_item_containers_by_item_id
from dms.queries        import get_item_container_children
from dms.queries        import get_site_url
from dms.queries        import get_user
from dms.queries        import get_random_question_answer
from dms.queries        import check_answer

from dms.views_error    import show_error_spam

from dms.text_icons     import CONTROL_LINK
from dms.utils          import get_tabbed_form
from dms.utils          import get_breadcrumb
from dms.utils          import get_footer_email
from dms.utils          import get_item_actions
from dms.utils          import get_folderish_actions
from dms.utils          import get_author_email
from dms.views          import get_my_item_container

from dms.encode_decode  import decode_html
from dms.help_form      import get_help_form

from dms.roles          import UserEditPerms

# -----------------------------------------------------
def item_comment(request, op='', item_container=None):
  """ Anzeige der Kommentare zu einem Beitrag """
  if item_container == None:
    item_container = get_item_containers_by_item_id(int(request.POST['item_id']))[0]
  t = get_template('utils/comment-item.html')
  items = get_visible_comments(item_container)
  ret = ''
  for item in items:
    #e=item.email
    #assert False
    c = Context ( { 'title'  : item.title,
                    'email'  : get_author_email(item.name, item.email),
                    'text'   : item.text,
                    'last_modified': item.last_modified.strftime('%d.%m.%Y %H:%M'),
                  } )
    ret += t.render(c)
  t = get_template('utils/comments.html')

  question, answer = get_random_question_answer()
  my_user = get_user(request.user.username)
  if my_user != None:
    my_name = my_user.get_full_name()
    my_email = my_user.email
  else:
    my_name = ''
    my_email = ''
  
  class DmsItemForm(forms.Form):
    if my_user == None:
      username   = forms.CharField(max_length=60,
                        widget=forms.TextInput(attrs={'size':60}) )
      email      = forms.CharField(required=False, max_length=200,
                        widget=forms.TextInput(attrs={'size':60}) )
      anti_spam_question = forms.CharField(required=False,
                                widget=forms.HiddenInput(attrs={'value':question}) )
      anti_spam_answer   = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'size':20}) )
    else:
      # --- eigentlich koennte required=False entfallen
      username   = forms.CharField(required=False,
                         widget=forms.HiddenInput(attrs={'value':my_name}) )
      email      = forms.CharField(required=False,
                         widget=forms.HiddenInput(attrs={'value':my_email}) )
    title      = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(widget=forms.Textarea(
                                              attrs={'rows':10, 'cols':60, 'id':'ta', 
                                                    'style':'width:100%;'}) )
  if request.method == 'POST' :
    data = request.POST.copy ()
  else :
    data = {}
  f = DmsItemForm(data)
  # falls ..this_item_id == 0
  try:
    folder = get_item_containers_by_item_id(item_container.container.this_item_id)[0]
    if folder.item.is_moderated:
      tab_base = 'tab_base_moderated'
    else:
      tab_base = 'tab_base'
  except:
    tab_base = 'tab_base_moderated'
  if my_user == None:
    tabs = [ (tab_base, [ 'username', 'email', 'title', 'text', 
                            'anti_spam_question', 'anti_spam_answer' ]), ]
  else:
    tabs = [ (tab_base, [ 'username', 'email', 'title', 'text', ]), ]
  form = get_tabbed_form(tabs, get_help_form(), 'comment', f)
  c = Context ( { 'comments': ret,
                  'form'    : form,
                  'submit'  : _('Kommentar abgeben'),
                  'control' : CONTROL_LINK,
                  'item_id' : item_container.item.id,
                  'next'    : item_container.get_absolute_url() } )
  if request.method == 'POST' and not f.errors :
    if request.user.username == '':
      if f.data.has_key('anti_spam_question'):
        is_ok = check_answer(f.data['anti_spam_question'], f.data['anti_spam_answer'])
    else:
      is_ok = True
    if is_ok:
      # --- sofort anzeigen?
      parent = item_container
      while not parent.item.app.is_folderish:
        parent = parent.get_parent()
      f.data['is_browseable'] = not parent.item.is_moderated
      DmsComment().save_values(f.data)
      return HttpResponseRedirect(request.POST['next'])
    else:
      return show_error_spam(request, item_container)
  else :
    return t.render(c)

# -----------------------------------------------------
@require_permission('perm_manage')
def item_manage_comments(request, op):
  """ """

  def save_values(my_item, items, data):
    """ """
    for item in items:
      if data.has_key('delete_'+smart_unicode(item.id)):
        item.delete()
      elif data.has_key('is_visible_'+smart_unicode(item.id)):
        if not item.is_browseable:
          item.is_browseable = True
          item.save()
      else:
        if item.is_browseable:
          item.is_browseable = False
          item.save()

  item_container = get_my_item_container(request, op)
  user_perms = UserEditPerms(request.user.username,request.path)
  t = get_template('app/manage-comment-item.html')
  if item_container.item.has_comments:
    if item_container.item.app.is_folderish:
      items = []
      item_containers = get_item_container_children(item_container)
      for i in item_containers:
        items += get_all_comments(i)
    else:
      items = get_all_comments(item_container)
  else:
    items = []
  ret = ''
  for item in items:
    c = Context ( { 'obj' : item,
                    'last_modified': item.last_modified.strftime('%d.%m.%Y %H:%M'),
                  } )
    ret += t.render(c)
  my_title = _('Kommentare verwalten')

  next = get_site_url(item_container, 'index.html/manage_comments/')
  if request.method == 'POST' :
    data = request.POST.copy()
    save_values(item_container, items, data)
    return HttpResponseRedirect(next)

  user_perms = UserEditPerms(request.user.username, request.path)
  dont = {'comment_mode':False, 'navigation_mode':False, 'sort_mode':False}
  vars = { 'content_div_style': 'frame-main-manage',
           'site'             : item_container.container.site,
           'user_perms'       : user_perms,
           'my_item'          : item_container.item,
           'id'               : item_container.item.id,
           'title'            : my_title,
           'sub_title'        : item_container.item.title,
           'action'           : get_item_actions(request, user_perms, 
                                    item_container, 'comment', None),
           'breadcrumb'       : get_breadcrumb(item_container),
           'add_mode'         : user_perms.perm_add,
           'manage_comments'  : mark_safe(ret),
           'show_header'      : True,
           'action'           : get_folderish_actions(request, user_perms, item_container, 
                                                      'comment', False, dont),
           'footer_email'     : get_footer_email(item_container.item),
           'last_modified'    : item_container.get_last_modified(),
           'next'             : next
        }
  return render_to_response ( 'app/base_manage_comments.html', vars )

