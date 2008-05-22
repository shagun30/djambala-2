#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  23.04.2008  Beginn der Arbeit
"""

import datetime

from dms.auth.models    import User
from dms.models         import DmsAudit

from dms.settings import *

last_date = datetime.datetime.now() - datetime.timedelta(30)

audits = DmsAudit.objects.filter(modified__lt=last_date)

audits.delete()