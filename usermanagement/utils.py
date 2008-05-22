# -*- coding: utf-8 -*-
"""
/dms/user_management/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch

hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  22.01.2007  navigation_mode
0.03  06.12.2007  new_email, new_name
"""

from django.utils.translation import ugettext as _

from dms.utils          import show_link

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_main_options(item_container, manage_options=False):
  """ die verschiedenen Programmoptionen """
  from django.template.loader import get_template
  from django.template import Context
  tSection = get_template('app/folder/section.html')
  content = ''
  links = []
  base_url = item_container.get_absolute_url()
  links.append(show_link(base_url + '?op=password_reset', _(u'Kennwort zurücksetzen')))
  cSection = Context( { 'section': _(u'Serviceoptionen'), 'links': links } )
  content += tSection.render(cSection)
  if manage_options:
    my_title = _(u'Mehrere Personen verwalten')
    links = []
    links.append(show_link(base_url + '?op=members_accept', _(u'Mitglieder freischalten')))
    links.append(show_link(base_url + '?op=members_delete', 
                           _(u'Mitglieder löschen (30 Tage ohne Bestätigung)')))
    cSection = Context( { 'section': my_title, 'links': links } )
    content += tSection.render(cSection)
    my_title = _(u'Einzelpersonen verwalten')
    links = []
    links.append(show_link(base_url + '?op=member_new_org', _(u'Dienststelle ändern')))
    links.append(show_link(base_url + '?op=member_new_email', _(u'E-Mail-Adresse ändern')))
    links.append(show_link(base_url + '?op=member_delete_username', _(u'Mitglied löschen (Zugangsname)')))
    links.append(show_link(base_url + '?op=member_delete_email', _(u'Mitglied löschen (E-Mail-Adresse)')))
    links.append(show_link(base_url + '?op=member_new_name', _(u'Namen ändern')))
    cSection = Context( { 'section': my_title, 'links': links } )
  return content + tSection.render(cSection)

