#!/usr/local/bin/python

"""
export_mysql_2_postgres.py

Konvertiert sql-Tabellen des dms_db-Datenbank

0.01    vom 01.06.2007
"""

import MySQLdb

HOST    = "localhost"
USER    = "root"
PASSWD  = "Geheim"
DB_VM   = "dms_db"

def doMain():
  """
  """
  db = MySQLdb.connect ( host=HOST, user=USER, passwd=PASSWD, db=DB_VM )
  cs  = db.cursor()
  # --- Tabellennamen
  tables = []
  query = """show tables"""
  cs.execute(query)
  rows = cs.fetchall()
  for row in rows:
    tables.append(row[0])
  # --- Feldnamen
  d_tables = {}
  for table in tables:
    fields = []
    query = """show fields from %s""" % table
    cs.execute(query)
    rows = cs.fetchall()
    for row in rows:
      #print table, row
      id = row[0]
      field_type = row[1]
      n_pos = field_type.find('(')
      if n_pos > -1:
        field_type = field_type[:n_pos]
      if field_type == 'tinyint':
        field_type = 'boolean'
      fields.append( (id, field_type) )
    d_tables[table] = fields
  # --- insert-Daten schreiben
  for table in tables:
    insert = 'INSERT into %s (' % table
    #print d_tables
    fields = d_tables[table]
    show_comma = False
    for field in fields:
      if show_comma:
        insert += ','
      else:
        show_comma = True
      insert += field[0]
    insert += ') VALUES('
    query = """select * from %s""" % table
    cs.execute(query)
    rows = cs.fetchall()
    data = ''
    n = 0
    for row in rows:
      data = ''
      for r in row:
        if data != '':
          data += ','
        if fields[n][1] in ['smallint', 'int', 'bigint']:
          data += str(r)
        elif fields[n][1] in ['varchar', 'char', 'text', 'longtext']:
          r = r.replace("'", "\\'")
          data += "'" + r + "'"
        elif fields[n][1] in ['date', 'datetime']:
          data += "'" + str(r) + "'"
        elif fields[n][1] in ['boolean']:
          if r == 1:
            data += 'true'
          else:
            data += 'false'
        else:
          print "UNBEKANNT", fields[n]
        n += 1
      n = 0
      print insert + data + ');'
  cs.close ()
  db.close ()

# ---------- Hauptprogramm

if __name__ == '__main__':
  doMain ()

