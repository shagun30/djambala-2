# -*- coding: utf-8 -*-
"""
/dms/utilities/help_form.py

.. enthaelt die kompletten Kontext-Hilfetexte fuer Info-Manager
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.10.2007  Beginn der Arbeit
"""

from django.utils.translation import ugettext as _

from dms.help_form_base   import get_help_form

help_form = get_help_form()

# ----------------------------------------------------------------
help_form['edu_object'] = {
     'title'      : _('Art der Lernresource'),
     'help'       : _("""<p>
W&auml;hlen Sie bitte die Lernresource(n) aus, deren Besitzer
ge&auml;ndert werden soll.
</p>""") }

# ----------------------------------------------------------------
help_form['app_object'] = {
     'title'      : _('Art der Web-Ressource'),
     'help'       : _("""<p>
W&auml;hlen Sie bitte hier die Art der Web-Resource, nach der Sie suchen.
</p>""") }

# ----------------------------------------------------------------
help_form['app_name'] = {
     'title'      : _('Name der Ressourcen'),
     'help'       : _("""<p>
Tragen Sie hier gegebenenfalls den Namen der gesuchten Ressource ein.
</p>""") }

# ----------------------------------------------------------------
help_form['complete_mode'] = {
     'title'      : _('Alle Lernresourcen'),
     'help'       : _("""<p>
Aktivieren Sie diesen Schalter, falls auch alle in diesem Ordner enthaltenen
Lernresourcen ge&auml;ndert werden sollen.
</p>""") }

# ----------------------------------------------------------------
help_form['user_old'] = {
     'title'      : _('Alter Besitzer'),
     'help'       : _("""<p>
Tragen Sie hier bitte gegebenenfalls den alten Zugangsnamen ein.
Sie k&ouml;nnen dieses Feld auch leer lassen.
</p>""") }

# ----------------------------------------------------------------
help_form['user_new'] = {
     'title'      : _('Neuer Besitzer'),
     'help'       : _("""<p>
Tragen Sie hier bitte den neuen Zugangsnamen ein.
</p>""") }

# ----------------------------------------------------------------
help_form['tab_base'] = {
     'title'      : _('Basisdaten'),
     'info'       : _("""<p>
Mit diesem Formular legen Sie die Person fest, die als
neue Besitzerin bzw. neuer Besitzer eingetragen werden soll. 
</p>
<ul>
<li><b>Diese Funktion arbeitet in der Regel rekursiv, wirkt also auch in allen
Unterordnern.</b></li>
<li><b>Diese Funktion besitzt keine Undo-Funktion!</b></li>
</ul>""") }

# ----------------------------------------------------------------
help_form['tab_find_base'] = {
     'title'      : _('Basisdaten'),
     'info'       : _("""<p>
Mit diesem Formular legen Sie die Art der Web-Ressource fest, nach
der Sie suchen.
</p>""") }

