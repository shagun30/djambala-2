# -*- coding: utf-8 -*-
"""
/dms/exercise/views_show.py

.. zeigt den Inhalt eines Materialpools an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.05.2008  Beginn der Arbeit
0.02  08.05.2008  Anzeige der Loesungen
"""

import string

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms.settings       import MY_DOMAINS
from dms.settings       import DOWNLOAD_URL

from dms.roles          import get_user_roles
from dms.roles          import has_permission

from dms.queries        import get_site_url
from dms.queries        import is_file_by_item_container
from dms.queries        import get_parent_container
from dms.queries        import get_role_by_name

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import get_footer_email
from dms.text_icons     import FOLDER_ICON
from dms.text_icons     import NEW_WINDOW_ICON
from dms.text_icons     import FILE_DETAIL
from dms.text_icons     import EXTERN_ICON

from dms.exercise.utils import get_user_support
from dms.exercise.utils import get_points, get_points_min_max
from dms.folder.utils   import get_folder_content
from dms.file.utils     import get_file_size
from dms.file.utils     import get_file_url

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def exercise_show(request, item_container):
  """ zeigt den Inhalt eine Aufgabe """

  def get_section_view(item_container, ics, sections, is_teacher):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tPoints = get_template('app/exercise/points.html')
    tMain = get_template('app/exercise/main_document.html')
    tSection = get_template('app/exercise/section.html')
    exercise_text = content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section_exist = False
    section = '--START--'
    links = []
    headers = [1,2,3,4,5,6]
    values = [0, 0, 0, 0, 0, 0]
    points_curr = notes_curr = 0.0
    n_curr = 0
    points = get_points(item_container)
    for i in ics :
      if is_teacher or i.owner == request.user or \
         i.item.name == item_container.item.string_2 or i.item.name == item_container.item.string_1:
        if section != i.section :
          if section != unknown :
            if section != '--START--' and links != [] :
              cSection = Context ( { 'section': section, 'links': links } )
              content += tSection.render ( cSection)
            if i.section in sections :
              section = i.section
              section_exist = True
            else :
              section = unknown
            links = []
        d = {}
        if i.item.title == '':
          d['title'] = i.item.name
        else:
          d['title'] = i.item.title
        d['text'] = i.item.text
        d['text_more'] = i.item.text_more
        if i.item.app.name in ['dmsFile', 'dmsExerciseFile']:
          d['size'] = ', ' + \
                      smart_unicode(get_file_size(i, i.container.is_protected())) + ' Bytes'
          d['name'] = i.item.name
        else:
          d['size'] = ''
        if i.item.app.is_folderish :
          d['folder_icon'] = FOLDER_ICON
        else:
          d['folder_icon'] = ''
        # --- handelt es sich um ein Datei- oder Ordner-Objekt?
        if i.item.app.name in ['dmsFile', 'dmsExerciseFile', 'dmsEduFileItem']:
          if i.item.url_more_extern:
            d['extern'] = '_extern'
            d['extern_icon'] = NEW_WINDOW_ICON
          else:
            d['extern'] = ''
            d['extern_icon'] = ''
          d['url'] = get_file_url(i, i.container.is_protected())
        else:
          d['url'] = get_site_url(i, i.item.name)
        if i.section == _(u'Aufgabe'):
          exercise_text += tMain.render ( Context({'link': d}) )
        elif i.section == _(u'Musterlösung'):
          d['title'] = i.item.name
          links.append(d)
        else:
          if is_teacher:
            d['check_url'] = '%s/check/?id=%i' % (i.get_absolute_url(), i.id)
            if i.item.integer_1 > -1:
              d['check_points'] = 1.0 * i.item.integer_1 / 100.0
          d['title'] = i.owner.get_standard_name()
          links.append(d)
          if i.item.integer_1 >= 0:
            v = i.item.integer_1
            points_curr += v
            n_curr += 1
            for h in headers:
              p = points[h-1]
              min = 100*p['min'] - 50
              max = 100*p['max'] + 49
              if min <= i.item.integer_1 and i.item.integer_1 <= max:
                notes_curr += int(h)
                values[h-1] += 1
                if i.item.integer_1 < min + 75:
                  d['check_note'] = str(h) + '-'
                elif i.item.integer_1 > max - 75:
                  d['check_note'] = str(h) + '+'
                else:
                  d['check_note'] = h
    if section != '--START--' and links != []:
      if section == unknown and not section_exist:
        section = ''
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    points = get_points_min_max(points)
    if item_container.item.app.name=='dmsExercise' and item_container.item.integer_1>-1:
      max_points = item_container.item.integer_1
    elif item_container.item.app.name=='dmsEduExerciseItem' and item_container.item.integer_6>-1:
      max_points = item_container.item.integer_6
    else:
      max_points = ''
    if n_curr > 0:
      points_curr = '%6.2f' % (points_curr / (100*n_curr) )
      notes_curr = '%6.2f' % ((1.0 * notes_curr) / n_curr)
    else:
      points_curr = ''
      notes_curr = ''
    points_text = tPoints.render(Context ({'headers': headers,
                                           'points': points,
                                           'max_points': max_points,
                                           'points_curr': points_curr,
                                           'notes_curr': notes_curr,
                                           'n_curr': n_curr,
                                           'values': values }))
    return content, exercise_text, points_text

  app_name = 'exercise'
  is_teacher = has_permission(request.user, item_container.container.path, 'perm_manage_folderish')
  ics, sections, d_sections = get_folder_content(item_container, alpha_mode=True)
  content, exercise_text, points_text = get_section_view(item_container, ics, sections, is_teacher)
  vars = get_folderish_vars_show(request, item_container, app_name,
                                 content,
                                 get_user_support(item_container, request.user))
  parent = get_parent_container(item_container.container)
  vars['no_top_main_navigation'] = (parent.min_role_id < get_role_by_name('no_rights').id) or \
                                  item_container.container.nav_name_left.find('webquest') >= 0
  vars['exercise_text'] = exercise_text
  vars['points_text'] = points_text
  return render_to_response ( 'app/exercise/base_folderish.html', vars )
