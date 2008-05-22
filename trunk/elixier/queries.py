# -*- coding: utf-8 -*-
"""
/dms/elixier/queries.py

.. enthaelt Anfragen an die Elixier-Datenbank
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.07.2007  Beginn der Arbeit
0.02  19.07.2007  Dispatcher
"""

import string

from django.utils.translation import ugettext as _

from dms.encode_decode      import encode_html
from dms.encode_decode      import decode_html

from dms.elixier.models   import DmsElixierBildungsebene
from dms.elixier.models   import DmsElixierFach
from dms.elixier.models   import DmsElixierItem
from dms.elixier.models   import DmsElixierMedienformat
from dms.elixier.models   import DmsElixierOrg
from dms.elixier.models   import DmsElixierQuelle

# -----------------------------------------------------
def get_total_count(fach=''):
  """ .. liefert die Anzahl aller enthaltenen Beitraege in der Elixier-Datenbank """
  if fach == '':
    return DmsElixierOrg.objects.all().count()
  else:
    return DmsElixierOrg.objects.filter(fach_sachgebiet__icontains=fach).count()

# -----------------------------------------------------
def get_total_item_count(fach_id):
  """ .. liefert die Anzahl aller enthaltenen Beitraege in der Elixier-Datenbank """
  if fach_id == -1:
    return DmsElixierItem.objects.count()
  else:
    return DmsElixierItem.objects.filter(fach_sachgebiet=fach_id).count()

# -----------------------------------------------------
def get_accepted_total_item_count(fach_id=-1):
  """ .. liefert die Anzahl der uebernommenen Beitraege in der Elixier-Datenbank """
  if fach_id == -1:
    return DmsElixierItem.objects.filter(status=1).count()
  else:
    return DmsElixierItem.objects.filter(status=1).filter(fach_sachgebiet=fach_id).count()

# -----------------------------------------------------
def get_rejected_total_item_count(fach_id=-1):
  """ .. liefert die Anzahl der abgelehnten Beitraege in der Elixier-Datenbank """
  if fach_id == -1:
    return DmsElixierItem.objects.filter(status=-1).count()
  else:
    return DmsElixierItem.objects.filter(status=-1).filter(fach_sachgebiet=fach_id).count()

# -----------------------------------------------------
def get_fach_sachgebiete():
  """ .. liefert die in der Elixier-Datenbank vorhandenen Fach/Sachgebiete """
  return DmsElixierOrg.objects.values('fach_sachgebiet').distinct().order_by('fach_sachgebiet')

# -----------------------------------------------------
def get_fach_sachgebiete_as_single():
  """ .. liefert die in der Elixier-Datenbank vorhandenen Fach/Sachgebiete """
  faecher = get_fach_sachgebiete()
  items = {}
  for fach in faecher:
    arr = string.splitfields(decode_html(fach['fach_sachgebiet']), ';')
    for f in arr:
      if f != '':
        f = encode_html(f.strip())
        if not items.has_key(f):
          items[f] = True
  ret = items.keys()
  ret.sort()
  return ret

# -----------------------------------------------------
def get_elixier_table_items(table_name):
  """ """
  if table_name == 'bildungsebene':
    return DmsElixierBildungsebene.objects.all().order_by('name')
  elif table_name == 'fach_sachgebiet':
    return DmsElixierFach.objects.all().order_by('name')
  elif table_name == 'medienformat':
    return DmsElixierMedienformat.objects.all().order_by('name')
  elif table_name == 'quelle':
    return DmsElixierQuelle.objects.all().order_by('name')
  else:
    return []

# -----------------------------------------------------
def get_elixier_filtered_items(bildungsebene, fach_sachgebiet, medienformat,
                               quelle, schlagwort, status=-2):
  """ liefert die Elixier-Datensaetze, die zum Suchmuster passen """
  fach = DmsElixierFach.objects.get(id=fach_sachgebiet)
  q = DmsElixierOrg.objects.filter(fach_sachgebiet__icontains=fach)
  if bildungsebene != None and bildungsebene != '':
    bildungsebene = DmsElixierBildungsebene.objects.get(id=bildungsebene)
    q = q.filter(bildungsebene__icontains=bildungsebene)
  if medienformat != None and medienformat != '':
    medienformat = DmsElixierMedienformat.objects.get(id=medienformat)
    q = q.filter(medienformat__icontains=medienformat)
  if quelle != None and quelle != '':
    quelle = DmsElixierQuelle.objects.get(id=quelle)
    q = q.filter(quelle_id__iexact=quelle)
  if schlagwort != None and schlagwort != '':
    q = q.filter(schlagwort__icontains=schlagwort)
  if status > -2 and status < 2:
    # durch die Brust ins Auge !!
    current_items = q.values('id_local')
    l1 = []
    for c in current_items:
      l1 += c.values()
    exclude_items = DmsElixierItem.objects.values('id_local').\
                       filter(id_local__in=l1).\
                       exclude(status=status)
    l2 = []
    for e in exclude_items:
      l2 += e.values()
    #assert (status == 0)
    return q.exclude(id_local__in=l2).order_by('-letzte_aenderung')
  return q.order_by('-letzte_aenderung')

# -----------------------------------------------------
def get_elixier_data():
  """ ..liefert alle Elixier-Datensaetze """
  return DmsElixierOrg.objects.all()

# -----------------------------------------------------
def get_elixier_items():
  """ ..liefert alle Elixier-Datensaetze """
  return DmsElixierItem.objects.all()

# -----------------------------------------------------
def get_elixier_org_by_id_local(id_local):
  """ ..liefert den zu id_local passenden Datensatz """
  items = DmsElixierOrg.objects.filter(id_local=id_local)
  if len(items) > 0:
    return items[0]
  else:
    return None

# -----------------------------------------------------
def get_elixier_item(item_id):
  """ ..liefert den zu item-id passenden Datensatz """
  res = DmsElixierOrg.objects.get(id=item_id)
  item = DmsElixierItem.objects.get(id_local=res.id_local)
  return res, item

# -----------------------------------------------------
def get_elixier_item_status(id_local):
  """ .. liefert den Status zu <id_local> oder None """
  items = DmsElixierItem.objects.filter(id_local=id_local)
  if len(items) > 0:
    return items[0]
  else:
    return None

# -----------------------------------------------------
def set_elixier_item_status(item, status):
  """ .. aendert den Status des Elixier-Beitrags """
  #id = item.id_local
  item.status = status
  item.save()

# -----------------------------------------------------
def change_elixier_item_status(id_local, status):
  """ .. aendert den Status des Elixier-Beitrags """
  item = get_elixier_item_status(id_local)
  if item != None:
    item.status = status
    item.save()

# -----------------------------------------------------
def set_elixier_item_fach_sachgebiet(item, fach_sachgebiet):
  """ .. aendert den Status des Elixier-Beitrags """
  #id = item.id_local
  item.fach_sachgebiet = fach_sachgebiet
  item.save()

# -----------------------------------------------------
def append_elixier_item_status(id_local, status, fach_sachgebiet):
  """ .. aendert den Status des Elixier-Beitrags """
  self = DmsElixierItem()
  self.id_local = id_local
  self.status = status
  self.fach_sachgebiet = fach_sachgebiet
  self.save()


