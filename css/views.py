#-!-coding: utf-8 -!-

from django.shortcuts import render_to_response

from django.utils.translation import ugettext as _

import dms.settings
import copy

from dms.roles          import require_permission
from dms.utils_form     import get_item_vars_show
from dms.queries        import get_top_item_container
from dms.queries        import get_site_by_id

def save_css(name, vars):
  """ """
  from django.template.loader import get_template
  from django.template import Context
  import os
  # -- CSS-Datei ins Dateisystem schreiben
  path = dms.settings.MEDIEN_ROOT + 'skin_style/' + name + '/'
  url  = dms.settings.MEDIEN_URL + 'skin_style/' + name + '/'
  vars['url'] = url
  vars['name'] = name
  vars['base_site_url'] = dms.settings.BASE_SITE_URL
  # -- Parametrisierung durchfuehren
  t = get_template('base_css.html')
  c = Context(vars)
  try :
    os.makedirs ( path )
  except :
    pass
  path += 'css_' + name + '.css'
  f = open ( path, 'w' )
  f.write ( t.render(c) )
  f.close ()

@require_permission('perm_manage_site')
def generate_css_data(request):
  """ erzeugt landesspezifische CSS-Dateien """
  my_module = __import__(u'dms.css.'+dms.settings.CSS_ORG, globals(), locals(), [''])
  return my_module.generate_my_css_data(request, save_css)
