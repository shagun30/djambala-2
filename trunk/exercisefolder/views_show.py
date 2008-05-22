# -*- coding: utf-8 -*-
"""
/dms/exercisefolder/views_show.py

.. zeigt den Inhalt eines Lernarchivs an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
"""

import datetime

from django.utils.encoding  import smart_unicode
from django.shortcuts   import render_to_response
from django.http        import HttpResponseRedirect
from django.template    import Context
from django.template.loader import get_template
from django.utils.safestring import SafeData, mark_safe, SafeUnicode
from django.utils.translation import ugettext as _

from dms.settings       import CURRICULUM_DOMAIN
from dms.settings       import MP3_DOMAIN
from dms.settings       import MP3_DOWNLOAD
from dms.settings       import ELIXIER_LOGOS_URL
from dms.settings       import EDUFOLDER_TRAINING_URL
from dms.settings       import EXERCISE_LAYOUT

from dms.text_icons     import SEPERATOR_ICON_GREY

from dms.text_icons     import SEPERATOR_ICON
from dms.queries        import get_lernrestyp_by_id
from dms.queries        import get_data_item_container
from dms.queries        import get_fach_by_id
from dms.queries        import get_schulart_by_id
from dms.queries        import get_base_site_url
from dms.queries        import get_site_url

from dms.utils_form     import get_folderish_vars_show
from dms.utils          import get_link_by_item_container
from dms.utils          import get_footer_email
from dms.utils_base     import show_link

from dms.folder.utils   import get_folder_content

from dms.exercisefolder.utils  import get_user_support
from dms.exercisefolder.utils  import get_main_folder_name

from dms.newsboard.utils  import get_folder_content as get_newsboard_content

from dms.edufileitem.utils  import get_edu_file_url
from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_main_folders(item_container, template_name, base_site_url):
  """ liefert die Unterordner der Hauptthemen """
  tSection = get_template('app/exercisefolder/%s/link_main.html' % template_name)
  ics, sections, d_sections = get_folder_content(item_container)
  content = ''
  n = 0
  while n < len(ics):
    vars = { 'base_site_url': base_site_url }
    vars['link_01'] = ics[n].item.name
    vars['title_01'] = ics[n].item.title
    n += 1
    if n < len(ics):
      vars['link_02'] = ics[n].item.name
      vars['title_02'] = ics[n].item.title
      n += 1
    content += tSection.render(Context(vars))
  return content

# -----------------------------------------------------
def get_sub_folders(item_container):
  """ liefert die Unterordner der Unterthemen """
  ics, sections, d_sections = get_folder_content(item_container)
  sub_items = []
  for ic in ics:
    sub_items.append( {'link': ic.item.name, 'title': ic.item.title })
  return sub_items

# -----------------------------------------------------
def get_sub_sub_content(item_container, template_name, base_site_url):
  """ liefert die Verweise auf die Inhalte """
  tSection = get_template('app/exercisefolder/%s/link_content.html' % template_name)
  ics, sections, d_sections = get_folder_content(item_container)
  content = ''
  n = 5
  for ic in ics:
    vars = { 'base_site_url': base_site_url }
    vars['link'] = ic.item.name
    vars['title'] = ic.item.title
    vars['content'] = ic.item.text
    vars['difficulty'] = n
    vars['class_no'] = n - 1
    if ic.item.image_url != '':
      vars['link_image'] = ic.item.image_url
    else:
      vars['link_image'] = base_site_url + '/dms_media/image/exercisefolder/mauswiesel/ergebniss_platzhalter.jpg'
    content += tSection.render(Context(vars))
    n -= 1
  return content

# -----------------------------------------------------
def exercisefolder_show(request, item_container):
  """ zeigt den Inhalt eines Lernarchivs """

  # --- Soll an eine andere Adresse weitergeleitet werden?
  if item_container.item.string_1 != '':
    return HttpResponseRedirect(item_container.item.string_1)

  # {{ base_site_url }}/dms_media/skin_style/{{site.skin_style}}/image_{{site.skin_style}}_edit.jpg
  app_name = 'exercisefolder'
  content = ''
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container))
  vars['footer_email'] = get_footer_email(item_container, class_link='')
  template_name = EXERCISE_LAYOUT[0][1]
  if item_container.item.integer_2 == 0: # Startseite der Aufgabensammlung
    return render_to_response ( 'app/exercisefolder/%s/index.html' % template_name, vars )
  elif item_container.item.integer_2 == 1: # Hauptthemen
    vars['main'] = item_container.item.name
    vars['main_folders'] = get_main_folders(item_container, template_name, vars['base_site_url'])
    return render_to_response ( 'app/exercisefolder/%s/index_main.html' % template_name, vars )
  elif item_container.item.integer_2 == 2: # Unterthemen
    vars['main'] = get_main_folder_name(item_container)
    vars['sub'] = item_container.item.name
    vars['sub_items'] = get_sub_folders(item_container)
    return render_to_response ( 'app/exercisefolder/%s/index_sub.html' % template_name, vars )
  elif item_container.item.integer_2 == 3: # Inhaltsuebersicht
    vars['main'] = get_main_folder_name(item_container)
    vars['sub'] = item_container.get_parent().item.name
    vars['sub_title'] = item_container.get_parent().item.title
    vars['sub_sub_title'] = item_container.item.title
    vars['sub_sub_content'] = get_sub_sub_content(item_container, template_name, vars['base_site_url'])
    return render_to_response ( 'app/exercisefolder/%s/index_sub_sub.html' % template_name, vars )
  assert False
