#-*-coding: utf-8 -*-
"""
/dms/edufolder/models.py

.. beschreibt die Datenbankstrukturen der Online-Lernarchive
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  09.07.2007  Beginn der Arbeit
0.02  20.08.2007  Fach-Sachgebiet, Zertifikat, EduItem ergaenzt
0.03  28.08.2007  DmsEduOrg
0.04  03.09.2007  DmsEduSchlagwortStem
"""

from django.utils.encoding  import smart_unicode
from django.db              import models

from django.utils.translation import ugettext as _

from dms.models             import DmsItem

from dms.encode_decode      import encode_html

# -----------------------------------------------------
# Klassen
# -----------------------------------------------------

class DmsEduLernResTyp(models.Model):
  """ Verfuegbare Lernressourcen """
  name               = models.CharField(max_length=60)
  order              = models.IntegerField()

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_lernrestyp'

  class Admin:
    list_display = ( 'id', 'name', 'order' )
    pass

class DmsEduMedienformat(models.Model):
  """ Verfuegbare Medienformate """
  name               = models.CharField(max_length=60)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_medienformat'

  class Admin:
    list_display = ( 'id', 'name')
    pass

class DmsEduFachSachgebiet(models.Model):
  """ Verfuegbare Schulstufen """
  name               = models.CharField(max_length=60)
  order_by           = models.IntegerField(db_index=True)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_fach_sachgebiet'

  class Admin:
    list_display = ( 'id', 'name', 'order_by' )
    pass

class DmsEduObjekt(models.Model):
  """ moegliche Edu-Ressourcen """
  name               = models.CharField(max_length=60)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_objekt'

  class Admin:
    list_display = ( 'id', 'name' )
    pass

class DmsEduSchlagwort(models.Model):
  """ moegliche Schlagworte """
  name               = models.CharField(max_length=60, unique=True)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_schlagwort'

  class Admin:
    list_display = ( 'id', 'name' )
    pass

class DmsEduSchulart(models.Model):
  """ Verfuegbare Schulstufen """
  name               = models.CharField(max_length=60)
  order              = models.IntegerField()

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_schulart'

  class Admin:
    list_display = ( 'id', 'name', 'order' )
    pass

class DmsEduSchulstufe(models.Model):
  """ Verfuegbare Schulstufen """
  name               = models.CharField(max_length=60)
  order              = models.IntegerField()

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_schulstufe'

  class Admin:
    list_display = ( 'id', 'name', 'order' )
    pass

class DmsEduSprache(models.Model):
  """ Verfuegbare Schulstufen """
  key                = models.CharField(max_length=10)
  name               = models.CharField(max_length=60)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_sprache'

  class Admin:
    list_display = ( 'id', 'name', 'key' )
    pass

class DmsEduZertifikat(models.Model):
  """ Verfuegbare Zertifikate """
  name               = models.CharField(max_length=60)
  policy_url         = models.URLField()
  logo_url           = models.URLField()

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_zertifikat'

  class Admin:
    list_display = ( 'id', 'name' )
    pass

class DmsEduZielgruppe(models.Model):
  """ Verfuegbare Zielgruppe """
  name               = models.CharField(max_length=60)
  order              = models.IntegerField()

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_zielgruppe'

  class Admin:
    list_display = ( 'id', 'name', 'order' )
    pass

# -----------------------------------------------------
# Beschreibung einer Lernressource
# -----------------------------------------------------

class DmsEduItem(models.Model):
  """ Beschreibung der Lernressource """
  item                = models.ForeignKey(DmsItem)

  fach_sachgebiet     = models.ManyToManyField(DmsEduFachSachgebiet)
  #lern_res_typ         integer_3 in dms_item
  #medienformat         integer_4 in dms_item
  schlagwort          = models.ManyToManyField(DmsEduSchlagwort)
  schulart            = models.ManyToManyField(DmsEduSchulart)
  schulstufe          = models.ManyToManyField(DmsEduSchulstufe)
  sprache             = models.ManyToManyField(DmsEduSprache)
  #zertifikat         integer_5 in dms_item
  zielgruppe          = models.ManyToManyField(DmsEduZielgruppe)

  #quelle               string_1 in dms_item
  #lokal_id             string_2 in dms_item
  metadaten_url       = models.URLField()
  autor               = models.CharField(max_length=120)
  herausgeber         = models.CharField(max_length=250)
  anbieter_herkunft   = models.CharField(max_length=250)
  isbn                = models.CharField(max_length=20)
  preis               = models.CharField(max_length=20)
  titel_lang          = models.TextField()
  beschreibung_lang   = models.TextField()
  publikations_datum  = models.CharField(max_length=30)
  standards_kmk       = models.TextField()
  standards_weitere   = models.TextField()
  techn_voraus        = models.TextField()
  lernziel            = models.TextField()
  lernzeit            = models.CharField(max_length=20)
  methodik            = models.TextField()
  lehrplan            = models.TextField()
  rechte              = models.TextField()
  alter_min           = models.IntegerField(default=-1)
  alter_max           = models.IntegerField(default=-1)

  def __unicode__(self):
    return smart_unicode(self.item)

  class Meta:
    db_table = 'dms_dms_edu_item'

  class Admin:
    list_display = ( 'id', 'item' )
    pass

  def get_last_modified(self):
    """ """
    return self.last_modified.strftime(_(u'%d.%m.%Y %H:%M'))

  def get_absolute_url(self):
    n_pos = len(self.container.site.base_folder)
    if self.item.app.is_folderish:
      return self.container.site.url + self.container.path[n_pos:] + 'index.html'
    else:
      return self.container.site.url + self.container.path[n_pos:] + self.item.name

  def check_value(self, key, old, new, has_changed, do_check_paragraph=False):
    """ """
    if old.has_key(key) and new.has_key(key) and old[key] != new[key]:
      if do_check_paragraph:
        self.__dict__[key] = check_paragraph(new[key])
      else:
        self.__dict__[key] = new[key]
      return True
    else:
      return has_changed

  def save_values(self, item_container, new, do_init=False):
    """ speichert die Werte von DmsEduItem """
    self.item               = item_container.item
    self.metadaten_url      = item_container.get_absolute_url()
    """
    self.autor              = encode_html(new['autor'])
    self.herausgeber        = encode_html(new['herausgeber'])
    self.anbieter_herkunft  = encode_html(new['anbieter_herkunft'])
    self.isbn               = encode_html(new['isbn'])
    self.preis              = encode_html(new['preis'])
    self.titel_lang         = encode_html(new['titel_lang'])
    """
    self.autor              = encode_html(new['autor'])
    self.herausgeber        = encode_html(new['herausgeber'])
    self.anbieter_herkunft  = encode_html(new['anbieter_herkunft'])
    self.isbn               = encode_html(new['isbn'])
    self.preis              = encode_html(new['preis'])
    self.titel_lang         = encode_html(new['titel_lang'])
    self.beschreibung_lang  = new['beschreibung_lang']
    self.publikations_datum = new['publikations_datum']
    self.standards_kmk      = new['standards_kmk']
    self.standards_weitere  = new['standards_weitere']
    self.techn_voraus       = new['techn_voraus']
    self.lernziel           = new['lernziel']
    self.lernzeit           = new['lernzeit']
    self.methodik           = new['methodik']
    self.lehrplan           = new['lehrplan']
    self.rechte             = new['rechte']
    self.alter_min          = new['alter_min']
    self.alter_max          = new['alter_max']
    self.save()
    if do_init:
      self.fach_sachgebiet = []
      self.schulart        = []
      self.schulstufe      = []
      self.sprache         = []
      self.zielgruppe      = []
      self.schlagwort      = []
    self.save()
    return self

  def save_modified_values(self, old, new):
    """ speichert die geaenderten Werte von DmsEduItem """
    new['autor']              = encode_html(new['autor'])
    new['herausgeber']        = encode_html(new['herausgeber'])
    new['anbieter_herkunft']  = encode_html(new['anbieter_herkunft'])
    new['isbn']               = encode_html(new['isbn'])
    new['preis']              = encode_html(new['preis'])
    new['titel_lang']         = encode_html(new['titel_lang'])
    new['publikations_datum'] = encode_html(new['publikations_datum'])
    has_changed = False
    has_changed = self.check_value('metadaten_url', old, new, has_changed)
    has_changed = self.check_value('autor', old, new, has_changed)
    has_changed = self.check_value('herausgeber', old, new, has_changed)
    has_changed = self.check_value('anbieter_herkunft', old, new, has_changed)
    has_changed = self.check_value('isbn', old, new, has_changed)
    has_changed = self.check_value('preis', old, new, has_changed)
    has_changed = self.check_value('titel_lang', old, new, has_changed)
    has_changed = self.check_value('beschreibung_lang', old, new, has_changed)
    has_changed = self.check_value('publikations_datum', old, new, has_changed)
    has_changed = self.check_value('standards_kmk', old, new, has_changed)
    has_changed = self.check_value('standards_weitere', old, new, has_changed)
    has_changed = self.check_value('techn_voraus', old, new, has_changed)
    has_changed = self.check_value('lernziel', old, new, has_changed)
    has_changed = self.check_value('lernzeit', old, new, has_changed)
    has_changed = self.check_value('methodik', old, new, has_changed)
    has_changed = self.check_value('lehrplan', old, new, has_changed)
    has_changed = self.check_value('rechte', old, new, has_changed)
    has_changed = self.check_value('alter_min', old, new, has_changed)
    has_changed = self.check_value('alter_max', old, new, has_changed)
    if has_changed:
      self.save()

# -----------------------------------------------------
# Beschreibung einer Lernressource
# -----------------------------------------------------

class DmsEduOrg(models.Model):
  """ Beschreibung der Landesserver """
  schluessel          = models.CharField(max_length=20, db_index=True)
  beschreibung        = models.CharField(max_length=120)
  url                 = models.URLField()
  
  def __unicode__(self):
    return smart_unicode(self.schluessel)

  class Meta:
    db_table = 'dms_dms_edu_org'

  class Admin:
    list_display = ('id', 'schluessel')
    pass

class DmsEduSchlagwortStem(models.Model):
  """
  Schlagworte sollten moeglichst universell verwandt werden koennen.
  Begriffe, die im Plural eingegben werden sollten ebenso gefunden
  werden wie die gleichen Begriffe im Singular. Dies erreicht man
  durch "stemming". Leider sind diese Verfahren nicht fehlerfrei.
  So führen z.B. Hesse und Hessen oder Ostern und Osten zu dem
  jeweils gleichen Stem-Wort. Ueber diese Tabelle koennen diese
  Fehler (nachtraeglich) korrigiert werden, indem diese Tabelle
  beim Einfuegen neuer Suchbegriffe abgefragt wird.
  """
  name               = models.CharField(max_length=60, unique=True)
  stem               = models.CharField(max_length=60, db_index=True)

  def __unicode__(self):
    return smart_unicode(self.name)

  class Meta:
    db_table = 'dms_edu_schlagwort_stem'

  class Admin:
    list_display = ('id', 'name', 'stem')
    pass

