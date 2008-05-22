"""
Creates permissions for all installed apps that need permissions.
"""

from django.dispatch import dispatcher
from django.db.models import get_models, signals

from django.utils.translation import ugettext as _

from dms.auth import models as auth_app

def create_superuser(app, created_models, verbosity, **kwargs):
    from dms.auth.models import User
    from dms.auth.create_superuser import createsuperuser as do_create
    if User in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Django's auth system, which means you don't have " \
                "any superusers defined.\nWould you like to create one now? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                do_create()
            break

dispatcher.connect(create_superuser, sender=auth_app, signal=signals.post_syncdb)
