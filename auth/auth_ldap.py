# -*- coding: utf-8 -*-
"""
/dms/auth/auth_ldap.py

.. verwaltet User in LDAP (fuer Download von Dateien)
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  19.12.2007  Beginn der Dokumentation
"""

import ldap
import re
import types

GROUP = 'groups'
COMMUNITY = 'community'

class ldap_user_class:
  """
  Diese Klasse bildet die Schnittstelle zur Verwaltung der
  kennwort-geschtzten Zugaenge via LDAP
  """

  def __init__(self, ldap_host, ldap_port, ldap_dn, ldap_user, ldap_passwd):
    """ Verbindungsdaten speichern """
    self.host    = ldap_host
    self.port    = ldap_port
    self.base_dn = ldap_dn
    self.user    = ldap_user
    self.passwd  = ldap_passwd

  def _open_ldap(self):
    """ Verbindung oeffnen """
    self.conn = ldap.open(self.host, int(self.port))
    if self.conn != None:
      self.conn.simple_bind_s("cn=" + self.user + "," + self.base_dn, self.passwd)
      return True
    else:
      return False

  def _close_ldap(self):
    """ Verbindung schliessen """
    self.conn.unbind_s()

  def _get_ou_dn(self, ou):
    """ """
    if ou == None:
      return self.base_dn
    else:
      return "ou=" + ou + "," + self.base_dn

  def _get_dn(self, uid, ou, bWithBase=True):
    if ou == None:
      dn = "uid=" + uid
    else:
      dn = "uid=" + uid + ",ou=" + ou
    if bWithBase:
      return dn + "," + self.base_dn
    else :
      return dn

  def _add_user(self, cn, uid, ou, pwd, descr, org_id, is_encrypted):
    """ Einen einzelnen User ergaenzen """
    if is_encrypted:
      cPassword = pwd
    else:
      cPassword = AuthEncoding.pw_encrypt(pwd,'SSHA')
    # einige UIDs kennzeichnen besondere Gruppen
    # Schueler?
    pat = 'sch_\d\d\d\d_.*.\.*'
    if re.match(pat, uid):
      gid = 10000
    else:
      # Schule?
      pat = 's_\d\d\d\d'
      if re.match(pat, uid):
        gid = 50000
      else:
        # Lehrer an einer Schule
        pat = '\d\d\d\d_'
        if re.match(pat, uid):
          gid = 20000
        else:
          # "freies" MItglied
          gid = 30000
    try:
      self.conn.add_s(self._get_dn(uid,ou),
         [
            #("objectclass",["account","simpleSecurityObject"]),
            ("objectclass",["posixAccount","Account"]),
            ("cn", [ str(cn), ]),
            ("uid", [ str(uid), ]),
            ("uidNumber", [str(org_id), ]),
            ("gidNumber", [ str(gid), ]),
            ("homeDirectory", ["/tmp", ]),
            ("userPassword", [ str(cPassword), ]),
            ("description", [ str(descr), ]),
         ]
       )
      return True
    except:
      return False

  def get_user_items(self, lItem):
    """ Die wichtigsten Items extrahieren """
    ret = []
    for rec_dn, rec_dict in lItem :
      ret.append( (rec_dict['uid'][0], rec_dict['userPassword'][0]) )
    return ret

  def get_user_names(self, lItem):
    """ Alle in lItems enthaltenen uids werden zurueckgegeben """
    ret = []
    for rec_dn, rec_dict in lItem :
      ret.append ( rec_dict['uid'][0] )
    return ret

  def _get_group_dn(self, group):
    dn = 'cn=%s,ou=%s' % (group, group)
    return dn + self.base_dn

  def _add_group(self, cn, ou, ou_community, uids):
    """ Eine Gruppe ergaenzen """
    if type(cn) == types.UnicodeType:
      cn = cn.encode('iso-8859-1')
    try:
      this_dn = 'cn=%s,%s' % (cn, self._get_ou_dn(ou))
      params = [
                ('objectclass',["device", "posixGroup", 'top']),
                ('cn', [cn]),
                ('gidNumber', ['1']),
              ]
      if uids != []:
        params.append(('memberUid', uids))
      self.conn.add_s(this_dn, params)
    except:
      pass

  def _modify_group(self, cn, ou, ops):
    """ Mitglieder einer Gruppe ergaenzen, loeschen """
    #try:
    this_dn = 'cn=%s,%s' % (cn, self._get_ou_dn(ou))
    self.conn.modify_s(this_dn, ops)
    #except:
    #  pass

  # ---------------------------------------------
  #
  # Hauptfunktionen
  #
  # ---------------------------------------------

  def get_user_list(self, uid_pat, ou):
    """ Die User zurueckliefern, die zu uid_pat passen """
    if not self._open_ldap():
      return []
    if ou == None:
      dn = self.base_dn
    else:
      dn = "ou=" + ou + "," + self.base_dn
    try:
      res = self.conn.search_s(dn, ldap.SCOPE_SUBTREE, "uid="+uid_pat, None)
    except :
      return []
    # --- Items extrahieren
    ret = self.get_user_names(res)
    self._close_ldap()
    return ret

  def get_single_user(self, uid, ou):
    """ Den User zurueckliefern, der zu uid und ou passt """
    if not self._open_ldap():
      return None
    try :
      res = self.conn.search_s(self._get_ou_dn(ou), ldap.SCOPE_SUBTREE, self._get_dn(uid,None,0), None)
    except:
      return []
    # --- Items extrahieren
    ret = self.get_user_items(res)
    self._close_ldap()
    if len(ret) > 0:
      return ret[0]
    else:
      return None

  def get_single_user_complete(self, uid, ou):
    """ Die kompletten Infos des Users zurueckliefern, der zu uid und ou passt """
    if not self._open_ldap():
      return None
    try:
      res = self.conn.search_s(self._get_ou_dn(ou), ldap.SCOPE_SUBTREE, self._get_dn(uid,None,0), None)
    except:
      return []
    self._close_ldap()
    return res[0]

  def add_user(self, cn, uid, ou, pwd, descr, org_id, is_encrypted):
    """ Einen einzelnen User ergaenzen """
    if self._open_ldap():
      res = self._add_user(cn, uid, ou, pwd, descr, org_id, is_encrypted)
      self._close_ldap()
      return res
    return False

  def add_group(self, cn):
    """ Eine User-Gruppe ergaenzen """
    if self._open_ldap():
      self._add_group(cn, GROUP, COMMUNITY, [])
      self._close_ldap()

  def del_group(self, cn):
    """ Eine User-Gruppe loeschen """
    if type(cn) == types.UnicodeType:
      cn = cn.encode('iso-8859-1')
    this_dn = 'cn=%s,%s' % (cn, self._get_ou_dn(GROUP))
    if self._open_ldap():
      try:
        self.conn.delete_s(this_dn)
      except:
        pass
      self._close_ldap()

  def del_user(self, uid, ou):
    """ Einen einzelnen User loeschen """
    if self._open_ldap():
      try:
        self.conn.delete_s(self._get_dn(uid,ou))
      except:
        pass
      self._close_ldap()

  def edit_user(self, cn, uid, gid, ou, pwd, descr, org_id):
    """ Einen einzelnen User aendern (durch Loeschen und neues Anlegen) """
    if self._open_ldap():
      try:
        self.conn.delete_s(self._get_dn(uid,ou))
      except:
        pass
      res = self._add_user(cn, uid, gid, ou, pwd, descr, org_id)
      self._close_ldap()
      return res
    return False

  def modify_group(self, cn, ou, ops):
    """ Eine User-Gruppe ergaenzen """
    if self._open_ldap():
      self._modify_group(cn, ou, ops)
      self._close_ldap()

  def modify_user_group(self, username, group, op):
    """ User in Gruppe ergaenzen bzw. loeschen """
    if type(username) == types.UnicodeType:
      username = username.encode('iso-8859-1')
    if type(group) == types.UnicodeType:
      group = group.encode('iso-8859-1')
    if self._open_ldap():
      mod_list = ((op, 'memberUid', username),)
      try:
        self._modify_group(group, GROUP, mod_list)
      except:
        pass
      self._close_ldap()

  def add_user_to_group(self, username, group):
    """ fuegt <username> der Gruppe <group> hinzu """
    self.modify_user_group(username, group, ldap.MOD_ADD)

  def del_user_from_group(self, username, group):
    """ loescht <username> aus der Gruppe <group> """
    self.modify_user_group(username, group, ldap.MOD_DELETE)

  def is_password_ok(self, uid, ou, pwd):
    """ Ueberpruefung des Kennwortes """
    if not self._open_ldap():
      return 0
    try:
      self.conn.bind_s(self._get_dn(uid,ou), pwd, ldap.AUTH_SIMPLE)
    except:
      self._close_ldap()
      return False
    self._close_ldap()
    return True
