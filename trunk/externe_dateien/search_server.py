#!/usr/bin/python
#-*-coding: utf-8 -*-
#
# Vgl. http://www.thesamet.com/blog/2007/02/04/pumping-up-your-applications-with-xapian-full-text-search/

import xapian
import string
import re

from twisted.web import xmlrpc, server
from twisted.internet import reactor, task

DEFAULT_SEARCH_FLAGS = (
        xapian.QueryParser.FLAG_BOOLEAN |
        xapian.QueryParser.FLAG_PHRASE |
        xapian.QueryParser.FLAG_LOVEHATE |
        xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
        xapian.QueryParser.FLAG_WILDCARD
        )

URL   = 0
TITLE = 1
DATE  = 2

WORD_RE = re.compile(r"[\w{1,32}]", re.U)

def p_alnum(c):
    return (c in string.ascii_letters + '*äöüßÄÖÜ' or c in string.digits)

class SearchServer(xmlrpc.XMLRPC):

    def __init__(self, db):
        xmlrpc.XMLRPC.__init__(self)
        self.db = xapian.Database(db)
        self.parser = xapian.QueryParser()
        self.stem = xapian.Stem('german2')
        self.parser.set_stemmer(self.stem)
        # make sure database is reloaded every 10 minutes
        lc = task.LoopingCall(self.reopen_db)
        lc.start(600)

    def reopen_db(self):
        try:
            self.db.reopen()
        except IOError:
            print "Unable to open database"

    def get_extra_query(self, items, item_name):
        """ Auswertung der Zusatzparameter """
        q = ''
        for i in items:
            if q != '':
                q += ' OR '
            q += ' ' + item_name + ':' + i
        return q

    def xmlrpc_search(self, query, offset, count, domain, mode=-1, ascending=True):
        """Search the database for <query>, return
        results[offest:offset+count], sorted by relevancy"""
        q = ''
        arr = string.splitfields(query, ' ')
        for s in arr:
          word = s.strip()
          if word != '':
            q += self.stem(word) + ' '
        database = xapian.Database('/data/xapian_db/')
        enquire = xapian.Enquire(database)
        if mode >= 0:
          #enquire.set_sort_by_value_then_relevance(mode, ascending)
          enquire.set_sort_by_value(mode, ascending)
        #stem = xapian.Stem("german")
        self.parser.set_default_op(xapian.Query.OP_AND)
        qp = xapian.QueryParser()
        qp.set_default_op(xapian.Query.OP_AND)
        qp.add_boolean_prefix('user', 'X1')
        qp.add_boolean_prefix('site', 'X2')
        qp.set_database(database)
        if domain == '':
          query = qp.parse_query(q, DEFAULT_SEARCH_FLAGS)
          print q
        else:
          query = qp.parse_query(q + ' site:' + domain, DEFAULT_SEARCH_FLAGS)
          print q + ' site' + domain
        enquire.set_query(query)
        try:
          mset = enquire.get_mset(offset, count)
        except IOError, e:
          if "DatabaseModifiedError" in str(e):
            self.reopen_db()
          raise

        results = []
        #print query
        for m in mset:
          results.append(
            {'percent': m[xapian.MSET_PERCENT],
             'url'    : m[xapian.MSET_DOCUMENT].get_value(URL),
             'title'  : m[xapian.MSET_DOCUMENT].get_value(TITLE),
             'date'   : m[xapian.MSET_DOCUMENT].get_value(DATE)})
        #print len(results)
        return {"count": mset.get_matches_upper_bound(), "results": results}

    def xmlrpc_search_edu(self, query, offset, count, domain, lernrestyp, fach,
                          zielgruppe, schulart, schulstufe, sprache, schlagwort,
                          mode=-1, ascending=True):
        """Search the database for <query>, return
        results[offest:offset+count], sorted by relevancy"""
        q = ''
        arr = string.splitfields(query, ' ')
        for s in arr:
          word = s.strip()
          if word != '':
            q += self.stem(word) + ' '
        database = xapian.Database('/data/xapian_db/')
        enquire = xapian.Enquire(database)
        if mode >= 0:
          #enquire.set_sort_by_value_then_relevance(mode, ascending)
          enquire.set_sort_by_value(mode, ascending)
        #stem = xapian.Stem("german")
        self.parser.set_default_op(xapian.Query.OP_AND)
        qp = xapian.QueryParser()
        qp.set_default_op(xapian.Query.OP_AND)
        qp.add_boolean_prefix('user', 'X1')
        qp.add_boolean_prefix('site', 'X2')
        qp.add_boolean_prefix('fach', 'X3')
        qp.add_boolean_prefix('zielgruppe', 'X4')
        qp.add_boolean_prefix('schulstufe', 'X5')
        qp.add_boolean_prefix('schulart', 'X6')
        qp.add_boolean_prefix('sprache', 'X7')
        qp.add_boolean_prefix('schlagwort', 'X8')
        qp.add_boolean_prefix('lernrestyp', 'X9')
        qp.set_database(database)
        extra = ''
        if domain != '':
          extra += ' site:' + domain
        if lernrestyp != '':
          extra += ' AND (' + self.get_extra_query(lernrestyp, 'lernrestyp') + ')'
        if fach != '':
          extra += ' AND (' + self.get_extra_query(fach, 'fach') + ')'
        if zielgruppe != '':
          extra += ' AND (' + self.get_extra_query(zielgruppe, 'zielgruppe') + ')'
        if schulart != '':
          extra += ' AND (' + self.get_extra_query(schulart, 'schulart') + ')'
        if schulstufe != '':
          extra += ' AND (' + self.get_extra_query(schulstufe, 'schulstufe') + ')'
        if sprache != '':
          extra += ' AND (' + self.get_extra_query(sprache, 'sprache') + ')'
        if schlagwort != '':
          extra += ' AND ' + schlagwort
        print q
        print q + '(' + extra +')'
        query = qp.parse_query(q + '(' + extra +')', DEFAULT_SEARCH_FLAGS)
        print query
        enquire.set_query(query)
        try:
          mset = enquire.get_mset(offset, count)
        except IOError, e:
          if "DatabaseModifiedError" in str(e):
            self.reopen_db()
          raise

        results = []
        for m in mset:
          results.append(
            {'percent': m[xapian.MSET_PERCENT],
             'url'    : m[xapian.MSET_DOCUMENT].get_value(URL),
             'title'  : m[xapian.MSET_DOCUMENT].get_value(TITLE),
             'date'   : m[xapian.MSET_DOCUMENT].get_value(DATE)})
        return {"count": mset.get_matches_lower_bound(),
                "results": results}

PORT = 3000
DB = '/data/xapian_db/'

reactor.listenTCP(PORT, server.Site(SearchServer(DB)))
reactor.run()
