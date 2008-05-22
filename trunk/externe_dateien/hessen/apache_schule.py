#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

.. erzeugt die Virtualhost-Eintraege der Schulen fuer Apache-Server

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  01.04.2008  Beginn der Arbeit
"""

from django.template.loader import get_template
from django.template import Context
from dms.hessen.schooldb.queries import *

def fill(s, length=45):
  """ """
  while len(s) < length:
    s += ' '
  return s

folder = {'BOW': 'bergstrasse',
          'DADI': 'darmstadt',
          'F': 'frankfurt',
          'FD': 'fulda',
          'GGMT': 'gross-gerau',
          'GIVB': 'giessen',
          'HRWM': 'hersfeld',
          'HTW': 'hochtaunus',
          'KS': 'kassel',
          'LDLM': 'lahn-dill',
          'MKK': 'main-kinzig',
          'MR': 'marburg',
          'OF': 'offenbach',
          'RTWI': 'wiesbaden',
          'SEWF': 'schwalm',
         }

tSection = get_template('app/hessen/schooldb/apache_schule.html')
regionen = get_regionen_all()
f = open('apache.txt','w')
f2 = open('named.txt','w')
for region in regionen:
  this_region = region[0]
  schulen = get_regionschulen_by_region(this_region)
  for schule in schulen:
    cSection = Context ( { 'schule': schule, 'region': folder[this_region] } )
    f.write(tSection.render(cSection))
    f.write('\n\n')
    entry = 'dms.%s.%s' % (schule.Name_Schule, schule.Name_Ort)
    entry = fill(entry) + ' 1D IN A 192.168.0.222\n'
    f2.write(entry)
f2.close()
f.close()



