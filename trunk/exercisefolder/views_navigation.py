#-*-coding: utf-8 -*-
"""
/dms/exercisefolder/views_navigation.py

.. enthaelt den View zum Aendern der Zuordnung des linken Navigationsbereichs
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  02.05.2008  Beginn der Arbeit
"""

from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.queries        import get_site_url
from dms.queries        import save_navigation

from dms.roles          import require_permission
from dms.roles          import UserEditPerms
from dms.utils          import get_breadcrumb
from dms.utils          import get_tabbed_form
from dms.utils          import get_footer_email
from dms.utils          import get_folderish_actions

from dms.utils_navigation import get_navmenu_choices_left
from dms.folder.help_form import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
@require_permission('perm_manage_site')
def exercisefolder_navigation(request, item_container):
  """ Eigenschaften des Ordners aendern """

  class dms_itemForm(forms.Form):
    navigation_left = forms.ChoiceField(
                            choices=get_navmenu_choices_left(item_container.container.menu_left_id),
                            widget=forms.RadioSelect({'region|':True,})
                            )
  app_name = u'folder'
  my_title = _(u'Navigationspunkt auswählen')

  data_init = {'navigation_left': item_container.container.nav_name_left,}
  if request.method == 'POST' :
    data = request.POST.copy()
  else :
    data = data_init
  f = dms_itemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte
  tabs = [('tab_navigation', ['navigation_left',]),]
  content=get_tabbed_form(tabs, help_form, app_name, f)

  if request.method == 'POST' and not f.errors:
    save_navigation(item_container, data_init, f.data)
    return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
  else :
    user_perms = UserEditPerms(request.user.username, request.path)
    vars={'content_div_style': 'frame-main-manage',
          'site'             : item_container.container.site,
          'my_name'          : item_container.item.name,
          'action'           : get_folderish_actions(request,user_perms, item_container, app_name, False),
          'breadcrumb'       : get_breadcrumb(item_container),
          'errors'           : f.errors,
          'content'          : content,
          'title'            : my_title,
          'sub_title'        : item_container.item.title,
          'footer_email'     : get_footer_email(item_container.item),
          'last_modified'    : item_container.get_last_modified(),
          #'next'             : get_site_url(item_container, 'index.html/navigation/'),
          'submit'           : my_title
        }
    return render_to_response ( 'app/base_edit.html', vars )
