# -*- coding: utf-8 -*-
"""
/dms/resource/queries.py

.. enthaelt Abfragen einer Ressourcenverwaltung
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2008  Beginn
....  ...
0.05  09.04.2008  get_event_list
"""


from django.utils.translation import ugettext as _

from dms.models               import DmsOrg

from dms.resource.models      import DmsResourceSettings
from dms.resource.models      import DmsResourceType
from dms.resource.models      import DmsResourceResource
from dms.resource.models      import DmsResourceEvent

import string

# -----------------------------------------------------
def exist_settings_org_id(org_id):
  """ ueberprueft, ob die Organisation in der Settings-Tabelle existiert """
  
  orgs = DmsResourceSettings.objects.filter(org__org_id=org_id)
  return len(orgs)>0

# -----------------------------------------------------
def get_org_settings(org_id):
  """ liefert org.settings zurueck """
  return DmsResourceSettings.objects.filter(org__org_id=org_id).order_by('time_start')

# -----------------------------------------------------
def create_org_settings(org_id, periods_list):
  """
  Legt in der Settings-Db Zeitintervalle als 'Schulstunden' oder andere Zeiträume neu an.
  Wenn die ersten vier Zeichen der Beschreibung mit der Uhrzeit uebereinstimmen: Zeitpunkt.
  """
  dms_settings = DmsResourceSettings.objects.filter(org__org_id=org_id)
  dms_settings.delete()
  org = DmsOrg.objects.get(org_id=org_id)
  for per in periods_list:
    dms_settings            = DmsResourceSettings()
    dms_settings.org        = org
    dms_settings.time_start = per[0]
    if per[2]=='24:00':
      dms_settings.time_end   = u"23:59:59"
    else:
      dms_settings.time_end   = per[2]
    dms_settings.name       = per[1].strip()
    dms_settings.is_period  = (per[0][:5] != per[1][:5])
    dms_settings.save()
  return


# -----------------------------------------------------
def clear_org_settings(org_id):
  """
  Loescht in der Settings-Db alle Eintraege zu org_id.
  """
  dms_settings = DmsResourceSettings.objects.filter(org__org_id=org_id)
  dms_settings.delete()
  return

# -----------------------------------------------------
def exist_type_org_id(org_id):
  """ ueberprueft, ob die Organisation in der Type-Tabelle (Kategorien) existiert """
  try:
    org = DmsResourceType.objects.get(org__org_id=org_id)
    return True
  except:
    return False

# -----------------------------------------------------
def create_org_type(org_id, new_types=[]):
  """ Vorbesetzung der Typen (Kategorien) """
  if new_types==[]:
    if org_id>0:
      new_types=[_(u'Beamer'), _(u'Laptop'), _(u'Laptop-Wagen'), _(u'PC-Raum'), _(u'Medien-Raum')]
    else:
      new_types=[_(u'Beamer'), _(u'Laptop'), _(u'Raum')]
  dms_type = DmsResourceType.objects.filter(org__org_id=org_id)
  dms_type.delete()
  org = DmsOrg.objects.get(org_id=org_id)
  for t in new_types:
    dms_type             = DmsResourceType()
    dms_type.org         = org
    dms_type.description = t
    dms_type.save()
  return True

# -----------------------------------------------------
def get_type_list(org_id):
  """ Liste der in org_id verfuegbaren Typen (Kategorien) """
  return DmsResourceType.objects.filter(org__org_id=org_id)

# -----------------------------------------------------
def get_resource_list(type_id):
  """ Liste der verfuegbaren Ressourcen vom Typ (Kategorie) type_id """
  return DmsResourceResource.objects.filter(res_type=type_id)

# -----------------------------------------------------
def append_type(org_id, description):
  """ neue Kategorie """
  dms_type             = DmsResourceType()
  org = DmsOrg.objects.get(org_id=org_id)
  dms_type.org         = org
  dms_type.description = description
  dms_type.save()
  return True
# -----------------------------------------------------
def delete_type( type_id):
  """ Loescht die Kategorie """
  dms_type = DmsResourceType.objects.filter(id=type_id)
  dms_type.delete()
  return None

# -----------------------------------------------------
def get_resource(res_id):
  """ Ressource zu einer Ressourcen-Id """
  res = DmsResourceResource.objects.filter(id=res_id)
  if len(res)>0:
    return res[0]
  else:
    return None

# -----------------------------------------------------
def get_orgid_of_resource(res_id):
  """ Zur Ressource gehörige Organisations-Kennung """
  res = DmsResourceResource.objects.filter(id=res_id)
  if len(res)>0:
    return res[0].res_type.org.org_id
  else:
    return None

# -----------------------------------------------------
def get_type_of_resource(res_id):
  """ Zur Ressource gehöriger Typ (Kategorie) """
  res = DmsResourceResource.objects.filter(id=res_id)
  if len(res)>0:
    my_type = DmsResourceType.objects.filter(id=res[0].res_type_id)
    return (my_type[0].id, my_type[0].description)
  else:
    return None

# -----------------------------------------------------
def append_resource(res_type_id, description, description_more, url):
  """ neue Ressourcee """
  dms_res                  = DmsResourceResource()
  dms_res.res_type_id      = res_type_id
  dms_res.description      = description
  dms_res.description_more = description_more
  dms_res.url              = url
  dms_res.save()
  return True

# -----------------------------------------------------
def get_adm_list(org_id): # momentan nicht benutzt
  """ Liste der zur Organisation gehörenden Admins """ # ---> utils?
  # nicht mehr unterstuetzt, admin-Feld aus Tabelle loeschen!
  adm_list = []
  for t in get_type_list(org_id):
    if not (t.admin in adm_list):
      adm_list.append(t.admin)
  return adm_list

# -----------------------------------------------------
def append_event(res_id, datetime_start, datetime_end, user_id):
  """ Erzeugt eine Reservierung """
  my_event = DmsResourceEvent()
  my_event.resource_id    = res_id
  my_event.datetime_start = datetime_start
  my_event.datetime_end   = datetime_end
  my_event.user_id        = user_id
  my_event.save()
  return None

# -----------------------------------------------------
def get_event_list(res_id):
  """ Liste der Reservierungen einer bestimmten Ressource """
  return DmsResourceEvent.objects.filter(resource__id=res_id)

# -----------------------------------------------------
def get_my_events(user_id):
  """ Reservierungen einer bestimmten Person """
  return DmsResourceEvent.objects.filter(user__id=user_id).order_by('datetime_start')

# -----------------------------------------------------
def delete_old_events(days, datetime_now):
  """ Loescht alle Reservierungen, die aelter als days Tage sind """
  dms_events = DmsResourceEvent.objects.filter(datetime_end__lt=datetime_now-days)
  n = len(dms_events)
  dms_events.delete()
  return n

# -----------------------------------------------------
def delete_event(event_id):
  """ Loescht die Reservierung """
  dms_events = DmsResourceEvent.objects.filter(id=event_id)
  n = len(dms_events)
  dms_events.delete()
  return None

# -----------------------------------------------------
