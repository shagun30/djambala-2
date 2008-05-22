# -*- coding: utf-8 -*-
"""
/dms/elixier/views_show.py

.. zeigt Inhalte der Elixier-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.07.2007  Beginn der Arbeit
0.02  19.07.2007  Dispatcher
"""

from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.utils_form     import get_item_vars_show
from dms.roles          import require_permission
from dms.utils          import show_link
from dms.views_error    import show_error

from dms.elixier.views_statistik  import views_statistik
from dms.elixier.views_beitraege  import views_beitraege
from dms.elixier.views_beitraege  import views_select_dest

# -----------------------------------------------------
@require_permission('perm_add')
def elixier_show(request,item_container):
  """ zeigt Inhalte der Elixier-Datenbank an """

  def get_section_view():
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    content = ''
    # --- Daten
    links = []
    links.append(show_link(item_container.get_absolute_url() + '?elixier_op=fach_beitraege',
                           _(u'Fachbeiträge sichten')))
    cSection = Context ( { 'section': _(u'Elixier-Daten'), 'links': links } )
    content += tSection.render ( cSection)
    # --- Statistik
    links = []
    links.append(show_link(item_container.get_absolute_url() + \
                           '?elixier_op=gesamt_statistik',
                           _(u'Elixier-Gesamtstatistik')))
    links.append(show_link(item_container.get_absolute_url() + '?elixier_op=fach_statistik',
                           _(u'Elixier-Fachstatistik')))
    cSection = Context ( { 'section': _(u'Elixier-Statistik'), 'links': links } )
    content += tSection.render ( cSection)
    return content

  get = request.GET.copy()
  if get.has_key('elixier_op'):
    if get['elixier_op'] in ['gesamt_statistik', 'fach_statistik']:
      return views_statistik(request, item_container, get['elixier_op'])
    elif get['elixier_op'] == 'fach_beitraege':
      return views_beitraege(request, item_container, get['elixier_op'])
    elif get['elixier_op'] == 'select_dest':
      return views_select_dest(request, item_container, get['elixier_op'])
    else:
      return show_error(request, item_container, _(u'Fehlende Elixier-Funktion'),
                 '<p>%s: "%s"</p>' % (_(u'Die folgende Elixier-Funktion existiert nicht'),
                                           get['elixier_op']) )
  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['content'] = get_section_view()
  return render_to_response ( 'app/base_folderish.html', vars )
