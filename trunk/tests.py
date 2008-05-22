# -*- coding: utf-8 -*-
"""
/dms/tests.py

Tests fuer das Django content Management Systems

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.
"""

import unittest

from django.test.client import Client

from django.utils.translation import ugettext as _

class SimpleTest(unittest.TestCase):
  """ erster Versuch zum Testen ... """

  def setUp(self):
    self.client = Client()

  def test_details(self):
    response = self.client.get('http://dms.bildung.hessen.de/')
    self.failUnlessEqual(response.status_code, 200)
    #self.failUnlessEqual(response.context['customers'], 5)



