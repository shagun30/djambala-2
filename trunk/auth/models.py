from django.core import validators
from django.core.exceptions import ImproperlyConfigured
from django.db import backend, connection, models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
import datetime

from django.utils.translation import ugettext as _

##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
# Starke Vereinfachung
# Hans Rauch, 14.01.2007
#
##############################################################################

import sha, binascii
from binascii import b2a_base64, a2b_base64
from random import choice, randrange

class SSHADigestScheme:
    '''
    SSHA is a modification of the SHA digest scheme with a salt
    starting at byte 20 of the base64-encoded string.
    '''
    # Source: http://developer.netscape.com/docs/technote/ldap/pass_sha.html

    def generate_salt(self):
        # Salt can be any length, but not more than about 37 characters
        # because of limitations of the binascii module.
        # 7 is what Netscape's example used and should be enough.
        # All 256 characters are available.
        salt = ''
        for n in range(7):
            salt += chr(randrange(256))
        return salt

    def encrypt(self, pw):
        pw = str(pw)
        salt = self.generate_salt()
        return b2a_base64(sha.new(pw + salt).digest() + salt)[:-1]

    def validate(self, reference, attempt):
        try:
            ref = a2b_base64(reference)
        except binascii.Error:
            # Not valid base64.
            return 0
        salt = smart_str(ref[20:])
        compare = b2a_base64(sha.new(smart_str(attempt) + salt).digest() + salt)[:-1]
        return (compare == reference)

def pw_validate(reference, attempt):
  """Validate the provided password string, which uses LDAP-style encoding
  notation.  Reference is the correct password, attempt is clear text
  password attempt."""
  lp = len('{SSHA}')
  return SSHADigestScheme().validate(reference[lp:], attempt)

def pw_encrypt(pw):
  """Encrypt the provided plain text password using the encoding if provided
  and return it in an LDAP-style representation."""
  return '{SSHA}' + SSHADigestScheme().encrypt(pw)

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    lp = len('{SSHA}')
    #return SSHADigestScheme().validate(reference[lp:], attempt)
    return SSHADigestScheme().validate(enc_password[lp:], raw_password)
    """
    algo, salt, hsh = enc_password.split('$')
    if algo == 'md5':
        import md5
        return hsh == md5.new(salt+raw_password).hexdigest()
    elif algo == 'sha1':
        import sha
        return hsh == sha.new(salt+raw_password).hexdigest()
    raise ValueError, "Got unknown password algorithm type in password."
    """

class SiteProfileNotAvailable(Exception):
    pass

class UserManager(models.Manager):
    def create_user(self, username, email, password):
        "Creates and saves a User with the given username, e-mail and password."
        now = datetime.datetime.now()
        user = self.model(None, username, '', '', email.strip().lower(), 'placeholder', False, True, False, now, now)
        user.set_password(password)
        user.save()
        return user

    def make_random_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        "Generates a random password with the given length and given allowed_chars"
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        from random import choice
        return ''.join([choice(allowed_chars) for i in range(length)])

class User(models.Model):
    """Users within the Django authentication system are represented by this model.

    Username and password are required. Other fields are optional.
    """
    username = models.CharField(_(u'username'), max_length=60, unique=True, validator_list=[validators.isAlphaNumericURL],
      help_text=_(u"Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."))
    sex = models.CharField(_(u'sex'), max_length=10)
    title = models.CharField(_(u'title'), max_length=30, blank=True)
    first_name = models.CharField(_(u'first name'), max_length=30, blank=True)
    last_name = models.CharField(_(u'last name'), max_length=40, blank=True)
    email = models.EmailField(_(u'e-mail address'), blank=True)
    password = models.CharField(_(u'password'), max_length=80, 
      help_text=_(u"Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    is_staff = models.BooleanField(_(u'staff status'), default=False, help_text=_(u"Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_(u'active'), default=True, 
      help_text=_(u"Designates whether this user can log into the Django admin. Unselect this instead of deleting accounts."))
    is_superuser = models.BooleanField(_(u'superuser status'), default=False, 
      help_text=_(u"Designates that this user has all permissions without explicitly assigning them."))
    last_login = models.DateTimeField(_(u'last login'), default=datetime.datetime.now)
    date_joined = models.DateTimeField(_(u'date joined'), default=datetime.datetime.now)
    objects = UserManager()
    class Meta:
        verbose_name = _(u'user')
        verbose_name_plural = _(u'users')
        ordering = ('username',)
    class Admin:
        fields = (
            (None, {'fields': ('username', 'password')}),
            (_(u'Personal info'), {'fields': ('sex', 'first_name', 'last_name', 'email')}),
            (_(u'Permissions'), {'fields': ('is_active', 'is_superuser')}),
            (_(u'Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
        list_display = ('username', 'email', 'sex', 'title', 'first_name', 'last_name')
        list_filter = ('is_superuser',)
        search_fields = ('username', 'first_name', 'last_name', 'email')

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return u"/users/%s/" % self.username

    def is_anonymous(self):
        "Always returns False. This is a way of comparing User objects to anonymous users."
        return False

    def is_authenticated(self):
        """Always return True. This is a way to tell if the user has been authenticated in templates.
        """
        return True

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        if self.title :
            full_name = u'%s %s %s' % (self.title, self.first_name, self.last_name)
        else :
            full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_standard_name(self):
        "Returns the last_name, first_name"
        if self.title :
            full_name = u'%s, %s %s' % (self.last_name, self.title, self.first_name)
        else :
            full_name = u'%s, %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def set_password(self, raw_password):
        #import sha, random
        #algo = 'sha1'
        #salt = sha.new(str(random.random())).hexdigest()[:5]
        #hsh = sha.new(salt+raw_password).hexdigest()
        #self.password = '%s$%s$%s' % (algo, salt, hsh)
        self.password = pw_encrypt(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        return check_password(raw_password, self.password)

    def has_perm(self, perm):
        "Returns True if the user has the specified permission."
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        return perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        "Returns True if the user has any permissions in the given app label."
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        return bool(len([p for p in self.get_all_permissions() if p[:p.index('.')] == app_label]))

    def get_and_delete_messages(self):
        messages = []
        for m in self.message_set.all():
            messages.append(m.message)
            m.delete()
        return messages

    def email_user(self, subject, message, from_email=None):
        "Sends an e-mail to this User."
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not settings.AUTH_PROFILE_MODULE:
                raise SiteProfileNotAvailable
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
                model = models.get_model(app_label, model_name)
                self._profile_cache = model._default_manager.get(user__id__exact=self.id)
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache

class AnonymousUser(object):
    id = None
    username = ''

    def __init__(self):
        pass

    def __unicode__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1 # instances always return the same hash value

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def set_password(self, raw_password):
        raise NotImplementedError

    def check_password(self, raw_password):
        raise NotImplementedError

    def get_and_delete_messages(self):
        return []

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

