from django.conf.urls.defaults import *

from dms.css.views import generate_css_data

urlpatterns = patterns('',
    (r'^css_generate/$', generate_css_data ),
)
