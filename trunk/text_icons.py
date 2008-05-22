# -*- coding: utf-8 -*-
"""
/dms/text_icons.py

Text-Symbole fuer das Django content Management Systems

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.
"""

from django.utils.translation import ugettext as _

FOLDER_ICON       = u' .. <img src="/dms_media/image/action/folder_icon.gif" title="%s" />' % _(u'Ordner-Symbol')
PROJECT_ICON      = u' .. <img src="/dms_media/image/action/lock_icon.gif" title="%s" />' % _(u'Schlüssel-Symbol')
#FILE_ICON         = u' <span class="grey"><i>[Datei]</i></span>'
FILE_ICON         = u' .. <img src="/dms_media/image/action/file_icon.gif" title="%s" />' % _(u'Datei-Symbol')
FILE_DETAIL       = u' <a href="%s" class="navLink"><span class="grey">(Info)</span></a>'
#FILE_DETAIL       = u' <a href="%s"><img src="/dms_media/image/action/more.gif" /></a>'
#EXTERN_ICON       = u'<span class="red"><strong>»</strong></span> '
EXTERN_ICON       = u'<img src="/dms_media/image/action/external_link.png" title="%s" /> ' % _(u'Fenster-Symbol')
#NEW_WINDOW_ICON   = u'<span class="red"><strong>··</strong></span> '
NEW_WINDOW_ICON   = u'<img src="/dms_media/image/action/window_icon.gif" title="%s" /> ' % _(u'Fenster-Symbol')
#CONTROL_LINK      = u'<span class="red">¬</span>&nbsp;'
CONTROL_LINK      = u'<img src="/dms_media/image/action/more_icon.gif" title="%s" /> ' % _(u'Ein/Ausblende-Symbol')
#REDIRECT_ICON     = u'&raquo;'
REDIRECT_ICON     = u'<img src="/dms_media/image/action/redirect_link.gif" title="%s" /> ' % _(u'Weiterleitung')
MAIL_ICON         = u'<img src="/dms_media/image/action/mail_icon.gif" title="%s" /> ' % _(u'E-Mail')
SEPERATOR_ICON    = u'<span class="red"><b><i>::</i></b></span>'
SEPERATOR_ICON_GREY = u'<span class="grey"><b><i>::</i></b></span>'
LINK_ICON         = u'<span class="grey">»</span> '
