# -*- coding: utf-8 -*-
"""
perms.py

.. beschreibt die Rechte innerhalb des dms-Systems:
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  17.01.2007  Beginn der Arbeit
0.02  21.01.2007  perm_manage_uer
"""

from django.utils.translation import ugettext as _

from django.utils.translation import ugettext as _

perm_read             = { 'name': 'perm_read',
                          'description': _('Lesen: kann Inhalte einsehen/lesen') }
perm_add              = { 'name': 'perm_add',
                          'description': _('Schreiben: kann Inhalte erg&auml;nzen/einf&uuml;gen') }
perm_add_folderish    = { 'name': 'perm_add_folderish',
                          'description': _('Schreiben: kann strukturelle Elemente (z.B. Ordner) erg&auml;nzen') }
perm_edit             = { 'name': 'perm_edit',
                          'description': _('&Auml;ndern: kann (auch fremde) Inhalte &auml;ndern') }
perm_edit_own         = { 'name': 'perm_edit_own',
                          'description': _('&Auml;ndern: kann eigene Inhalte &auml;ndern') }
perm_edit_folderish   = { 'name': 'perm_edit_folderish',
                          'description': _('&Auml;ndern: kann strukturelle Elemente (z.B. Ordner) &auml;ndern') }
perm_manage           = { 'name': 'perm_manage',
                          'description': _('Verwalten: kann (auch fremde) Inhalte umbenennen, l&ouml;schen, ausschneiden, kopieren') }
perm_manage_own       = { 'name': 'perm_manage_own',
                          'description': _('Verwalten: kann eigene Inhalte umbenennen, l&ouml;schen, ausschneiden, kopieren') }
perm_manage_folderish = { 'name': 'perm_manage_folderish',
                          'description': _('Verwalten: kann strukturelle Elemente umbenennen, (z.B. Ordner)  l&ouml;schen, ausschneiden, kopieren') }
perm_manage_site      = { 'name': 'perm_manage_site',
                          'description': _('Site-Verwaltung: kann Sites einrichten, &auml;ndern, l&ouml;schen ...') }
perm_manage_user      = { 'name': 'perm_manage_user',
                          'description': _('User-Verwaltung: kann Community-Mitglieder in Arbeitsgruppen etc. aufnehmen') }
perm_manage_user_new  = { 'name': 'perm_manage_user_new',
                          'description': _('User-Verwaltung erweitert: kann Community-Mitglieder eintragen, l&ouml;schen, freischalten ...') }