#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# ---> cron-job

from dms.resource.queries import delete_old_events
import mx.DateTime

days_wait = 45

now = mx.DateTime.now()
n = delete_old_events( days_wait, now)

#print n