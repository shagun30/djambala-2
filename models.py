#-*-coding: utf-8 -*-
"""
models.py

.. beschreibt die Datenbankstrukturen des dms-Systems:
            Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  13.01.2007  Beginn der Dokumentation
0.02  19.01.2007  Tabellen zur User-Verwaltung
0.03  20.01.2007  is_top_folder
0.04  23.01.2007  is_userfolder
0.05  02.02.2007  save_navigation
0.06  03.02.2007  impress_url
0.07  15.02.2007  info_slot_right wird ausgewertet
0.08  05.03.2007  has_comments
0.09  12.03.2007  has_comments
0.10  21.03.2007  download_protecte
0.11  23.03.2007  DmsFeed
0.12  27.03.2007  self.__dict__[key] = ..
0.13  19.09.2007  is_changeable
0.14  24.09.2007  is_exchangeable - fuer Elixier-Austausch
0.15  15.02.2008  right_logo
0.16  19.03.2008  signal_post_save, save_modified_values mit new_user, DmsAudit
0.17  14.05.2006  integer_6
"""

import  datetime
import  string
import  re
import  types

from django.db              import models
from django.dispatch        import dispatcher
from django.utils.encoding  import smart_unicode

from django.utils.translation import ugettext as _

from dms.auth.models        import User
from dms.signals            import signal_pre_delete
from dms.signals            import signal_post_save

from encode_decode          import decode_html
from dms.utils_base         import convert_str_to_date
from dms.utils_base         import expand_link_icons

# -----------------------------------------------------
# Hilfsfunktionen
# -----------------------------------------------------

def do_check_paragraph(text):
  """ """
  if text == '' or string.find(text, '<p>') >= 0:
    return text
  return '<p>' + text +'</p>'

def boolean_has_changed(key, old, new):
  if (old.has_key(key) and not new.has_key(key) ) \
    or (not old.has_key(key) and new.has_key(key) ) \
    or (old.has_key(key) and new.has_key(key) and bool(old[key]) != bool(new[key]) ):
    return True
  else :
    return False

def get_boolean(key, new):
  return bool( new.has_key(key) and new[key] )

def get_last_modified():
  """ liefert formatierten aktuellen Zeitpunkt """
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def check_boolean(self, key, old, new, has_changed):
  """ """
  if old.has_key(key) and boolean_has_changed(key, old, new):
    self.__dict__[key] = get_boolean(key, new)
    return True
  else:
    return has_changed

# -----------------------------------------------------
# Klassen zur User-Verwaltung: 1.Teil
# -----------------------------------------------------

class DmsLicense(models.Model):
  """ verschiedene Lizenzen """
  name                = models.CharField(max_length=80)
  url                 = models.URLField()
  image_url           = models.URLField()

  def __unicode__(self):
    return self.name

  class Admin:
    list_filter = ('name',)
    list_display = ( 'id', 'name' )
    pass

# -----------------------------------------------------
# Klasse der Module/Programme
# -----------------------------------------------------

class DmsApp(models.Model):
  """ Beschreibung der Web-Applikationen ... """
  name                = models.CharField(max_length=40, unique=True)
  description         = models.CharField(max_length=60)
  is_folderish        = models.BooleanField()
  is_userfolder       = models.BooleanField()
  is_linkable         = models.BooleanField()
  is_available        = models.BooleanField(default=1)
  has_own_breadcrumb  = models.BooleanField(default=0)
  sub_app_id          = models.IntegerField(default=0)

  def __unicode__(self):
      return self.name

  class Admin:
    #list_filter = ('is_folderish', 'is_userfolder', 'is_usermanagement', 'sub_app_id')
    list_filter = ('is_folderish', 'is_userfolder', 'sub_app_id')
    list_display = ( 'id', 'name', 'is_folderish' )
    pass

class DmsAppAllowed(models.Model):
  """ Web-Applikationen, die in parent_app eingefuegt werden duerfen ... """
  parent_app          = models.ForeignKey(DmsApp)
  child_app           = models.IntegerField()

  def __unicode__(self):
      return smart_unicode(self.parent_app)

  class Admin:
    list_display = ( 'id', 'parent_app', 'child_app' )
    pass

class DmsNavMenuLeft(models.Model):
  """ Navigationsmenu am linken Rand """
  menu_id             = models.IntegerField(db_index=True, default=-1)
  is_main_menu        = models.BooleanField(default=0)
  name                = models.CharField(max_length=60, db_index=True)
  description         = models.CharField(max_length=80)
  navigation          = models.TextField()

  def __unicode__(self):
      return self.name

  class Admin:
    list_filter = ('menu_id',)
    list_display = ( 'id', 'menu_id', 'name' )
    pass

  def save_menu(self, new, is_main_menu=False):
    """ Menue speichern """
    key = 'name'
    self.name = new[key]
    key = 'description'
    if new.has_key(key):
      self.description = new[key]
    key = 'navigation'
    self.navigation = new[key]
    key = 'is_main_menu'
    if new.has_key(key):
      self.is_main_menu = new[key]
    else:
      self.is_main_menu = is_main_menu
    self.save ()

class DmsNavMenuTop(models.Model):
  """ Navigationsmenu am oberen Rand
      menu_id = -1: Ausgangsdefinition des Menus
  """
  menu_id             = models.IntegerField(db_index=True, default=-1)
  name                = models.CharField(max_length=60, db_index=True)
  navigation          = models.TextField()

  def __unicode__(self):
      return self.name

  class Admin:
    list_filter = ('menu_id',)
    list_display = ( 'id', 'menu_id', 'name' )
    pass

  def save_menu(self, old, new):
    """ falls erforderlich werden die neuen Werte gespeichert """
    has_changed = False
    key = 'name'
    if old.has_key(key) and old[key] != new[key] :
      self.name = new[key]
      self.save()
    key = 'description'
    if old.has_key(key) and old[key] != new[key] :
      self.description = new[key]
      has_changed = True
    key = 'navigation'
    if old.has_key(key) and old[key] != new[key] :
      self.navigation = new[key]
      has_changed = True
    if has_changed:
      self.save ()

class DmsSite(models.Model):
  """ hier werden die Pfade gespeichert """
  url                = models.URLField (unique=True)
  base_folder        = models.URLField (unique=True)
  name               = models.CharField ( max_length=60 )
  title              = models.CharField ( max_length=200 )
  sub_title          = models.CharField ( max_length=200 )
  title_class        = models.CharField ( max_length=40 )
  logo               = models.CharField ( max_length=120 )
  logo_url           = models.URLField ()
  logo_width         = models.IntegerField()
  logo_height        = models.IntegerField()
  right_logo         = models.CharField ( max_length=120 )
  right_logo_url     = models.URLField ()
  right_logo_width   = models.IntegerField()
  right_logo_height  = models.IntegerField()
  skin_style         = models.CharField(max_length=30)
  left_image_url     = models.URLField ()
  left_image_width   = models.IntegerField()
  left_image_height  = models.IntegerField()
  navigation_bottom_image = models.CharField(max_length=240)
  impress_url        = models.URLField ()
  master_links       = models.TextField()
  help_url           = models.URLField ()
  search_form        = models.TextField()
  org_id             = models.IntegerField(default=0, db_index=True)

  def __unicode__(self):
      return self.name

  class Admin:
    list_display = ( 'id', 'url', 'name', 'base_folder' )
    pass

class DmsContainer(models.Model):
  """ hier werden die Pfade gespeichert """
  # --- id des Item-Objektes, das diesen Container bildet
  this_item_id        = models.IntegerField(db_index=True)
  site                = models.ForeignKey(DmsSite)
  path                = models.CharField(max_length=240,unique=True)
  is_top_folder       = models.BooleanField(default=False)
  min_role_id         = models.IntegerField(default=2000)
  nav_title           = models.CharField(max_length=60)
  menu_top_id         = models.IntegerField(default=1)
  menu_left_id        = models.IntegerField(default=1)
  nav_name_top        = models.CharField(max_length=60)
  nav_name_left       = models.CharField(max_length=60)
  sections            = models.TextField()
  show_next           = models.BooleanField(default=0)

  def __unicode__(self):
      return self.path

  class Admin:
    list_filter = ('site', 'min_role_id', 'is_top_folder')
    list_display = ( 'id', 'this_item_id', 'path', 'site' )
    pass

  def save_values(self, old, new):
    """ falls erforderlich werden die neuen Werte gespeichert """
    has_changed = False
    has_changed = check_boolean(self, 'is_top_folder', old, new, has_changed)
    key = 'min_role_id'
    if old.has_key(key) and old[key] != new[key] :
      self.min_role_id = int(new[key])
      has_changed = True
    key = 'nav_title'
    if old.has_key(key) and old[key] != new[key] :
      self.nav_title = decode_html(new[key])
      has_changed = True
    key = 'menu_id'
    if old.has_key(key) and old[key] != new[key] :
      self.menu_left_id = decode_html(new[key])
      has_changed = True
    key = 'sections'
    if old.has_key(key) and old[key] != new[key] :
      self.sections = decode_html(new['sections'])
      has_changed = True
    has_changed = check_boolean(self, 'show_next', old, new, has_changed)
    if has_changed:
      self.save()
      return True
    else:
      return False

  def is_protected(self):
    """ wird dieses Ordner-Objekt geschuetzt? """
    return (self.min_role_id < 2000)

class DmsItem ( models.Model ) :
  """ Basisbeschreibung eines Objektes """
  app                 = models.ForeignKey(DmsApp, db_index=True)
  owner               = models.ForeignKey(User)
  license             = models.ForeignKey(DmsLicense)
  name                = models.CharField(max_length=200,db_index=True)
  title               = models.CharField(max_length=240)
  sub_title           = models.CharField(max_length=240)
  text                = models.TextField(null=True)
  text_more           = models.TextField(null=True)
  url_more            = models.URLField(null=True, db_index=True)
  url_more_extern     = models.BooleanField(default=0)
  image_url           = models.URLField(null=True)
  image_url_url       = models.URLField(null=True)
  image_extern        = models.BooleanField(default=0)
  is_wide             = models.BooleanField(default=1)
  is_important        = models.BooleanField(default=0)
  info_slot_right     = models.TextField(null=True)
  has_user_support    = models.BooleanField(default=False)
  has_comments        = models.BooleanField(default=False)
  is_moderated        = models.BooleanField(default=False)
  is_exchangeable     = models.BooleanField(default=True)
  string_1            = models.URLField(null=True, db_index=True)
  string_2            = models.URLField(null=True, db_index=True)
  integer_1           = models.IntegerField(db_index=True)
  integer_2           = models.IntegerField(db_index=True)
  integer_3           = models.IntegerField(db_index=True)
  integer_4           = models.IntegerField(db_index=True)
  integer_5           = models.IntegerField(db_index=True)
  integer_6           = models.IntegerField()
  extra               = models.TextField(null=True)

  def __unicode__(self):
      return self.name

  class Admin:
    list_filter = ('app', )
    list_display = ( 'id', 'name', 'app', 'title', 'owner' )
    pass

  def check_int(self, key, old, new, has_changed):
    """ """
    if old.has_key(key) and new.has_key(key) and old[key] != new[key]:
      self.__dict__[key] = int(new[key])
      return True
    else:
      return has_changed

  def check_value(self, key, old, new, has_changed,
                        check_paragraph=False, check_html=False):
    """ """
    # --- Normalisierung
    if old.has_key(key) and not new.has_key(key):
      new[key] = old[key]
    if not old.has_key(key) and new.has_key(key):
      old[key] = new[key]
    if old.has_key(key) and old[key] != new[key]:
      if check_paragraph:
        if check_html:
          self.__dict__[key] = do_check_paragraph(decode_html(new[key]))
        else:
          self.__dict__[key] = do_check_paragraph(new[key])
      else:
        if check_html:
          self.__dict__[key] = decode_html(new[key])
        else:
          self.__dict__[key] = new[key]
      return True
    else:
      return has_changed

  def check_text(self, key, old, new, has_changed,
                       check_paragraph=False, check_html=False):
    """ """
    if old.has_key(key):
      o = expand_link_icons(old[key])
      n = expand_link_icons(new[key])
      if o != n:
        if check_paragraph:
          self.__dict__[key] = do_check_paragraph(decode_html(n))
        else:
          self.__dict__[key] = decode_html(n)
        return True
      else:
        return has_changed
    else:
      return has_changed

  def check_new_text(self, key, text, check_html=True):
    """ """
    n = expand_link_icons(text)
    if check_html:
      self.__dict__[key] = do_check_paragraph(n)
    else:
      self.__dict__[key] = n

  def check_boolean(self, key, old, new, has_changed):
    """ """
    if old.has_key(key) and boolean_has_changed(key, old, new):
      self.__dict__[key] = get_boolean(key, new)
      return True
    else:
      return has_changed

  def get_new_item(self, name, new, container, app, owner, license=None):
    """ initialiSiert einen neuen Datensatz """

    def get_select (key, new):
      """ falls <key> nicht in <new> existiert, wird '' zurueckgegeben """
      if new.has_key(key):
        return new[key]
      else:
        return ''

    def get_value(key, new, default, check_paragraph=False):
      """ """
      if new.has_key(key):
        if check_paragraph:
          self.__dict__[key] = do_check_paragraph(new[key])
        else:
          self.__dict__[key] = new[key]
      else:
        self.__dict__[key] = default

    def get_boolean_value(key, new, default):
      """ """
      if new.has_key(key):
        self.__dict__[key] = bool( new.has_key(key) and new[key])
      else:
        self.__dict__[key] = default

    self.app = app
    if license == None:
      license = DmsLicense.objects.get(id=1)
    self.license = license
    self.owner = owner
    self.name = name
    get_value('title', new, '')
    get_value('sub_title', new, '')
    get_value('text', new, '', app.name != 'dmsText')
    self.check_new_text('text', self.text, app.name != 'dmsText')
    if app.name in ['dmsText', 'dmsEmailForm']:
      get_value('text_more', new, '', False)
    else:
      get_value('text_more', new, '', app.name != 'dmsText')
      self.check_new_text('text_more', self.text_more)
    get_value('url_more', new, '')
    get_boolean_value('url_more_extern', new, False)
    get_value('image_url', new, '')
    get_value('image_url_url', new, '')
    get_boolean_value('image_extern', new, False)
    get_boolean_value('is_wide', new, True)
    get_boolean_value('is_important', new, False)
    get_value('info_slot_right', new, '')
    get_boolean_value('has_user_support', new, False)
    get_boolean_value('has_comments', new, False)
    get_boolean_value('is_moderated', new, True)
    get_boolean_value('is_exchangeable', new, True)
    get_value('string_1', new, '')
    get_value('string_2', new, '')
    get_value('integer_1', new, -1)
    get_value('integer_2', new, -1)
    get_value('integer_3', new, -1)
    get_value('integer_4', new, -1)
    get_value('integer_5', new, -1)
    get_value('integer_6', new, -1)
    if new.has_key('extra'):
      self.extra = new['extra']
    else:
      self.extra = ''
    return self

  def copy(self):
    """ erzeugt eine Kopie von paste_item """
    new_item = DmsItem()
    new_item = self
    new_item.id = None
    new_item.save()
    return new_item

  def save_values(self, old, new, profi_mode=False):
    """ falls erforderlich werden die neuen Werte gespeichert """
    from datetime import date

    def header_to_info_slot(text):
      """ wandelt HTML aus dem WYSIWYG-Editor in Infoslot-Format um """
      from django.template.loader import get_template
      from django.template import Context
      t = get_template('utils/info_slot_right.html')
      ret = ''
      HEADER_START = r'<[hH][1-6]>'
      HEADER_END   = r'</[hH][1-6]>'
      s = text
      s_obj = re.search(HEADER_START, s, re.M)
      while s_obj:
        e_obj = re.search(HEADER_END, s, 0)
        if s_obj and e_obj:
          header = string.strip(s[s_obj.end():e_obj.start()])
          if header == '<br />' or header == '&nbsp;':
            header = ''
          s = string.strip(s[e_obj.end():])
          s_obj = re.search(HEADER_START, s, re.M)
          if s_obj == None :
            info = s
          else :
            info = s[:s_obj.start()]
          s = s[len(info):]
          info = string.strip(info)
          if header != '':
            c = Context ( { 'header': header.strip(), 'info': info.strip(), } )
          else:
            c = Context ( { 'info': info.strip(), } )
          ret += t.render(c)
          #assert False
          s_obj = re.search(HEADER_START, s, re.M)
      return ret

    def boolean_has_changed(key, old, new):
      if (old.has_key(key) and not new.has_key(key) ) \
        or (not old.has_key(key) and new.has_key(key) ) \
        or (old.has_key(key) \
        and new.has_key(key) and bool(old[key]) != bool(new[key]) ):
        return True
      else :
        return False

    def get_boolean(key, new):
      return bool( new.has_key(key) and new[key] )

    def select_has_changed ( key, old, new ) :
      if (old.has_key(key) and not new.has_key(key) ) \
        or (not old.has_key(key) and new.has_key(key) ) \
        or (old.has_key(key) and new.has_key(key) and old[key] != new[key] ):
        return True
      else :
        return False

    def get_select ( key, new ) :
      if new.has_key(key) :
        return new[key]
      else :
        return None

    has_changed = False
    if old.has_key('license') and new.has_key('license') \
    and old['license'] != int(new['license']):
      has_changed = True
      self.license = DmsLicense.objects.filter(id=int(new['license']))[0]
    has_changed = self.check_value('title', old, new, has_changed, check_html=not profi_mode)
    has_changed = self.check_value('sub_title', old, new, has_changed, check_html=True)
    has_changed = self.check_text('text', old, new, has_changed, self.app.name != 'dmsText')
    has_changed = self.check_text('text_more', old, new, has_changed, self.app.name != 'dmsText')
    has_changed = self.check_value('url_more', old, new, has_changed)
    has_changed = self.check_boolean('url_more_extern', old, new, has_changed)
    has_changed = self.check_value('image_url', old, new, has_changed)
    has_changed = self.check_value('image_url_url', old, new, has_changed)
    has_changed = self.check_boolean('image_extern', old, new, has_changed)
    has_changed = self.check_boolean('is_wide', old, new, has_changed)
    has_changed = self.check_boolean('is_important', old, new, has_changed)
    key = 'info_slot_right'
    if old.has_key(key) and old[key] != new[key] :
      self.info_slot_right = header_to_info_slot(new[key])
      has_changed = True
    has_changed = self.check_boolean('has_user_support', old, new, has_changed)
    has_changed = self.check_boolean('has_comments', old, new, has_changed)
    has_changed = self.check_boolean('is_moderated', old, new, has_changed)
    has_changed = self.check_boolean('is_changeable', old, new, has_changed)
    has_changed = self.check_boolean('show_next', old, new, has_changed)
    has_changed = self.check_value('string_1', old, new, has_changed)
    has_changed = self.check_value('string_2', old, new, has_changed)
    has_changed = self.check_int('integer_1', old, new, has_changed)
    has_changed = self.check_int('integer_2', old, new, has_changed)
    has_changed = self.check_int('integer_3', old, new, has_changed)
    has_changed = self.check_int('integer_4', old, new, has_changed)
    has_changed = self.check_int('integer_5', old, new, has_changed)
    has_changed = self.check_int('integer_6', old, new, has_changed)
    has_changed = self.check_value('extra', old, new, has_changed)

    if has_changed :
      self.save()
      return True
    else:
      return False

class DmsItemContainer ( models.Model ) :
  """ Verbindungstabelle Item-Container """
  container           = models.ForeignKey(DmsContainer)
  item                = models.ForeignKey(DmsItem)
  owner               = models.ForeignKey(User)
  is_deleted          = models.BooleanField(default=False)
  parent_item_id      = models.IntegerField(db_index=True)
  section             = models.CharField(max_length=60)
  order_by            = models.IntegerField(default=100)
  part_of_id          = models.IntegerField(default=-1) # Webquest, Arbeitsgruppen
  is_browseable       = models.BooleanField(default=True)
  is_data_object      = models.BooleanField(default=True)
  is_changeable       = models.BooleanField(default=True)
  visible_start       = models.DateTimeField (default=datetime.datetime.now())
  visible_end         = models.DateTimeField (default=datetime.datetime.now()+\
                                              datetime.timedelta(8*365.25))
  last_modified       = models.DateTimeField(db_index=True,
                                             default=datetime.datetime.now())

  def __unicode__(self):
    try:
      return smart_unicode(self.container) + ' :: ' + smart_unicode(self.item)
    except:
      return _('ohne container und/oder item')

  class Admin:
    list_filter = ('is_deleted', 'last_modified')
    list_display = ( 'id', 'container', 'item', 'owner', 'is_deleted',
                     'last_modified' )
    pass

  def get_last_modified(self):
    """ """
    return self.last_modified.strftime('%d.%m.%Y %H:%M')

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

  def check_boolean(self, key, old, new, has_changed):
    """ """
    if old.has_key(key) and boolean_has_changed(key, old, new):
      self.__dict__[key] = get_boolean(key, new)
      return True
    else:
      return has_changed

  def check_date(self, key, old, new, has_changed):
    """ """
    if old.has_key(key):
      if type(new[key]) == types.UnicodeType:
        new_date = convert_str_to_date(new[key])
      else:
        new_date = new[key]
      t = type(new[key])
      if old[key] != new_date:
        self.__dict__[key] = new_date
        return True
      else:
        return has_changed

  def move(self, item_container, container):
    """ verschiebt ein Objekt """
    if item_container.is_changeable:
      self.container      = container
      self.parent_item_id = item_container.item.id
      self.save()

  def copy(self, paste_item_container, container, item, parent_item_id):
    """ kopiert ein Objekt """
    new_item_container = DmsItemContainer()
    new_item_container = paste_item_container
    new_item_container.id = None
    new_item_container.container = container
    new_item_container.item = item
    new_item_container.parent_item_id = parent_item_id
    try:
      new_item_container.part_of_id = DmsItemContainer.objects.filter(item=item)[0]
    except:
      new_item_container.part_of_id = -1
    new_item_container.save()
    return new_item_container

  def save_values(self, my_container, item, owner, is_browseable, section,
                        folder_id=None,
                        visible_start=None, visible_end=None, 
                        is_data_object=True,
                        parent_item_container=None,
                        order_by=100):
    """ """
    item_containers = DmsItemContainer.objects.filter(item=item)
    self.container      = my_container
    self.item           = item
    self.owner          = owner
    self.order_by       = order_by
    if parent_item_container == None:
      self.part_of_id     = -1
    else:
      self.part_of_id     = parent_item_container.id
    self.is_deleted     = False
    self.is_browseable  = is_browseable
    self.is_changeable  = True
    if len(item_containers) > 0:
      self.visible_start  = item_containers[0].visible_start
      self.visible_end    = item_containers[0].visible_end
      self.is_data_object = is_data_object
    else:
      this_year = int(datetime.datetime.now().strftime ( '%Y' ))
      if visible_start == None:
        self.visible_start = datetime.date.today()
      else:
        self.visible_start = convert_str_to_date(visible_start)
      if visible_end == None:
        self.visible_end = datetime.date(int(this_year)+10,12,31)
      else:
        self.visible_end = convert_str_to_date(visible_end)
      self.is_data_object = is_data_object
    self.last_modified  = datetime.datetime.now()
    if folder_id != None:
      self.parent_item_id = folder_id
    else:
      self.parent_item_id = my_container.this_item_id
    self.section        = section
    self.save()
    return self

  def save_modified_values(self, old, new, changed = False, new_user=None):
    """ falls erforderlich werden die neuen Werte gespeichert """
    from datetime import date

    has_changed = False
    has_changed = self.check_value('section', old, new, has_changed)
    has_changed = self.check_boolean('order_by', old, new, has_changed)
    has_changed = self.check_boolean('part_of_id', old, new, has_changed)
    has_changed = self.check_boolean('is_browseable', old, new, has_changed)
    has_changed = self.check_date('visible_start', old, new, has_changed)
    has_changed = self.check_date('visible_end', old, new, has_changed)
    if changed or has_changed:
      self.last_modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
      if new_user != None:
        self.owner = new_user
      self.save()

  def get_parent(self):
    """ liefert zu einem Objekt das Eltern-Objekt """
    if self.parent_item_id >= 0:
      item_containers = DmsItemContainer.objects.select_related().\
                        filter(item=self.parent_item_id)
      if len(item_containers) > 0:
        return item_containers[0]
      else:
        return None
    else:
      return DmsItemContainer.objects.filter(item__id=1)[0]

  def set_is_changeable(self, changeable=True):
    """ setzt is_changeable-Flag """
    self.is_changeable = changeable
    self.save()
 
class DmsComment(models.Model):
  """ Kommentare """
  #parent_id           = models.IntegerField(db_index=True)
  parent_item         = models.ForeignKey(DmsItem)
  name                = models.CharField(max_length=80)
  email               = models.URLField(null=True)
  title               = models.CharField(max_length=80)
  text                = models.TextField(null=True)
  value               = models.IntegerField(default=0) # Bewertung
  is_browseable       = models.BooleanField(default=False)
  last_modified       = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
      return self.name + '/' + self.title

  class Admin:
    list_filter = ('is_browseable', 'last_modified')
    list_display = ( 'id', 'parent_item', 'name', 'title',
                     'is_browseable', 'last_modified' )
    pass

  def save_values(self, new):
    from datetime import date

    def get_boolean ( key, new ) :
      return bool( new.has_key(key) and new[key] )

    key = 'item_id'
    self.parent_item_id = int(new[key])
    key = 'username'
    self.name = new[key]
    key = 'email'
    if new.has_key(key):
      self.email = new[key]
    else:
      self.email = ''
    key = 'title'
    self.title = new[key]
    key = 'text'
    self.text = new[key]
    key = 'value'
    if new.has_key(key):
      self.value = new[key]
    else:
      self.value = 0
    key = 'is_browseable'
    self.is_browseable = get_boolean ( key, new )
    self.last_modified = datetime.datetime.now()
    self.save ()

class DmsRoles(models.Model):
  """ """
  name                  = models.CharField(max_length=30, unique=True)
  description           = models.CharField(max_length=80)
  perm_read             = models.BooleanField()
  perm_add              = models.BooleanField()
  perm_add_folderish    = models.BooleanField()
  perm_edit             = models.BooleanField()
  perm_edit_own         = models.BooleanField()
  perm_edit_folderish   = models.BooleanField()
  perm_manage           = models.BooleanField()
  perm_manage_own       = models.BooleanField()
  perm_manage_folderish = models.BooleanField()
  perm_manage_site      = models.BooleanField()
  perm_manage_user      = models.BooleanField()
  perm_manage_user_new  = models.BooleanField()

  class Meta:
    db_table = 'auth_role'

  def __unicode__(self):
    return self.name

  class Admin:
    list_display = ( 'id', 'name', 'description' )
    pass

class DmsUserUrlRole(models.Model):
  """ """
  user                  = models.ForeignKey(User)
  container             = models.ForeignKey(DmsContainer)
  role                  = models.ForeignKey(DmsRoles)

  def __unicode__(self):
    return smart_unicode(self.user) + ' :: ' + smart_unicode(self.container)

  class Admin:
    # ????? list_filter = ('role')
    list_display = ( 'id', 'user', 'container', 'role' )
    pass

  class Meta:
      db_table = 'auth_user_url_role'

  def save_user_url_role(self, user, container, role):
    """ initialisiert einen neuen Datensatz """
    self.user_id   = user
    self.container_id = container
    self.role_id   = role
    self.save()
    return self

class DmsQuota(models.Model):
  """ jeder User steht in seinem Home-Verzeichnis ein bestimmtes Quota zur Verfuegung """
  username            = models.CharField(max_length=60, unique=True)
  max                 = models.IntegerField(default=10000000)
  value               = models.IntegerField(default=0)

  def __unicode__(self):
      return self.username

  class Admin:
    list_display = ( 'username', 'max', 'value' )
    pass


class DmsOrg(models.Model):
  """ Schulen haben eine org_id > 0 """
  org_id                = models.IntegerField(unique=True)
  organisation          = models.CharField(max_length=120, db_index=True)
  sub_organisation      = models.CharField(max_length=80)
  street                = models.CharField(max_length=50)
  zip                   = models.CharField(max_length=10)
  town                  = models.CharField(max_length=50, db_index=True)
  phone                 = models.CharField(max_length=40)
  fax                   = models.CharField(max_length=40)
  email                 = models.URLField()
  homepage              = models.URLField()

  class Meta:
      db_table = 'auth_org'

  def __unicode__(self):
    return smart_unicode(self.org_id) + ' :: ' + self.organisation

  class Admin:
    list_display = ( 'id', 'org_id', 'organisation' )
    pass

class DmsOrgGroup(models.Model):
  """ Gruppen von Einrichtungen koennen hierdurch ausgewaehlt werden """
  name                  = models.CharField(max_length=80, db_index=True)
  contains              = models.CharField(max_length=40)

  class Meta:
      db_table = 'auth_org_group'

  def __unicode__(self):
    return smart_unicode(self.name) + ' :: ' + self.contains

  class Admin:
    list_display = ( 'id', 'name', 'contains' )
    pass

class DmsUserOrg(models.Model):
  """ """
  user                  = models.ForeignKey(User)
  # --- org = models.ForeignKey(DmsOrg) ist falsch, da org_id wegen der Schulnummern
  # --- extern vergeben wurden
  org_id                = models.IntegerField(db_index=True)

  class Meta:
    db_table = 'auth_user_org'

  def __unicode__(self):
    return smart_unicode(self.org_id) + ' :: ' + smart_unicode(self.user)

  class Admin:
    list_filter = ('org_id',)
    list_display = ('id', 'org_id', 'user')
    pass

#class DmsUserfolderConnected(models.Model):
#  """ gekoppelte Userfolder, um User gleichzeitig in mehreren Userfoldern eintragen zu koennen """
#  uf_master  = models.IntegerField(db_index=True)
#  uf_slave   = models.IntegerField()
#  uf_master_role = models.IntegerField()
#  uf_slave_role  = models.IntegerField()
#
#  class Meta:
#    db_table = 'auth_uf_connected'
#
#  def __unicode__(self):
#    return smart_unicode(self.uf_master) + ' :: ' + smart_unicode(self.uf_slave)
#
#  class Admin:
#    list_filter = ('uf_master_id', 'uf_slave_id')
#    list_display = ('id', 'uf_master_id', 'uf_slave_id', 'uf_master_role_id', 'uf_slave_role_id')
#    pass

class DmsGroup(models.Model):
  """ Unterorganisationseinheiten wie z.B. Klassen """
  # --- org_id muss anstelle von models.ForeignKey(DmsOrg) verwendet werden,
  # --- da org_id extern vorgegeben wird
  org_id                = models.IntegerField(db_index=True)
  description           = models.CharField(max_length=120)
  is_primary            = models.BooleanField(default=False)

  class Meta:
    db_table = 'auth_group_dms'

  def __unicode__(self):
    return  smart_unicode(self.org_id) + ' :: ' + self.description

  class Admin:
    # ??? list_filter = ('is_primary')
    list_display = ( 'id', 'org_id', 'description', 'is_primary' )
    pass

class DmsUserGroup(models.Model):
  """ """
  user                  = models.ForeignKey(User)
  group                 = models.ForeignKey(DmsGroup)

  class Meta:
    db_table = 'auth_user_group'

  def __unicode__(self):
    return  smart_unicode(self.user) + ' :: ' + smart_unicode(self.group)

  class Admin:
    # ??? list_filter = ('group')
    list_display = ( 'id', 'user', 'group' )
    pass

class DmsSubOrg(models.Model):
  """ Schulen haben eine org_id > 0 """
  """ Unterorganisationseinheiten wie z.B. Klassen """
  # --- org_id muss anstelle von models.ForeignKey(DmsOrg) verwendet werden,
  # --- da org_id extern vorgegeben wird
  org_id                = models.IntegerField(db_index=True)
  name                  = models.CharField(max_length=30, db_index=True)
  description           = models.CharField(max_length=80)

  class Meta:
    db_table = 'auth_sub_org'

  def __unicode__(self):
    return self.name

  class Admin:
    list_display = ( 'id', 'org_id', 'name', 'description' )
    pass

class DmsFeed(models.Model):
  """ RSS-Feed """
  name                = models.CharField(max_length=60, unique=True)
  title               = models.CharField(max_length=120)
  description         = models.CharField(max_length=180)
  link                = models.URLField()
  general_mode        = models.IntegerField(default=0)
  owner               = models.ForeignKey(User)
  is_deleted          = models.BooleanField(default=False)
  last_modified       = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
    return self.name

  class Admin:
    #fields = (
    #    (None, {'fields': ('username', 'password')}),
    #    (_('Personal info'), {'fields': ('sex', 'first_name', 'last_name', 'email')}),
    #    (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
    #    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    #)
    list_filter = ('general_mode', 'is_deleted', 'last_modified')
    #search_fields = ( 'name', 'title', 'owner')
    list_display = ( 'id', 'name', 'title', 'general_mode', 'owner', 'is_deleted', 'last_modified' )
    pass

class DmsFeedItem(models.Model):
  """ RSS-Feed-Item """
  feed                = models.ForeignKey(DmsFeed)
  item_container      = models.ForeignKey(DmsItemContainer)
  owner               = models.ForeignKey(User)
  is_browseable       = models.BooleanField(default=False)
  is_deleted          = models.BooleanField(default=False)
  last_modified       = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
    return smart_unicode(self.feed)

  class Admin:
    list_filter = ('is_browseable', 'is_deleted', 'last_modified')
    list_display = ( 'id', 'feed', 'owner', 'is_browseable', 'is_deleted', 'last_modified' )
    pass

  def save_values(self, feed, item_container, owner):
    """ initialiSiert einen neuen Datensatz """
    self.feed           = feed
    self.item_container = item_container
    self.owner          = owner
    self.is_browseable  = False
    self.is_deleted     = False
    self.last_modified  = datetime.datetime.now()
    self.save()

class DmsAntiSpam(models.Model):
  """ Fragen und Antworten fuer Mini-Abti-Spam-System """
  question            = models.CharField(max_length=120)
  answer              = models.CharField(max_length=20)

  def __unicode__(self):
    return self.answer

  class Admin:
    list_display = ( 'id', 'question', 'answer' )
    pass

class DmsSearchEngine(models.Model):
  """ Fragen und Antworten fuer Mini-Abti-Spam-System """
  name                = models.CharField(max_length=40)
  url_query           = models.CharField(max_length=240)

  def __unicode__(self):
    return self.name

  class Admin:
    pass

# -----------------------------------------------------
# Audit
# -----------------------------------------------------

OP_CHOICES = (
  ('a', _(u'Ergänzt')),
  ('e', _(u'Geändert')),
  ('d', _(u'Gelöscht')),
)

class DmsAudit(models.Model):
  """ Beschreibung der Aktivitaeten innerhalb des Sites ... """
  #org_id   = models.IntegerField(unique=True)
  app       = models.ForeignKey(DmsApp)
  path      = models.CharField(max_length=240, db_index=True)
  name      = models.CharField(max_length=200)
  title     = models.CharField(max_length=240)
  owner     = models.ForeignKey(User, db_index=True)
  operation = models.CharField(max_length=1, choices=OP_CHOICES)
  modified  = models.DateTimeField(default=datetime.datetime.now(), db_index=True)

  def __unicode__(self):
    return self.name

  class Meta:
    db_table = 'dms_audit'

# -----------------------------------------------------
# "Hauptprogramm"
# -----------------------------------------------------

dispatcher.connect(signal_pre_delete, signal=models.signals.pre_delete, sender=DmsItemContainer)
dispatcher.connect(signal_post_save, signal=models.signals.post_save, sender=DmsItemContainer)
