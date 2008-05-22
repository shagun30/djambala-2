# -*- coding: utf-8 -*-
"""
/dms/help_document/views_show.py

.. zeigt die Hilfen zu einer Web-Applikation an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.09.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring  import SafeData, mark_safe, SafeUnicode

from django.utils.translation import ugettext as _

from dms.queries        import get_site_by_id
from dms.queries        import get_item_container
from dms.queries        import get_app

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def helpdocument_show(request, app):
  """ zeigt die kompletten Hilfetexte """

  def sort_by_description(item):
    return item[1]['title']

  # --- Objekt mit Hilfetext(en) suchen
  path = request.path.replace('form', 'formular')
  item_container = get_item_container(path, '')
  tSection = get_template('app/helpdocument/help_item.html')
  im = 'from dms.%s.help_form import help_form' % app
  try:
    exec(im)
  except:
    exec('from dms.help_form import help_form')
  site = get_site_by_id(1)
  if app == 'comment':
    description = _(u'Kommentarsystem')
  else:
    description = get_app('dms'+app).description
  my_title = _(u'Djambala-Hilfesystem')
  help_items = help_form.items()
  help_items.sort(key=sort_by_description)
  content = ''
  for help in help_items:
    if not help[1].has_key('info'):
      section = Context ( { 'help_name' : help[0],
                            'help_title': help[1]['title'],
                            'help_text' : help[1]['help'] } )
      content += tSection.render(section)
  vars = {
           'header_title': my_title,
           'title': my_title,
           'sub_title': description,
           'site': site,
           'this_site_title': my_title,
           'text': mark_safe(item_container.item.text),
           'text_more': mark_safe(item_container.item.text_more),
           'image_url': item_container.item.image_url,
           'content': mark_safe(content),
         }
  return render_to_response ( 'base_help.html', vars )
