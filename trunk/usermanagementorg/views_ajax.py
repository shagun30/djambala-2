#-*-coding: utf-8 -*-
"""
/dms/usermanagementorg/views_ajax.py

.. enthaelt Ajax-Funktion fuer User-Management der Institutionen
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  18.04.2008  Beginn der Arbeit
"""

import time

from django.http              import HttpResponse
from django.shortcuts         import render_to_response
from django.template.loader   import get_template
from django.template          import Context

from django.utils.translation import ugettext as _

from dms.roles                import require_permission
from dms.queries              import get_org_by_name

from dms.utils_base           import ACL_USERS

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_user_new')
def usermanagementorg_ajax_get_org(request, item_container):
  """ moegliche Organisationen """
  orgs = get_org_by_name(request.GET['query'], False)
  res = '<orgs>\n'
  for org in orgs:
    res += '<org_item>\n<name><![CDATA[%s, %s, %s]]></name>\n</org_item>\n' % (org.organisation, org.town, org.zip)
  res += '</orgs>\n'
  return HttpResponse(res, mimetype="text/xml; charset=utf-8")
