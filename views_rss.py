#-*-coding: utf-8 -*-
"""
/dms/views_rss.py

.. enthaelt Hilfsfunktionen fuer alle dms-Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.13.2007  Beginn der Arbeit
0.02  28.02.2008  Auswertung vorhandener Feeds
"""

from django             import newforms as forms
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django.db          import transaction

from django.utils.translation import ugettext as _

#from dms.roles          import *
from dms.models         import DmsItem
from dms.models         import DmsFeed
from dms.models         import DmsFeedItem
from dms.queries        import get_feed
from dms.queries        import exist_feed_item
from dms.queries        import get_feed_items
from dms.queries        import get_site_url

from dms.utils          import get_tabbed_form
from dms.utils          import get_folderish_actions
from dms.views          import get_my_item_container
from dms.mail           import send_control_email
from dms.utils_form     import get_item_vars_edit

from dms.help_form      import get_help_form

from dms.feeds          import get_feeds

# -----------------------------------------------------
def item_rss(request, op):
  """ Anzeige moeglicher RSS-Feeds """

  @transaction.commit_manually
  def save_values(item_container, new, user):
    """ Abspeichern der geaenderten Werte """
    if new.has_key('rss_feeds'):
      items = new['rss_feeds']
      for r in new['rss_feeds']:
        f = get_feed(int(r))
        if not exist_feed_item(f, item_container):
          DmsFeedItem().save_values(f, item_container, user)
        send_control_email(item_container, f)
    transaction.commit()

  item_container = get_my_item_container(request, op)
  my_item = item_container.item

  choices = []
  feeds = get_feeds(2)
  for feed in feeds:
    choices.append ( (feed.id, feed.title ) )
  feeds = get_feeds(1)
  for feed in feeds:
    choices.append ( (feed.id, feed.title ) )

  class DmsItemForm ( forms.Form ) :
    rss_feeds  = forms.MultipleChoiceField(required=False, choices=choices,
                        widget=forms.CheckboxSelectMultiple() )

  if request.method == 'POST' :
    data = request.POST.copy ()
  else:
    items = get_feed_items(item_container)
    feeds = []
    for item in items:
      feeds.append(item.feed.id)
    data = { 'rss_feeds': feeds, }
  f = DmsItemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [ ('tab_rss',  [ 'rss_feeds', ]), ]
  content = get_tabbed_form(tabs, get_help_form(), 'rssfeed', f)

  app_name = 'rssfeed'
  if request.method == 'POST' and not f.errors :
    save_values(item_container, f.cleaned_data, request.user)
    return HttpResponseRedirect(get_site_url(item_container, item_container.item.name))
  else :
    #user_perms = UserEditPerms(request.user.username, request.path)
    my_title = _('RSS-Feed zuordnen')
    vars = get_item_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['sub_title'] = my_item.sub_title
    #vars['action'] = get_folderish_actions(request, user_perms, item_container,
    #                                                app_name, False)
    vars['moderated_text'] = '<h4>' + my_item.title + '</h4>\n' + my_item.text
    vars['content'] = content
    vars['submit'] = my_title
    return render_to_response ( 'app/base_edit.html', vars )

