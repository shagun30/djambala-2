# -*- coding: utf-8 -*-
"""
/dms/folder/utils.py

.. enthaelt Hilfefunktionen fuer Ordner
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  22.01.2007  navigation_mode
0.03  21.05.2007  Entschlackung
0.04  19.06.2007  get_add_ons
0.05  12.07.2007  discussboard wurde hinzugefuegt
0.06  10.09.2007  add_if_app_available
0.07  01.10.2007  faqboard wurde hinzugefuegt (wf)
0.08  31.10.2007  this_section-Parameter
0.09  14.11.2007  newsletter wurde hinzugefuegt (wf)
"""

import string

from django.utils.translation import ugettext as _

from dms.roles          import UserEditPerms
from dms.queries        import get_folder_filtered_items

from dms.utils          import add_if_app_available

# -----------------------------------------------------
def get_folder_content(item_container, alpha_mode=False, app_types=[], this_section= '' ):
  """ .. filtert die Inhalte in <item-container> """
  items = get_folder_filtered_items(item_container, alpha_mode, app_types)
  d_sections = {}
  sections = []
  for s in string.splitfields(item_container.container.sections, '\n'):
    s = s.strip()
    if s != '':
      sections.append(s)
      d_sections[s] = []
  # --- Umsortieren
  d_sections['unknown'] = []
  for i in items:
    if this_section == '' or this_section == i.section:
      if d_sections.has_key(i.section) :
        d_sections[i.section].append(i)
      else :
        d_sections['unknown'].append(i)
  items = []
  for s in sections :
    items += d_sections[s]
  return items+d_sections['unknown'], sections, d_sections

# -----------------------------------------------------
def get_add_ons(username, path, item_container, with_projectgroup=True):
  """ liefert die Add-ons fuer Ordner und Projektgruppen """
  user_perms = UserEditPerms(username, path)
  add_ons = {}
  #--- haeufig benoetigt
  add_ons[0] = []
  add_if_app_available(item_container, add_ons[0],
             'dmsFolder',
             'index.html/add/folder/',
             _(u'Ordner'))
  add_if_app_available(item_container, add_ons[0],
             'dmsDocument',
             'index.html/add/document/',
             _(u'Informationsseite für kürzere Texte'))
  add_if_app_available(item_container, add_ons[0],
             'dmsFile',
             'index.html/add/file/',
             _(u'Datei (z.B. Word-Dokument, PDF-Datei)'))
  add_if_app_available(item_container, add_ons[0],
             'dmsImage',
             'index.html/add/image/',
             _(u'Bild, Foto, Grafik'))
  add_if_app_available(item_container, add_ons[0],
             'dmsRedirect',
             'index.html/add/redirect/',
             _(u'Verweis auf eine andere Web-Adresse'))
  # --- seltener benoetigt
  add_ons[1] = []
  if with_projectgroup:
    add_if_app_available(item_container, add_ons[1],
             'dmsProjectgroup',
             'index.html/add/projectgroup/',
             _(u'Arbeits- bzw. Lerngruppe'))
  # nur in geschuetzten Bereichen sind Aufgaben sillvoll
  if item_container.container.is_protected():
    add_if_app_available(item_container, add_ons[1],
              'dmsExercise',
              'index.html/add/exercise/',
              _(u'Aufgabe (mit Abgabemöglichkeit)'))
  add_if_app_available(item_container, add_ons[1],
             'dmsDiscussboard',
             'index.html/add/discussboard/',
             _(u'Diskussionsforum'))
  add_if_app_available(item_container, add_ons[1],
             'dmsFAQboard',
             'index.html/add/faqboard/',
             _(u'FAQ-Liste'))
  add_if_app_available(item_container, add_ons[1],
             'dmsGuestbook',
             'index.html/add/guestbook/',
             _(u'Gästebuch'))
  add_if_app_available(item_container, add_ons[1],
             'dmsGallery',
             'index.html/add/gallery/',
             _(u'Galerie'))
  add_if_app_available(item_container, add_ons[1],
             'dmsLinklist',
             'index.html/add/linklist/',
             _(u'Link-Liste'))
  add_if_app_available(item_container, add_ons[1],
             'dmsPool',
             'index.html/add/pool/',
             _(u'Materialpool'))
  add_if_app_available(item_container, add_ons[1],
             'dmsNewsboard',
             'index.html/add/newsboard/',
             _(u'Nachrichtenbrett'))
  add_if_app_available(item_container, add_ons[1],
             'dmsNewsletter',
             'index.html/add/newsletter/',
             _(u'Newsletter'))
  add_if_app_available(item_container, add_ons[1],
             'dmsPinboard',
             'index.html/add/pinboard/',
             _(u'Pinnwand'))
  add_if_app_available(item_container, add_ons[1],
             'dmsResource',
             'index.html/add/resource/',
             _(u'Ressourcenverwaltung'))
  add_if_app_available(item_container, add_ons[1],
             'dmsProjectgroupEmail',
             'index.html/add/projectgroupemail/',
             _(u'Rundschreiben'))
  add_if_app_available(item_container, add_ons[1],
             'dmsEventboard',
             'index.html/add/eventboard/',
             _(u'Terminkalender'))
  #add_if_app_available(item_container, add_ons[1],
  #             'dmsAgenda',
  #             'index.html/add/agenda/',
  #             _(u'Terminplaner f. Institutionen'))
  add_if_app_available(item_container, add_ons[1],
             'dmsToDoList',
             'index.html/add/todolist/',
             _(u'To-Do-Liste'))
  add_if_app_available(item_container, add_ons[1],
             'dmsWebquest',
             'index.html/add/webquest/',
             _(u'Webquest'))
  # --- der Rest
  add_ons[2] = []
  add_if_app_available(item_container, add_ons[2],
             'dmsEmailForm',
             'index.html/add/emailform/',
             _(u'E-Mail-Formular'))
  add_if_app_available(item_container, add_ons[2],
             'dmsSurvey',
             'index.html/add/survey/',
             _(u'Fragebogen / Erfassungsformular'))
  add_if_app_available(item_container, add_ons[2],
             'dmsFreemind',
             'index.html/add/freemind/',
             _(u'Freemind-Player'))
  add_if_app_available(item_container, add_ons[2],
             'dmsImagethumb',
             'index.html/add/imagethumb/',
             _(u'Minibild (Kontaktabzug) für Nachrichten etc.'))
  add_if_app_available(item_container, add_ons[2],
             'dmsRssFeedManager',
             'index.html/add/rssfeedmanager/',
             _(u'RSS-Feeds verwalten'))
  add_if_app_available(item_container, add_ons[2],
             'dmsText',
             'index.html/add/text/',
             _(u'Textseite (ohne HTML-Formatierungen)'))
  add_if_app_available(item_container, add_ons[2],
             'dmsLecture',
             'index.html/add/lecture/',
             _(u'Vortrag'))
  add_if_app_available(item_container, add_ons[2],
             'dmsUserFolder',
             'index.html/add/userfolder/',
             _(u'Zugriffskontrolle: Zugänge ermöglichen, löschen, ändern ...'))
  add_if_app_available(item_container, add_ons[2],
             'dmsUserChangeManagement',
             'index.html/add/userchangemanagement/',
             _(u'Zugriffskontrolle: Personendaten wie E-Mail-Adresse oder Kennwort ändern ...'))
  add_if_app_available(item_container, add_ons[2],
             'dmsWiki',
             'index.html/add/wiki/',
             _(u'Wiki'))
  # --- Site-Optionen
  add_ons[3] = []
  if user_perms.perm_manage_site:
    add_if_app_available(item_container, add_ons[3],
             'dmsUserRegistration',
             'index.html/add/userregistration/',
             _(u'Community-Mitglieder registrieren'))
    add_if_app_available(item_container, add_ons[3],
             'dmsUserManagement',
             'index.html/add/usermanagement/',
             _(u'Community-Mitglieder verwalten'))
    add_if_app_available(item_container, add_ons[3],
             'dmsUserManagementOrg',
             'index.html/add/usermanagementorg/',
             _(u'Community-Mitglieder einer Institution verwalten'))
    add_if_app_available(item_container, add_ons[3],
             'dmsElixier',
             'index.html/add/elixier/',
             _(u'Elixier-Verwaltungsprogramm'))
    add_if_app_available(item_container, add_ons[3],
              'dmsFolderProtected',
              'index.html/add/folderprotected/',
              _(u'Geschützter Ordner'))
    add_if_app_available(item_container, add_ons[3],
             'dmsMediaSurvey',
             'index.html/add/mediasurvey/',
             _(u'Medien-Fragebogen'))
    add_if_app_available(item_container, add_ons[3],
             'dmsFolderSchool',
             'index.html/add/folderschool/',
             _(u'Schulordner (Basisordner)'))
    add_if_app_available(item_container, add_ons[3],
             'dmsSchoolmanagement',
             'index.html/add/schoolmanagement/',
             _(u'Verwaltung der Schulseiten'))
    add_if_app_available(item_container, add_ons[3],
             'dmsTrainingDB',
             'index.html/add/trainingdb/',
             _(u'Suche in der Fortbildungsdatenbank'))
    add_if_app_available(item_container, add_ons[3],
             'dmsSchoolDB',
             'index.html/add/schooldb/',
             _(u'Suche in der Schul-Datenbank'))
  return user_perms, add_ons