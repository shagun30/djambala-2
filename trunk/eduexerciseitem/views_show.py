# -*- coding: utf-8 -*-
"""
/dms/eduexerciseitem/views_show.py

.. zeigt den Inhalt der Aufgabe in einem Lernarchiv an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  14.05.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template

from django.utils.translation import ugettext as _

from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_data_item_container
from dms.queries        import get_eduitem

from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_item_vars_show
from dms.utils_form     import get_folderish_vars_show
from dms.utils_base     import show_link

from dms.folder.utils   import get_folder_content as get_folder_folder_content
from dms.file.utils     import get_file_url
from dms.edulinkitem.views_show import get_details
from dms.eduexerciseitem.utils  import get_user_support
from dms.edufolder.utils  import get_folder_content
from dms.edufileitem.utils  import get_edu_file_url
from dms.newsboard.utils  import get_folder_content as get_newsboard_content
from dms.views_comment  import item_comment

from dms.exercise.views_show  import exercise_show
from dms_ext.extension        import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def eduexerciseitem_show(request, item_container):
  """ zeigt den Inhalt einer Aufgabe """

  app_name = 'eduexerciseitem'
  # --- Detail-Ansicht
  if request.GET.has_key('show_details'):
    vars = get_item_vars_show(request, item_container, app_name,
                              ignore_own_breadcrumb=True)
    data = get_eduitem(item_container.item)
    vars['text_more'] += get_details(item_container, True, data)
    if data.beschreibung_lang != '':
      vars['text'] += data.beschreibung_lang
    if item_container.item.has_comments:
      comments = item_comment(request, item_container=item_container)
    else:
      comments = ''
    vars['comments'] = comments
    return render_to_response ( 'base-full-width.html', vars )

  return exercise_show(request, item_container)