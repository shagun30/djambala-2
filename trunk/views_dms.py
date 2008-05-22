#-*-coding: utf-8 -*-
"""
/dms/views_dms.py

.. enthaelt den Dispatcher fuer alle dms-Objekte
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.01.2007  Beginn der Umsetzung
0.02  16.01.2007  document_add
0.03  22.01.2007  user_folder
0.04  23.01.2007  redirect
0.05  28.01.2007  lecture
0.06  16.03.2007  newsboard
0.07  22.03.2007  image
0.08  27.04.2007  import
0.09  04.06.2007  eventboard, eventitem
0.10  16.06.2007  get_role
0.11  04.07.2007  rssfeed
0.12  15.07.2007  discussitem
0.13  17.07.2007  pinboard
0.14  06.09.2007  edutextitem
0.15  14.09.2007  edufolder_sitemap
0.16  01.10.2007  faqboard
0.17  29.10.2007  gallery, photo
0.18  05.11.2007  todolist
0.19  06.11.2007  emailform
0.20  10.11.2007  is_protected
0.21  14.11.2007  newsletter, newsletteritem
0.22  16.11.2007  folderprotected
0.23  29.11.2007  export
0.24  14.01.2008  survey, surveyitem
0.25  19.01.2008  emailitem (Umstellung auf Survey-Prinzip)
0.26  28.01.2008  resource, agenda
0.27  31.01.2008  projectgroupemail
0.28  09.02.2008  wiki
0.29  18.02.2008  trainingdb
0.30  25.02.2008  views_reportsingle
0.31  26.02.2008  views_reportquestion
0.32  10.03.2008  Korrektur der Fehlertexte bei unzureichenden Zugriffsrechten
0.33  11.03.2008  eduscormitem
0.34  16.03.2008  freemind
0.35  17.03.2008  wikiitem
0.36  30.03.2008  folderorg
0.37  18.04.2008  usermanagementorg
0.38  30.04.2008  webquest
0.39  01.05.2008  exercise
0.40  02.05.2008  exercisefolder
0.41  14.05.2008  eduexerciseitem
0.42  16.05.2008  folderschool
0.43  20.05.2008  schoolmanagement
"""

import string, datetime

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.settings       import BASE_SITE_URL
from dms.settings       import ORG
from dms.feeds          import get_feed_by_name

from dms.models                           import DmsItem
from dms.queries                          import get_item_container
from dms.queries                          import get_role_by_user_path
from dms.queries                          import get_feed_name

#from dms.agenda.views_show                import agenda_show
#from dms.agenda.views_add                 import agenda_add
#from dms.agenda.views_edit                import agenda_edit

from dms.discussboard.views_show               import discussboard_show
from dms.discussboard.views_add                import discussboard_add
from dms.discussboard.views_edit               import discussboard_edit
from dms.discussboard.views_manage             import discussboard_manage
from dms.discussboard.views_manage_browseable  import discussboard_manage_browseable

from dms.discussitem.views_show             import discussitem_show
from dms.discussitem.views_add              import discussitem_add
from dms.discussitem.views_edit             import discussitem_edit

from dms.document.views_show                import document_show
from dms.document.views_add                 import document_add
from dms.document.views_edit                import document_edit

from dms.eduexerciseitem.views_show               import eduexerciseitem_show
from dms.eduexerciseitem.views_add                import eduexerciseitem_add
from dms.eduexerciseitem.views_edit               import eduexerciseitem_edit
from dms.eduexerciseitem.views_manage             import eduexerciseitem_manage
from dms.eduexerciseitem.views_manage_browseable  import eduexerciseitem_manage_browseable
from dms.eduexerciseitem.views_sort               import eduexerciseitem_sort

from dms.edufolder.views_show               import edufolder_show
from dms.edufolder.views_add                import edufolder_add
from dms.edufolder.views_edit               import edufolder_edit
from dms.edufolder.views_manage             import edufolder_manage
from dms.edufolder.views_manage_browseable  import edufolder_manage_browseable
from dms.edufolder.views_navigation         import edufolder_navigation
from dms.edufolder.views_sitemap            import edufolder_sitemap
from dms.edufolder.views_newitems           import edufolder_newitems
from dms.edufolder.views_sort               import edufolder_sort

from dms.edufileitem.views_show             import edufileitem_show
from dms.edufileitem.views_add              import edufileitem_add
from dms.edufileitem.views_edit             import edufileitem_edit

from dms.edugalleryitem.views_add                import edugalleryitem_add
from dms.edugalleryitem.views_edit               import edugalleryitem_edit
from dms.edugalleryitem.views_manage             import edugalleryitem_manage
from dms.edugalleryitem.views_manage_browseable  import edugalleryitem_manage_browseable
from dms.edugalleryitem.views_sort               import edugalleryitem_sort
from dms.edugalleryitem.views_show               import edugalleryitem_show
from dms.edugalleryitem.views_exibition          import edugalleryitem_exibition

from dms.edulinkitem.views_show             import edulinkitem_show
from dms.edulinkitem.views_add              import edulinkitem_add
from dms.edulinkitem.views_edit             import edulinkitem_edit

from dms.edumediaitem.views_show               import edumediaitem_show
from dms.edumediaitem.views_add                import edumediaitem_add
from dms.edumediaitem.views_edit               import edumediaitem_edit
from dms.edumediaitem.views_manage             import edumediaitem_manage
from dms.edumediaitem.views_manage_browseable  import edumediaitem_manage_browseable
from dms.edumediaitem.views_sort               import edumediaitem_sort

from dms.eduscormitem.views_show            import eduscormitem_show
from dms.eduscormitem.views_add             import eduscormitem_add
from dms.eduscormitem.views_edit            import eduscormitem_edit

from dms.edutextitem.views_show             import edutextitem_show
from dms.edutextitem.views_add              import edutextitem_add
from dms.edutextitem.views_edit             import edutextitem_edit

from dms.eduwebquestitem.views_show               import eduwebquestitem_show
from dms.eduwebquestitem.views_add                import eduwebquestitem_add
from dms.eduwebquestitem.views_edit               import eduwebquestitem_edit
from dms.eduwebquestitem.views_manage             import eduwebquestitem_manage
from dms.eduwebquestitem.views_manage_browseable  import eduwebquestitem_manage_browseable
from dms.eduwebquestitem.views_sort               import eduwebquestitem_sort
from dms.eduwebquestitem.views_navigation_left    import eduwebquestitem_navigation_left

from dms.elixier.views_show                 import elixier_show
from dms.elixier.views_add                  import elixier_add
from dms.elixier.views_edit                 import elixier_edit
from dms.elixier.views_beitraege            import elixier_ajax_get_unknown
from dms.elixier.views_beitraege            import elixier_ajax_get_ok
from dms.elixier.views_beitraege            import elixier_ajax_get_rejected

from dms.emailform.views_show               import emailform_show
from dms.emailform.views_add                import emailform_add
from dms.emailform.views_edit               import emailform_edit
from dms.emailform.views_manage             import emailform_manage
from dms.emailform.views_sort               import emailform_sort

from dms.emailitem.views_show               import emailitem_show
from dms.emailitem.views_add                import emailitem_add
from dms.emailitem.views_edit               import emailitem_edit

from dms.eventitem.views_show               import eventitem_show
from dms.eventitem.views_add                import eventitem_add
from dms.eventitem.views_edit               import eventitem_edit

from dms.eventboard.views_show              import eventboard_show
from dms.eventboard.views_add               import eventboard_add
from dms.eventboard.views_edit              import eventboard_edit
from dms.eventboard.views_manage            import eventboard_manage
from dms.eventboard.views_manage_browseable import eventboard_manage_browseable
from dms.eventboard.views_show              import eventboard_ajax_get_events

from dms.exercise.views_show               import exercise_show
from dms.exercise.views_add                import exercise_add
from dms.exercise.views_edit               import exercise_edit
from dms.exercise.views_manage             import exercise_manage

from dms.exercisefile.views_show           import exercisefile_show
from dms.exercisefile.views_add            import exercisefile_add
from dms.exercisefile.views_edit           import exercisefile_edit
from dms.exercisefile.views_download       import exercisefile_download
from dms.exercisefile.views_check          import exercisefile_check

from dms.exercisefolder.views_show               import exercisefolder_show
from dms.exercisefolder.views_add                import exercisefolder_add
from dms.exercisefolder.views_edit               import exercisefolder_edit
from dms.exercisefolder.views_manage             import exercisefolder_manage
from dms.exercisefolder.views_manage_browseable  import exercisefolder_manage_browseable
from dms.exercisefolder.views_navigation         import exercisefolder_navigation
from dms.exercisefolder.views_sitemap            import exercisefolder_sitemap
from dms.exercisefolder.views_sort               import exercisefolder_sort

from dms.export_dms.views_add              import export_add

from dms.faqboard.views_show               import faqboard_show
from dms.faqboard.views_add                import faqboard_add
from dms.faqboard.views_edit               import faqboard_edit
from dms.faqboard.views_manage             import faqboard_manage
from dms.faqboard.views_manage_browseable  import faqboard_manage_browseable
from dms.faqboard.views_sort               import faqboard_sort

from dms.faqitem.views_show                import faqitem_show
from dms.faqitem.views_add                 import faqitem_add
from dms.faqitem.views_edit                import faqitem_edit

from dms.file.views_show                  import file_show
from dms.file.views_add                   import file_add
from dms.file.views_edit                  import file_edit
from dms.file.views_download              import file_download

from dms.folder.views_show                import folder_show
from dms.folder.views_add                 import folder_add
from dms.folder.views_edit                import folder_edit
from dms.folder.views_manage              import folder_ajax_get_standard
from dms.folder.views_manage              import folder_ajax_get_delete
from dms.folder.views_manage              import folder_ajax_get_undo
from dms.folder.views_manage              import folder_ajax_get_delete_total
from dms.folder.views_manage              import folder_ajax_get_cut
from dms.folder.views_manage              import folder_ajax_get_copy
from dms.folder.views_manage              import folder_ajax_get_link
from dms.folder.views_manage              import folder_manage
from dms.folder.views_manage_site         import folder_manage_site
from dms.folder.views_manage_browseable   import folder_manage_browseable
from dms.folder.views_sort                import folder_sort
from dms.folder.views_navigation          import folder_navigation
from dms.folder.views_navigation_top      import folder_navigation_top
from dms.folder.views_navigation_left     import folder_navigation_left

from dms.folderfs.views_show              import folderfs_show
from dms.folderfs.views_show              import folderfs_add_file
from dms.folderfs.views_show              import folderfs_add_folder
from dms.folderfs.views_show              import folderfs_download
from dms.folderfs.views_add               import folderfs_add
from dms.folderfs.views_edit              import folderfs_edit
from dms.folderfs.views_show              import folderfs_ajax_get_file_table

from dms.folderschool.views_show            import folderschool_show
from dms.folderschool.views_add             import folderschool_add
from dms.folderschool.views_edit            import folderschool_edit
from dms.folderschool.views_manage          import folderschool_manage
from dms.folderschool.views_manage_browseable  import folderschool_manage_browseable
from dms.folderschool.views_navigation_left    import folderschool_navigation_left
from dms.folderschool.views_sort            import folderschool_sort

from dms.freemind.views_show                import freemind_show
from dms.freemind.views_download            import freemind_download
from dms.freemind.views_add                 import freemind_add
from dms.freemind.views_edit                import freemind_edit

from dms.gallery.views_show                 import gallery_show
from dms.gallery.views_exibition            import gallery_exibition
from dms.gallery.views_add                  import gallery_add
from dms.gallery.views_edit                 import gallery_edit
from dms.gallery.views_manage               import gallery_manage
from dms.gallery.views_manage_browseable    import gallery_manage_browseable
from dms.gallery.views_sort                 import gallery_sort

from dms.guestbook.views_show               import guestbook_show
from dms.guestbook.views_add                import guestbook_add
from dms.guestbook.views_edit               import guestbook_edit
from dms.guestbook.views_manage             import guestbook_manage
from dms.guestbook.views_manage_browseable  import guestbook_manage_browseable

from dms.guestbookitem.views_show           import guestbookitem_show
from dms.guestbookitem.views_add            import guestbookitem_add
from dms.guestbookitem.views_edit           import guestbookitem_edit

from dms.home.views_show                    import home_show
from dms.home.views_add                     import home_add
from dms.home.views_edit                    import home_edit
from dms.home.views_manage                  import home_manage
from dms.home.views_manage_browseable       import home_manage_browseable
from dms.home.views_navigation_left         import home_navigation_left
from dms.home.views_sort                    import home_sort

from dms.image.views_show                   import image_show
from dms.image.views_add                    import image_add
from dms.image.views_edit                   import image_edit
from dms.image.views_download               import image_download

from dms.imagethumb.views_show              import imagethumb_show
from dms.imagethumb.views_add               import imagethumb_add
from dms.imagethumb.views_edit              import imagethumb_edit

from dms.import_dms.views_add               import import_add

from dms.lecture.views_show                 import lecture_show
from dms.lecture.views_show_complete        import lecture_show_complete
from dms.lecture.views_edit                 import lecture_edit
from dms.lecture.views_add                  import lecture_add
from dms.lecture.views_manage               import lecture_manage
from dms.lecture.views_manage_browseable    import lecture_manage_browseable
from dms.lecture.views_sort                 import lecture_sort

from dms.linkitem.views_show                import linkitem_show
from dms.linkitem.views_add                 import linkitem_add
from dms.linkitem.views_edit                import linkitem_edit

from dms.linklist.views_show                import linklist_show
from dms.linklist.views_add                 import linklist_add
from dms.linklist.views_edit                import linklist_edit
from dms.linklist.views_manage              import linklist_manage
from dms.linklist.views_manage_browseable   import linklist_manage_browseable
from dms.linklist.views_sort                import linklist_sort

from dms.mediasurvey.views_show             import mediasurvey_show
from dms.mediasurvey.views_add              import mediasurvey_add
from dms.mediasurvey.views_edit             import mediasurvey_edit

from dms.newsboard.views_show               import newsboard_show
from dms.newsboard.views_add                import newsboard_add
from dms.newsboard.views_edit               import newsboard_edit
from dms.newsboard.views_manage             import newsboard_manage
from dms.newsboard.views_manage_browseable  import newsboard_manage_browseable

from dms.newsitem.views_show                import newsitem_show
from dms.newsitem.views_add                 import newsitem_add
from dms.newsitem.views_edit                import newsitem_edit

from dms.newsletter.views_show              import newsletter_show
from dms.newsletter.views_add               import newsletter_add
from dms.newsletter.views_edit              import newsletter_edit
from dms.newsletter.views_manage            import newsletter_manage
from dms.newsletter.views_manage_browseable import newsletter_manage_browseable
from dms.newsletter.views_sort              import newsletter_sort
from dms.newsletter.views_show              import newsletter_select_section
from dms.newsletter.views_show              import newsletter_send

from dms.newsletteritem.views_show          import newsletteritem_show
from dms.newsletteritem.views_add           import newsletteritem_add
from dms.newsletteritem.views_edit          import newsletteritem_edit

from dms.pinboard.views_show                import pinboard_show
from dms.pinboard.views_add                 import pinboard_add
from dms.pinboard.views_edit                import pinboard_edit
from dms.pinboard.views_manage              import pinboard_manage
from dms.pinboard.views_manage_browseable   import pinboard_manage_browseable

from dms.pinitem.views_show                 import pinitem_show
from dms.pinitem.views_add                  import pinitem_add
from dms.pinitem.views_edit                 import pinitem_edit

from dms.photo.views_show                   import photo_show
from dms.photo.views_add                    import photo_add
from dms.photo.views_edit                   import photo_edit

from dms.pool.views_show                    import pool_show
from dms.pool.views_add                     import pool_add
from dms.pool.views_edit                    import pool_edit
from dms.pool.views_manage                  import pool_manage
from dms.pool.views_manage_browseable       import pool_manage_browseable
from dms.pool.views_sort                    import pool_sort

from dms.projectgroup.views_show            import projectgroup_show
from dms.projectgroup.views_add             import projectgroup_add
from dms.projectgroup.views_edit            import projectgroup_edit
from dms.projectgroup.views_manage          import projectgroup_manage
from dms.projectgroup.views_manage_browseable  import projectgroup_manage_browseable
from dms.projectgroup.views_navigation_left    import projectgroup_navigation_left
from dms.projectgroup.views_sort            import projectgroup_sort

from dms.projectgroupemailitem.views_show          import projectgroupemailitem_show
from dms.projectgroupemailitem.views_add           import projectgroupemailitem_add
from dms.projectgroupemailitem.views_edit          import projectgroupemailitem_edit

from dms.projectgroupemail.views_show              import projectgroupemail_show
from dms.projectgroupemail.views_add               import projectgroupemail_add
from dms.projectgroupemail.views_edit              import projectgroupemail_edit
from dms.projectgroupemail.views_manage            import projectgroupemail_manage
from dms.projectgroupemail.views_manage_browseable import projectgroupemail_manage_browseable
from dms.projectgroupemail.views_sort              import projectgroupemail_sort

from dms.redirect.views_show                import redirect_show
from dms.redirect.views_add                 import redirect_add
from dms.redirect.views_edit                import redirect_edit

from dms.resource.views_show                import resource_show
from dms.resource.views_show                import resource_show_my_events
from dms.resource.views_show                import resource_del_event
from dms.resource.views_add                 import resource_add
from dms.resource.views_edit                import resource_edit
from dms.resource.views_manage              import resource_manage
#from dms.resource.views_types               import resource_manage_types
#from dms.resource.views_types               import resource_new_delete_types
from dms.resource.views_types               import resource_types_del
from dms.resource.views_types               import resource_type_new
from dms.resource.views_resources           import resource_resource_new

from dms.rssfeed.views_show                 import rssfeed_show
from dms.rssfeed.views_add                  import rssfeed_add
from dms.rssfeed.views_edit                 import rssfeed_edit

from dms.rssfeedmanager.views_show          import rssfeedmanager_show
from dms.rssfeedmanager.views_add           import rssfeedmanager_add
from dms.rssfeedmanager.views_edit          import rssfeedmanager_edit
from dms.rssfeedmanager.views_manage        import rssfeedmanager_manage
from dms.rssfeedmanager.views_manage_browseable import rssfeedmanager_manage_browseable

from dms.schoolmanagement.views_show        import schoolmanagement_show
from dms.schoolmanagement.views_add         import schoolmanagement_add
from dms.schoolmanagement.views_edit        import schoolmanagement_edit

from dms.scorm                              import scorm_show
from dms.scorm                              import scorm_show_top
from dms.scorm                              import scorm_show_left
from dms.scorm                              import scorm_show_main
from dms.scorm                              import scorm_ajax_call

from dms.searchxapian.views_ajax            import searcheduxapian_ajax_get_schlagwort

from dms.sheet.views_show                   import sheet_show
from dms.sheet.views_add                    import sheet_add
from dms.sheet.views_edit                   import sheet_edit

from dms.survey.views_show                  import survey_show
from dms.survey.views_add                   import survey_add
from dms.survey.views_edit                  import survey_edit
from dms.survey.views_manage                import survey_manage
from dms.survey.views_sort                  import survey_sort
from dms.survey.views_export                import survey_export_csv
from dms.survey.views_reset                 import survey_reset
from dms.survey.views_start                 import survey_start
from dms.survey.views_stop                  import survey_stop
from dms.survey.views_report                import survey_report
from dms.survey.views_reportsingle          import survey_reportsingle
from dms.survey.views_reportquestion        import survey_reportquestion

from dms.surveyitem.views_show              import surveyitem_show
from dms.surveyitem.views_add               import surveyitem_add
from dms.surveyitem.views_edit              import surveyitem_edit

from dms.text.views_show                    import text_show
from dms.text.views_add                     import text_add
from dms.text.views_edit                    import text_edit

from dms.todoitem.views_show                import todoitem_show
from dms.todoitem.views_add                 import todoitem_add
from dms.todoitem.views_edit                import todoitem_edit

from dms.todolist.views_show                import todolist_show
from dms.todolist.views_add                 import todolist_add
from dms.todolist.views_edit                import todolist_edit
from dms.todolist.views_manage              import todolist_manage
from dms.todolist.views_manage_browseable   import todolist_manage_browseable
from dms.todolist.views_sort                import todolist_sort

from dms.userfolder.views_show              import userfolder_show
from dms.userfolder.views_add               import userfolder_add

from dms.userchangemanagement.views_show    import userchangemanagement_show
from dms.userchangemanagement.views_add     import userchangemanagement_add
from dms.userchangemanagement.views_edit    import userchangemanagement_edit

from dms.usermanagement.views_show          import usermanagement_show
from dms.usermanagement.views_add           import usermanagement_add
from dms.usermanagement.views_edit          import usermanagement_edit
from dms.usermanagement.views_ajax          import usermanagement_ajax_get_org

from dms.usermanagementorg.views_show       import usermanagementorg_show
from dms.usermanagementorg.views_add        import usermanagementorg_add
from dms.usermanagementorg.views_edit       import usermanagementorg_edit
from dms.usermanagementorg.views_ajax       import usermanagementorg_ajax_get_org

from dms.userregistration.views_show        import userregistration_show
from dms.userregistration.views_add         import userregistration_add
from dms.userregistration.views_edit        import userregistration_edit

from dms.views_error                        import show_error

from dms.webquest.views_show                import webquest_show
from dms.webquest.views_add                 import webquest_add
from dms.webquest.views_edit                import webquest_edit
from dms.webquest.views_manage              import webquest_manage
#from dms.webquest.views_manage_browseable   import webquest_manage_browseable
from dms.webquest.views_sort                import webquest_sort
from dms.webquest.views_navigation_left     import webquest_navigation_left

from dms.wiki.views_show                    import wiki_show
from dms.wiki.views_add                     import wiki_add
from dms.wiki.views_edit                    import wiki_edit
from dms.wiki.views_manage                  import wiki_manage
from dms.wiki.views_manage_browseable       import wiki_manage_browseable

from dms.wikiitem.views_show                import wikiitem_show
from dms.wikiitem.views_show                import wikiitem_diff
from dms.wikiitem.views_add                 import wikiitem_add
from dms.wikiitem.views_edit                import wikiitem_edit

import hotshot

if 'hessen' in ORG:
  from dms.hessen.schooldb.views_show   import schooldb_show
  from dms.hessen.schooldb.views_add    import schooldb_add
  from dms.hessen.schooldb.views_edit   import schooldb_edit
  from dms.hessen.trainingdb.views_show   import trainingdb_show
  from dms.hessen.trainingdb.views_add    import trainingdb_add
  from dms.hessen.trainingdb.views_edit   import trainingdb_edit

# -----------------------------------------------------
def add_dms_object ( request, app ) :
  """ """
  # --- Gegebenenfalls wird index.html ergaenzt
  path = request.path
  if string.find(path, '.html') < 0 :
    path += 'index.html'
  # --- Das Objekt wird gesucht
  item = get_item_container(path, '/add/' + app + '/')
  # --- Die zu "app" passende Operation wird ausgefuehrt
  if item != None :
    # --- 'dmsFolder' wird zu folder_show, folder_edit etc
    return eval(app + '_add(request, item)')
  else:
    # --- Die Fehlermeldung muss noch verbessert werden
    return render_to_response ( 'error.html',
                  { 'request': request.META,
                    'content': '<p>Der Pfad ' + request.path + ' ist falsch</p>'
                  }
                )

# -----------------------------------------------------
def dispatch_dms_object(request, op=''):
  """ fuehrt die passende Operation op aus """
  #do_debug = True
  do_debug = False
  if do_debug:
    prof = hotshot.Profile("/var/log/cmsprofile/djambala.prof")
    prof.start()
  path = request.path
  # --- Das Objekt wird gesucht
  if op == '':
    my_op = op
  else :
    my_op = '/' + op + '/'
  item_container = get_item_container(path, my_op)
  if item_container == None:
    if path != '' and path[-1] != '/':
      path += '/'
    # --- Gegebenenfalls wird index.html ergaenzt
    if string.find(path, '.html') < 0:
      path += 'index.html'
    # --- Das Objekt wird gesucht
    if op == '' :
      my_op = op
    else :
      my_op = '/' + op + '/'
    item_container = get_item_container(path, my_op)
    # --- RSS-Feed ?
    if item_container == None:
      path = request.path
      name, ret_path = get_feed_name(request, op)
      feed = get_feed_by_name(name)
      if feed != None:
        return rssfeed_edit(request, feed, ret_path)

  # --- Die zu "op" passende Operation wird ausgefuehrt
  if item_container != None:
    if item_container.container.is_protected():
      user = request.user
      if not user.is_authenticated():
        return show_error(request, item_container, _('Sie sind nicht eingeloggt ...'),
                   u'', BASE_SITE_URL + '/login/?next=' + item_container.get_absolute_url(),
                   is_hint=True)
      this_role = get_role_by_user_path(user, path)
      if this_role > item_container.container.min_role_id:
        return show_error(request, item_container, _('Zugriffsrechte reichen nicht aus ...'),
                   _(u'<p>Sie sind zwar eingeloggt - Ihre Zugriffsrechte sind hier aber zu gering!</p>'),
                   is_hint=True)
    if op == '' :
      op = 'show'
    if op == 'show':
      if item_container.is_deleted:
        return show_error(request, item_container, _('Gel&ouml;schtes Objekt'),
               _(u'<p>Das Objekt ') + '<i>%s</i>' % item_container.item.name + \
                          _(' wurde entfernt!</p>') )
      if not item_container.item.app.name in ['dmsNewsItem', 'dmsEventItem']:
        today = datetime.datetime.today()
        if today < item_container.visible_start:
          return show_error(request, item_container, _('Geschlossenes Zeitfenster'),
                 _(u'<p>Das Objekt <i>%s</i> ist noch nicht sichtbar!</p>') % \
                            item_container.item.name )
        elif today > item_container.visible_end:
          return show_error(request, item_container, _('Geschlossenes Zeitfenster'),
                 _(u'<p>Das Objekt <i>%s</i> ist nicht mehr sichtbar!</p>') % \
                            item_container.item.name )
    # --- 'dmsFolder' wird zu folder_show, folder_edit etc
    if do_debug:
      result = eval(string.lower(item_container.item.app.name[3:]) + '_' + op + \
                '(request, item_container)' )
      prof.stop()
      return result
    else:
      return eval(string.lower(item_container.item.app.name[3:]) + '_' + op + \
                '(request, item_container)' )
  else:
    info = _(u'<p>Bitte informieren Sie uns, indem Sie uns die genaue Adresse angeben, bei der der Fehler auftrat.</p>\n')
    return show_error(request, item_container, _('Falsche Adresse'),
                      _(u'<p>Die Seite existiert nicht oder es trat ein Datenbankfehler auf!</p>\n') + info)

# -----------------------------------------------------
def dispatch_ajax(request, ajax_op=''):
  """ fuehrt die passende Operation op aus """
  #do_debug = True
  do_debug = False
  if do_debug:
    prof = hotshot.Profile("/var/log/cmsprofile/djambala.prof")
    prof.start()
  # --- Das Objekt wird gesucht
  if ajax_op == '':
    show_error(request, item_container, _('Falsche Ajax-Funktion'),
                      _(u'<p>Die entsprechende Ajax-Funktion existiert nicht!</p>\n') + info)
  path = request.path
  path = path[:path.find('/ajax/')]
  item_container = get_item_container(path)
  if item_container == None:
    # --- Gegebenenfalls wird index.html ergaenzt
    if string.find(path, '.html') < 0:
      path += 'index.html'
    # --- Das Objekt wird gesucht
    item_container = get_item_container(path)
  # --- Die zu "op" passende Operation wird ausgefuehrt
  if item_container != None:
    if item_container.container.is_protected():
      user = request.user
      if not user.is_authenticated():
        return show_error(request, item_container, _('Zugriffsrecht'),
                    _(u'<p>Sie sind bislang nicht eingeloggt!</p>'),
                    BASE_SITE_URL + '/login/?next=' + item_container.get_absolute_url(),
                    is_hint=True)
      this_role = get_role_by_user_path(user, path)
      i = item_container.container.min_role_id
      if this_role > item_container.container.min_role_id:
        return show_error(request, item_container, _('Zugriffsrecht'),
                          _(u'<p>Sie sind zwar eingeloggt - Ihre Zugriffsrechte sind zu gering!</p>'),
                          is_hint=True)
    if item_container.is_deleted:
      return show_error(request, item_container, _('Gelöschtes Objekt'),
              _(u'<p>Das Objekt ') + '<i>%s</i>' % item_container.item.name + \
                        _(' wurde entfernt!</p>') )
    if not item_container.item.app.name in ['dmsNewsItem', 'dmsEventItem']:
      today = datetime.datetime.today()
      if today < item_container.visible_start:
        return show_error(request, item_container, _('Geschlossenes Zeitfenster'),
                _(u'<p>Das Objekt <i>%s</i> ist noch nicht sichtbar!</p>') % \
                          item_container.item.name )
      elif today > item_container.visible_end:
        return show_error(request, item_container, _('Geschlossenes Zeitfenster'),
                _(u'<p>Das Objekt <i>%s</i> ist nicht mehr sichtbar!</p>') % \
                          item_container.item.name )
    # --- 'dmsFolder' wird zu folder_show, folder_edit etc
    if do_debug:
      result = eval(string.lower(item_container.item.app.name[3:]) + '_' + op + \
                '(request, item_container)' )
      prof.stop()
      return result
    else:
      return eval(ajax_op + '(request, item_container)' )
  else:
    info = _(u'<p>Bitte informieren Sie uns, indem Sie uns die genaue Adresse angeben, bei der der Fehler auftrat.</p>\n')
    return show_error(request, item_container, _('Falsche Adresse'),
                      _(u'<p>Die Ajax-Funktion existiert nicht oder es trat ein Datenbankfehler auf!</p>\n') + info)

