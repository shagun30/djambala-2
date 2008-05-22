import codecs

from dms.settings import *
from dms.mediasurvey.models   import DmsMediaSurvey
from dms.encode_decode  import decode_html

import string
import MySQLdb

HOST     = DATABASE_SCHOOL_HOST
USER     = DATABASE_SCHOOL_USER
PASSWD   = DATABASE_SCHOOL_PASSWORD
DB_DMS   = DATABASE_SCHOOL_NAME

def write_csv(ssa, org_id, ok, name):
  return '"%s";%i;%i,"%s"' % (ssa, org_id, ok, name)

def get_alle_schulen():
  db = MySQLdb.connect ( host=HOST, user=USER, passwd=PASSWD, db=DB_DMS )
  query = """SELECT sta.Schul_Nr, sta.NameSchule, sta.Schulamt
             FROM Schulstamm=sta,Schulstelle=ste
             WHERE ste.SchulID = sta.ID AND ste.Standort_Kz=0 AND ste.Loesch_Datum = ''
             ORDER BY sta.Schulamt, Schul_nr
          """
  cs  = db.cursor()
  cs.execute(query)
  rows = cs.fetchall()
  cs.close()
  db.close()
  return rows

schulen = get_alle_schulen()

answered = 0
f = codecs.open('/tmp/medienfragebogen.csv', 'w', 'utf8')
for schule in schulen:
  items = DmsMediaSurvey.objects.filter(org_id=schule[0])
  try:
    s = decode_html(schule[1])
  except:
    s = schule[1]
  if len(items) > 0:
    f.write(write_csv(schule[2], schule[0], 1, s))
    answered += 1
  else:
    f.write(write_csv(schule[2], schule[0], 0, s))
  f.write('\n')

f.close()
print answered