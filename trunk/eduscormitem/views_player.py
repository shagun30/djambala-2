# -*- coding: utf-8 -*-
"""
/dms/eduscormitem/views_player.py

.. zeigt den Inhalt eines Scorm-Paketes an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  12.03.2008  Beginn der Arbeit
"""

import pickle

from django.shortcuts   import render_to_response
from django.template    import Context
from django.template.loader import get_template
from django.utils.safestring  import mark_safe

from django.utils.translation import ugettext as _

from dms.queries            import get_base_site_url
from dms.edufileitem.utils  import get_edu_file_url
from dms.file.utils         import get_file_path
from dms.utils_form         import get_item_vars_show

from dms_ext.extension      import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def scorm_top(request, item_container):
  """ zeigt den oberen Bereich des Scorm-Players """
  app_name = 'edutextitem'
  vars = get_item_vars_show(request, item_container, app_name)
  return render_to_response ( 'scorm/top.html', vars )

# -----------------------------------------------------
def scorm_left(request, item_container):
  """ zeigt den linken Bereich des Scorm-Players """

  declare_str = ''
  function_str = ''
  nodes = ['', '', '', '', '', '']

  def get_node_name(index):
    return 'node_%i' % index

  def get_var_name(index):
    return 'var %s;\n' % get_node_name(index)

  def get_function(nodes, index, level, href, title):
    """ """
    this_node = get_node_name(index)
    nodes[level+1] = this_node
    i = level + 2
    while i < len(nodes):
      nodes[i] = ''
      i += 1
    res = "var %s = createMenu(%s, '%s', '%s');\n" % (this_node, nodes[level], href, title)
    return res, nodes

  app_name = 'edutextitem'
  base_url = get_edu_file_url(item_container)
  nav_pickle = '%s/navigation/navigation.pickle' % get_file_path(item_container)
  f = open(nav_pickle, 'r')
  nav_list = pickle.load(f)
  f.close()

  index = 0
  nodes[0] = get_node_name(0)
  function_str += 'var %s = tree.getRoot();\n' % nodes[0]
  index += 1

  for d in nav_list:
    declare_str += get_var_name(index)
    level = d['level']
    href = d['href']
    title = d['title']
    line, nodes = get_function(nodes, index, level, href, title)
    function_str += line
    index += 1

  vars = get_item_vars_show(request, item_container, app_name)
  vars['scorm_base'] = '%s/scorm/' % get_edu_file_url(item_container)
  vars['vars'] = mark_safe(declare_str)
  vars['function_calls'] = mark_safe(function_str)
  return render_to_response ( 'scorm/left.html', vars )

# -----------------------------------------------------
def scorm_index(request, item_container):
  """ zeigt den Scorm-Player """
  app_name = 'edutextitem'
  vars = {}
  vars['scorm_base'] = '%s/scorm/' % get_edu_file_url(item_container)
  vars['ajax_url'] = get_base_site_url() + '/index.html/ajax/scorm_ajax_call'
  return render_to_response ( 'scorm/index.html', vars )
