#-*-coding: utf-8 -*-
"""
/dms/rssfeed/views_edit.py

.. enthaelt den View zum Aendern der Eigenschaften eines RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.07.2007  Beginn der Arbeit
"""

from django.http        import HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.models         import get_last_modified

from dms.queries        import get_item_container

from dms.roles          import require_permission
from dms.utils          import get_tabbed_form
from dms.utils          import remove_link_icons
from dms.utils_form     import get_item_vars_edit

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html

from dms.rssfeed.utils  import get_global_choices
from dms.rssfeed.help_form   import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_edit')
def rssfeed_edit(request, feed, ret_path):
  """ Eigenschaften des RSS-Feeds aendern """

  def save_values(feed, old, new):
    """ geaenderte Werte des RSS-Feeds speichern """
    has_changed = False
    key = 'title'
    if old[key] != new[key]:
      feed.title = encode_html(new[key])
      has_changed = True
    key = 'text'
    if old[key] != new[key]:
      feed.description = encode_html(new[key])
      has_changed = True
    key = 'url_more'
    if old[key] != new[key]:
      feed.link = new[key]
      has_changed = True
    key = 'section'
    if old[key] != new[key]:
      feed.general_mode = new[key]
      has_changed = True
    if has_changed:
      feed.last_modified = get_last_modified()
      feed.save()

  class DmsItemForm(forms.Form):
    """ Elemente des Eingabeformulars """
    title      = forms.CharField(max_length=240,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(max_length=180,
                       widget=forms.TextInput(attrs={'size':60}) )
    url_more   = forms.CharField(required=False, max_length=200,
                       widget=forms.TextInput(attrs={'size':60}) )
    section    = forms.ChoiceField(choices=get_global_choices(),
                       widget=forms.RadioSelect() )

  data_init = {
                'title'    : decode_html(feed.title),
                'text'     : remove_link_icons(feed.description),
                'url_more' : feed.link,
                'section'  : feed.general_mode,
              }
  app_name = 'rssfeed'
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = DmsItemForm(data)
  my_title = _(u'RSS-Feed ändern')
  tabs = [ ('tab_base', [ 'title', 'text', 'url_more', 'section', ]), ]
  content = get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors :
    save_values(feed, data_init, f.data)
    return HttpResponseRedirect(ret_path)
  else:
    path = request.path
    n_pos = path[:-1].rfind('/')
    path = path[:n_pos]
    n_pos = path.rfind('/')
    path = path[:n_pos+1]
    item_container = get_item_container(path, '')
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    return render_to_response ( 'app/base_edit.html', vars )
