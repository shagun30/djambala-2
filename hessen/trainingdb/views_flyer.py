# -*- coding: utf-8 -*-
"""
/dms/hessen/trainingdb/views_flyer.py

.. zeigt den Flyer einer Veranstaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.02.2008  Beginn der Arbeit
0.02  14.05.2008  show_error
"""

from django.template.loader   import get_template
from django.template          import Context
from django.core.mail         import EmailMultiAlternatives
from django                   import newforms as forms
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.settings       import CONTROL_EMAIL
from dms.utils_form     import get_item_vars_show
from dms.utils          import get_tabbed_form
from dms.hessen.trainingdb.queries    import get_anbieter_by_iq_id
from dms.hessen.trainingdb.queries    import get_veranstaltung_by_iq_id
from dms.hessen.trainingdb.queries    import get_faecher_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_schularten_by_veranst_iq_id
from dms.hessen.trainingdb.queries    import get_zielgruppen_by_veranst_iq_id

from dms.hessen.trainingdb.utils      import get_datum
from dms.hessen.trainingdb.utils      import get_schularten_str
from dms.hessen.trainingdb.utils      import get_zielgruppen_str
from dms.hessen.trainingdb.utils      import get_faecher_str

from dms.hessen.trainingdb.help_form  import help_form

from dms.views_error                  import show_error
from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def trainingdb_show_flyer(request, item_container, veranst_iq_id):
  """ zeigt Flyer zur Veranstaltung """
  item = get_veranstaltung_by_iq_id(veranst_iq_id)
  if item == None:
    return show_error(request, item_container, _(u'Falsche Veranstaltung'),
                _(u'<p>Die betreffende Veranstaltung existiert nicht (mehr) in der Datenbank!</p>'))

  anbieter = '%s<br />%s<br />%s %s' % (item[1].anbieter_name,
                                        item[1].anbieter_strasse,
                                        item[1].anbieter_plz,
                                        item[1].anbieter_ort)
  app_name = u'trainingdb'
  vars = get_item_vars_show(request, item_container, app_name)
  # --- Zeitraum zusammenbauen
  if item[0].veranst_status in ['', 'freigegeben']:
    status = ''
  else:
    status = item[0].veranst_status
  if item[0].veranst_anmeldung != None:
    anmeldung = item[0].veranst_anmeldung.strftime('%d.%m.%Y')
  else:
    anmeldung = ''
  vars['thema'] = item[0].veranst_thema
  vars['beschreibung'] = mark_safe(item[0].veranst_beschreibung.replace('\n', '<br />\n'))
  vars['zeitraum'] = get_datum(item)
  vars['faecher'] = get_faecher_str(get_faecher_by_veranst_iq_id(veranst_iq_id))
  vars['zielgruppen'] = get_zielgruppen_str(get_zielgruppen_by_veranst_iq_id(veranst_iq_id))
  vars['schularten'] = get_schularten_str(get_schularten_by_veranst_iq_id(veranst_iq_id))
  vars['veranst_ort'] = item[0].veranst_ort
  vars['veranst_punkte'] = item[0].veranst_punkte
  vars['veranst_kosten'] = item[0].veranst_kosten
  vars['veranst_intern_id'] = item[0].veranst_intern_id
  vars['veranst_iq_id'] = item[0].veranst_iq_id
  vars['veranst_hinweise'] = mark_safe(item[0].veranst_hinweise.replace('\n', '<br />\n'))
  vars['veranst_zusatz'] = mark_safe(item[0].veranst_zusatz.replace('\n', '<br />\n'))
  vars['veranst_url'] = item[0].veranst_url
  vars['veranst_url_text'] = item[0].veranst_url_text
  vars['veranst_leitung'] = item[0].veranst_leitung
  vars['veranst_dozenten'] = item[0].veranst_dozenten
  vars['veranst_fest_teilnehmer'] = item[0].veranst_feste_teilnehmer
  vars['veranst_status'] = status
  vars['veranst_v_art'] = item[2].v_art_name
  vars['anbieter_url'] = item[1].anbieter_url
  vars['anbieter_name'] = item[1].anbieter_name
  vars['anbieter_person'] = item[1].anbieter_person
  vars['anbieter_strasse'] = item[1].anbieter_strasse
  vars['anbieter_plz'] = item[1].anbieter_plz
  vars['anbieter_ort'] = item[1].anbieter_ort
  vars['anbieter_telefon'] = item[1].anbieter_telefon
  vars['anbieter_fax'] = item[1].anbieter_fax
  vars['anbieter_email'] = item[1].anbieter_email
  return render_to_response ( 'app/hessen/trainingdb/show_flyer.html', vars )
