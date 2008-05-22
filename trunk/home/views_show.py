# -*- coding: utf-8 -*-
"""
/dms/home/views_show.py

.. zeigt den Inhalt eines Home-Verzeichnisses an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  15.04.2008  Beginn der Arbeit
"""

from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from dms.roles                import UserEditPerms
from dms.roles          import require_permission

from dms.queries              import get_site_url
from dms.queries              import is_file_by_item_container
from dms.queries              import get_my_homes
from dms.queries              import get_item_container_by_path
from dms.queries              import get_role_by_id
from dms.queries              import get_user_by_username

from dms.utils                import get_link_by_item_container
from dms.utils_form           import get_folderish_vars_show

from dms.encode_decode  import encode_html
from dms.folder.utils   import get_folder_content
from dms.home.utils     import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_folderish')
def home_show ( request, item_container ):
  """ zeigt den Inhalt des Home-Verzeichnisses """

  def get_section_view(items, sections, last_modified):
    """ erzeugt die Section-Ansicht der im Ordner enthaltenen Objekte """
    from django.template.loader import get_template
    from django.template import Context
    tSection = get_template('app/folder/section.html')
    user = get_user_by_username(item_container.item.name)
    my_homes = get_my_homes(user)
    links = []
    for home in my_homes:
      try:
        ic = get_item_container_by_path(home.container.path)
        role = get_role_by_id(home.role.id)
        link = '%s &nbsp;&nbsp; (%s)' % (get_link_by_item_container(ic), role.name)
        links.append(link)
      except:
        # Ordner existiert nicht
        pass
    cSection = Context ( { 'section': _(u'Meine Seiten'), 'links': links } )
    homes = tSection.render ( cSection)

    content = ''
    unknown = _(u'Unbekannter Zwischentitel')
    section = '--START--'
    links = []
    folder_is_protected = (item_container.container.min_role_id < 2000)
    for i in items:
      if last_modified < i.last_modified:
        last_modified = i.last_modified
      if section != i.section :
        if section != unknown :
          if section != '--START--' and links != []:
            cSection = Context ( { 'section': section, 'links': links } )
            content += tSection.render ( cSection)
          if i.section in sections :
            section = i.section
          else :
            section = unknown
          links = []
      if is_file_by_item_container(i):
        user_perms = UserEditPerms(request.user.username, request.path)
        if user_perms.perm_read:
          links.append(get_link_by_item_container(i, folder_is_protected=folder_is_protected))
        else:
          links.append(i.item.title)
      else:
        links.append(get_link_by_item_container(i, folder_is_protected=folder_is_protected))
    if section != '--START--' and links != []:
      cSection = Context ( { 'section': section, 'links': links } )
      content += tSection.render ( cSection)
    return homes + content, last_modified

  if request.GET.has_key('section'):
    section = request.GET['section']
  else:
    section = ''
  app_name = 'home'
  items, sections, d_sections = get_folder_content(item_container, this_section=section)
  last_modified = item_container.last_modified
  content, last_modified = get_section_view(items, sections, last_modified)
  vars = get_folderish_vars_show(request, item_container, app_name, content,
                                 get_user_support(item_container, item_container.item.name), 
                                 last_modified=last_modified)
  vars['ajax_url'] = get_site_url(item_container, 'index.html/ajax/')
  vars['user_support_header'] = _(u'Aktionen')
  return render_to_response ( 'app/home/base_folderish.html', vars )

