#-*-coding: utf-8 -*-
"""
/dms/feeds.py

.. enthaelt den Dispatcher fuer alle RSS-Feeds
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.03.2007  Beginn der Arbeit
0.02  24.03.2007  Verallgemeinerung - Daten aus Datenbank
"""

from django.utils.translation import ugettext as _

from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext as _

from dms.settings       import MP3_DOWNLOAD

from dms.models     import DmsFeed
from dms.models     import DmsFeedItem

from dms.queries     import get_site_url
from dms.utils_base     import show_link
from dms.encode_decode  import decode_html

# -----------------------------------------------------
class RssFeeds(Feed):
  """ Klasse fuer RSS-Feeds """

  def get_object(self, rss_feed):
    """ """
    if len(rss_feed) != 1:
      raise ObjectDoesNotExist
    return DmsFeed.objects.get(name__exact=rss_feed[0])

  def title(self, obj):
    """ """
    if obj == None:
      raise ObjectDoesNotExist
    #return decode_html(obj.title)
    return obj.title

  def description(self, obj):
    """ """
    if obj == None:
      raise ObjectDoesNotExist
    d = obj.description
    return obj.description

  def link(self, obj):
    """ """
    if obj == None:
      raise ObjectDoesNotExist
    return obj.link

  def item_link(self, item_obj):
    """ """
    if item_obj.item_container.item.url_more.find('stream://') == 0:
      return MP3_DOWNLOAD + item_obj.item_container.item.url_more[9:]
    else:
      return get_site_url(item_obj.item_container, item_obj.item_container.item.name)

  def items(self, obj):
    return DmsFeedItem.objects.select_related().filter(feed=obj).\
                       filter(is_browseable=True).order_by('-last_modified')

def get_feeds(general_mode=2):
  """ """
  return DmsFeed.objects.filter(general_mode=general_mode).filter(is_deleted=False).order_by('name')

def get_all_feeds():
  """ """
  return DmsFeed.objects.extra(where=['general_mode!=0']).order_by('general_mode', 'name')

def get_feed_by_name(name):
  try:
    return DmsFeed.objects.get(name__exact=name)
  except:
    return None