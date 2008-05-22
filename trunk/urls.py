#-*-coding: utf-8 -*-
"""
queries.py

.. erster Wegweiser fuer Django (content Management System)

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.01.2007  Beginn der Arbeit
0.10  01.10.2007  replace_info_manager
0.11  23.10.2007  show_empty_folders
0.12  01.11.2007  exibition
0.13. 21.11.2007  find_items
0.14  13.05.2008  check
"""

from django.conf.urls.defaults  import *
#from django.contrib             import databrowse

from django.utils.translation import ugettext as _

from dms.helpdocument.views_show import helpdocument_show
from dms.views                  import logout_view
from dms.views                  import item_show_images
from dms.views_clipboard        import item_rename
from dms.views_clipboard        import item_delete, item_delete_total, item_undo
from dms.views_clipboard        import item_cut, item_copy
from dms.views_clipboard        import item_link_copy, item_link_multiple
from dms.views_clipboard        import item_delete_multiple 
from dms.views_clipboard        import item_delete_total_multiple
from dms.views_clipboard        import item_undo_multiple
from dms.views_clipboard        import item_cut_multiple, item_copy_multiple
from dms.views_clipboard        import item_paste
from dms.views_comment          import item_comment, item_manage_comments
from dms.views_rss              import item_rss
from dms.views_dms              import add_dms_object
from dms.views_dms              import dispatch_dms_object
from dms.views_dms              import dispatch_ajax
from dms.css.views              import generate_css_data
from dms.searchxapian.views_show import searchxapian_show
from dms.searchxapian.views_edu_show import searcheduxapian_show

from dms.utilities.info_manager import find_items
from dms.utilities.info_manager import change_owner
from dms.utilities.info_manager import show_info_managers
from dms.utilities.info_manager import show_resources
from dms.utilities.info_manager import show_empty_folders

from dms.xmlrpc.xmlrpc          import rpc_handler

from dms.feeds                  import RssFeeds
from dms.models                 import *

feeds = { 'rss': RssFeeds }

#databrowse.site.register(DmsApp)
#databrowse.site.register(DmsNavMenuLeft)
#databrowse.site.register(DmsSite)
#databrowse.site.register(DmsContainer)
#databrowse.site.register(DmsItem)
#databrowse.site.register(DmsItemContainer)
#databrowse.site.register(DmsComment)
#databrowse.site.register(DmsRoles)
#databrowse.site.register(DmsUserUrlRole)
#databrowse.site.register(DmsOrg)
#databrowse.site.register(DmsUserOrg)
#databrowse.site.register(DmsSubOrg)
#databrowse.site.register(DmsGroup)
#databrowse.site.register(DmsUserGroup)
#databrowse.site.register(DmsFeed)
#databrowse.site.register(DmsFeedItem)

urlpatterns = patterns('',
    # -- Ein/Ausloggen
    (r'^login/$',             'dms.auth.views.login', 
                               {'template_name': 'registration/login.html'}),
    (r'^accounts/login/$',    'dms.auth.views.login', 
                               {'template_name': 'registration/login.html'}),
    (r'^logout/$',            logout_view),
    (r'^password_change/$',   'dms.auth.views.password_change',
                               {'template_name': 'registration/password_change.html'}),
    #(r'^userdata_edit/$',     'dms.userdata.views.userdata_edit'),

    # -- Verwaltungsmodul
    (r'^admin/',              include('django.contrib.admin.urls')),

    # -- dms-ajax-Objekte
    (r'/ajax/(?P<ajax_op>.*)/$',              dispatch_ajax ),
    # -- dms-Objekte ergaenzen
    (r'.html/add/(?P<app>.*)/$',              add_dms_object ),

    # -- dms-Hilfe
    (r'/form_help/(?P<app>.*)/$',             helpdocument_show ),

    (r'^xml_rpc_srv/',                        rpc_handler),
    # -- dms-Objekte
    (r'/(?P<op>rename)/$',                    item_rename ),
    (r'/(?P<op>delete)/$',                    item_delete ),
    (r'/(?P<op>delete_total)/$',              item_delete_total ),
    (r'/(?P<op>undo)/$',                      item_undo ),
    (r'/(?P<op>cut)/$',                       item_cut ),
    (r'/(?P<op>copy)/$',                      item_copy ),
    (r'/(?P<op>link_copy)/$',                 item_link_copy ),
    (r'/(?P<op>link_multiple)/$',             item_link_multiple ),
    (r'/(?P<op>delete_multiple)/$',           item_delete_multiple ),
    (r'/(?P<op>delete_total_multiple)/$',     item_delete_total_multiple ),
    (r'/(?P<op>undo_multiple)/$',             item_undo_multiple ),
    (r'/(?P<op>cut_multiple)/$',              item_cut_multiple ),
    (r'/(?P<op>copy_multiple)/$',             item_copy_multiple ),
    (r'/(?P<op>paste)/$',                     item_paste ),
    (r'(?P<op>manage_comments)/$',            item_manage_comments ),
    (r'(?P<op>add_comment)/$',                item_comment ),
    (r'/(?P<op>add_rss)/$',                   item_rss ),
    (r'/(?P<op>show_images)/$',               item_show_images ),

    (r'.html$',                               dispatch_dms_object ),
    (r'/(?P<op>edit)/$',                      dispatch_dms_object ),
    (r'/(?P<op>check)/$',                     dispatch_dms_object ),
    (r'/(?P<op>show)/$',                      dispatch_dms_object ),
    (r'/(?P<op>download)/$',                  dispatch_dms_object ),
    (r'/(?P<op>exibition)/$',                 dispatch_dms_object ),
    (r'searchxapianedu',                      searcheduxapian_show ),
    (r'searchxapian',                         searchxapian_show ),
    (r'find_items',                           find_items ),
    (r'change_owner',                         change_owner ),
    (r'info_managers',                        show_info_managers ),
    (r'resources/(?P<username>.*)/$',         show_resources ),
    (r'empty_folders',                        show_empty_folders ),

    (r'.html/(?P<op>.*)/$', dispatch_dms_object ),

    # -- Hilferoutinen
    (r'^css_generate', generate_css_data ),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    #(r'^databrowse/(.*)', databrowse.site.root),
    # -- ..html vergessen?
    (r'.*$', dispatch_dms_object ),
)
