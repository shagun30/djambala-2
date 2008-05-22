# -*- coding: utf-8 -*-
"""
/dms/elixier/views_statistik.py

.. zeigt statistische Informationen der Elixier-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.07.2007  Beginn der Arbeit
0.02  25.10.2007  get_edu_fach_id_by_name
"""

from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.roles          import require_permission
from dms.utils_form     import get_item_vars_show
from dms.utils          import show_link
from dms.queries        import get_edu_fach_id_by_name

from dms.elixier.queries  import get_total_item_count
from dms.elixier.queries  import get_accepted_total_item_count
from dms.elixier.queries  import get_rejected_total_item_count
from dms.elixier.queries  import get_fach_sachgebiete_as_single

# -----------------------------------------------------
@require_permission('perm_manage')
def views_statistik(request,item_container, op):
  """ zeigt statistische Informationen der Elixier-Datenbank an """

  BACK_URL = show_link(item_container.get_absolute_url(), _(u'Zurück zur Übersicht ...'))

  def get_stat_items(op):
    
    def get_values(fach_id=-1):
      total = get_total_item_count(fach_id)
      accepted = get_accepted_total_item_count(fach_id)
      rejected = get_rejected_total_item_count(fach_id)
      return total, accepted, rejected, total-accepted-rejected

    title = ''
    items = []
    if op == 'gesamt_statistik':
      title = _(u'Gesamtstatistik der Elixier-Datenbank')
      total, accepted, rejected, unknown = get_values()
      items.append ( { 'info': _(u'Alle Elixier-Beiträge'),
                       'total': total, 'accepted': accepted, 'rejected': rejected,
                       'unknown': unknown } )
    elif op == 'fach_statistik':
      t_total = t_accepted = t_rejected = t_unknown = 0
      title = _(u'Fachstatistik der Elixier-Datenbank')
      faecher = get_fach_sachgebiete_as_single()
      for fach in faecher:
        fach_id = get_edu_fach_id_by_name(fach)
        if fach_id > 0:
          total, accepted, rejected, unknown = get_values(fach_id)
          t_total += total
          t_accepted += accepted
          t_rejected += rejected
          t_unknown += unknown
          items.append ( { 'info': fach,
                           'total': total, 'accepted': accepted, 'rejected': rejected,
                           'unknown': unknown } )
      items.append ( { 'info': _(u'<b>Gesamtstatistik</b>'),
                       'total': t_total, 'accepted': t_accepted, 'rejected': t_rejected,
                       'unknown': t_unknown } )
    return title, items, get_total_item_count(-1)

  def get_stat_infos(op):
    """ zeigt statistische Informationen der Elixier-Datenbank """
    from django.template.loader import get_template
    from django.template import Context
    t_statistik = get_template('app/elixier/base_statistik.html')
    title, items, total = get_stat_items(op)
    statistik_context = Context (  { 'title': title, 'items': items, 'total': total, 'next': BACK_URL } )
    return t_statistik.render(statistik_context)

  app_name = 'elixier'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['text'] = ''
  vars['text_more'] = ''
  vars['content'] = get_stat_infos(op)
  vars['is_sortable_table'] = True
  return render_to_response ( 'app/base_folderish.html', vars )
