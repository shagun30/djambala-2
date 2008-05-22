# -*- coding: utf-8 -*-
"""
/dms/eventboard/views_show.py

.. zeigt den Inhalt eines Terminkalenders an
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  04.06.2007  Beginn der Arbeit
0.02  21.01.2008  Monatsansicht
"""

from django.http        import HttpResponse
from django.shortcuts   import render_to_response

from django.utils.translation import ugettext as _

from django.template.loader   import get_template
from django.template          import Context

from dms.queries        import get_visible_comment_count_by_item_containers
from dms.queries        import get_item_container_by_path_and_name
from dms.queries        import get_site_url

from dms.utils          import show_link
from dms.utils          import get_link_by_item_container
from dms.utils_form     import get_folderish_vars_show
from dms.utils_form     import get_folderish_vars_show

from dms.eventboard.utils   import get_folder_content
from dms.eventboard.utils   import get_user_support

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------
def get_visibilty(item_container):
  """ """
  if item_container.visible_start == item_container.visible_end:
    return ' <i>[' + u'%s' % item_container.visible_start.strftime('%d.%m.%Y') + ']</i>'
  else:
    return ' <i>[' + u'%s-%s' % \
                  ( item_container.visible_start.strftime('%d.%m.%Y'),
                    item_container.visible_end.strftime('%d.%m.%Y')
                  ) + ']</i>'

# -----------------------------------------------------
def get_ordering(item_container):
  """ Sortierreihenfolge in der Listenanzeige """
  if item_container.item.integer_3==1: return True
  else                               : return False

# -----------------------------------------------------
def get_items_view(request, item_container):
  """ erzeugt die Section-Ansicht der im Terminkalender enthaltenen Ereignisse """
  t_list = get_template('app/eventboard/eventlist.html')
  content = ''
  t_section = get_template('app/eventboard/eventitem.html')
  t_section_old = get_template('app/eventboard/eventitem-old.html')
  t_archives = get_template('app/archives.html')
  if item_container.item.name.find('archiv') == 0:
    items = get_folder_content(item_container, 'all', get_ordering(item_container))
    items_old_dist = []
  else:
    items = get_folder_content(item_container, 'new', get_ordering(item_container))
    items_old_dist = get_folder_content(item_container, 'old', get_ordering(item_container))
  items_old = []
  for i in items_old_dist:
    if i.item.app.name == 'dmsEventItem':
      items_old.append(i)
  archives = []
  comment_counts = get_visible_comment_count_by_item_containers(items)
  content_list = t_list.render( Context({'items':items, 'title': _(u'Übersicht')}) )
  for i in items:
    if i.item.url_more != '':
      more_items = show_link(i.item.url_more, _(u'Weitere Infos ...'), i.item.url_more_extern,
                              url_class='navLink')
    else:
      more_items = ''
    if i.item.app.name == 'dmsEventboard':
      archives.append(show_link(i.get_absolute_url(), i.item.title))
    else:
      visibility = get_visibilty(i)
      last_modified = i.get_last_modified() + visibility
      cSection = Context ({
                            'name'         : i.item.name,
                            'title'        : i.item.title + visibility,
                            'sub_title'    : i.item.sub_title,
                            'text'         : i.item.text,
                            'user_name'    : i.item.string_1,
                            'email'        : i.item.string_2,
                            'date'         : i.get_last_modified(),
                            'image_url'    : i.item.image_url,
                            'image_url_url': i.item.image_url_url,
                            'image_extern' : i.item.image_extern,
                            'last_modified': i.get_last_modified(),
                            'more_infos'   : more_items,
                            'comments'     : comment_counts[i.item.id]
                          })
      content += t_section.render(cSection)
  if items_old != [] or archives != []:
    if archives != []:
      archiv_txt = t_archives.render( Context({'title': _(u'Archiv alter Kalender'),
                                                'archives': archives}) )
    else:
      archiv_txt = ''
    cSection = Context ({ 'items_old': items_old, 'archives': archiv_txt, })
    content += t_section_old.render(cSection)
  return content_list + \
          t_list.render( Context({'title': item_container.item.title,}) ) + \
          content

# -----------------------------------------------------
def get_items_monthview(request, item_container, date_calendar=None):
  """ erzeugt die Kalender-Ansicht der im Terminkalender enthaltenen Ereignisse """
  import calendar, time
  
  MONTHNAME = [ 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
                'August', 'September', 'Oktober', 'November', 'Dezember' ]
  DAYNAME   = [ 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
                'Samstag', 'Sonntag']
  
  calendar.setfirstweekday(calendar.MONDAY)
  
  today = time.strftime("%Y.%m.%d")
  if date_calendar != None:
    this_date = date_calendar # Format-Fehler abfangen?
  else:
    this_date = today
  y,m,d = this_date.split('.')
  dayrange = list(calendar.monthrange(int(y),int(m)))
  days = dayrange[1]
  nameId = dayrange[0]
  base_date = this_date[:this_date.rfind('.')+1]
  items = get_folder_content(item_container, 'all', get_ordering(item_container))
  # -- Vorbereitung
  dDays = {}
  for day in xrange(days) :
    d = day + 1
    if d < 10 :
      curr_date = base_date + '0' + str(d)
    else :
      curr_date = base_date + str(d)
    dDays[curr_date] = []
  periods = []
  for item_cont in items :
    if dDays.has_key(item_cont.visible_start.strftime("%Y.%m.%d")) :
      dDays[item_cont.visible_start.strftime("%Y.%m.%d")].append ( item_cont )
    if item_cont.visible_start.strftime("%Y.%m.%d") != item_cont.visible_end.strftime("%Y.%m.%d") :
      if dDays.has_key(item_cont.visible_end.strftime("%Y.%m.%d")) :
        dDays[item_cont.visible_end.strftime("%Y.%m.%d")].append ( item_cont )
      periods.append(item_cont)
  # Ereignisse, die ueber mehrere Tage gehen, auswerten
  for day in xrange(days) :
    d = day + 1
    if d < 10 :
      curr_date = base_date + '0' + str(d)
    else :
      curr_date = base_date + str(d)
    for item_cont in periods :
      if (item_cont.visible_start.strftime("%Y.%m.%d") < curr_date) and (curr_date < item_cont.visible_end.strftime("%Y.%m.%d")) and (nameId < 5) :
        dDays[curr_date].append ( item_cont )
    nameId = ( nameId + 1 ) % 7
  year = int(y)
  nextYear = year
  prevYear = year
  if int(m) == 12 :
    nextYear += 1
    nextMonth = 1
  else :
    nextMonth = int(m) + 1
  if int(m) == 1 :
    prevMonth = 12
    prevYear -= 1
  else :
    prevMonth = int(m) - 1
  if prevMonth < 10 :
    prevMonth = '0' + str(prevMonth)
  if nextMonth < 10 :
    nextMonth = '0' + str(nextMonth)
  date_cal_prev = str(prevYear) + '.' + str(prevMonth) + '.01'
  date_cal_next = str(nextYear) + '.' + str(nextMonth) + '.01'
  content = ''
  t_monthhead = get_template('app/eventboard/month_head.html')
  cSection = Context ({
                        'monthname'     : MONTHNAME[int(m)-1],
                        'year'          : str(y),
                        'date_cal_prev' : str(date_cal_prev),
                        'date_cal_next' : str(date_cal_next)
                      })
  content += t_monthhead.render(cSection)
  nameId = dayrange[0]
  for day in xrange(days) :
    d = day + 1
    if d < 10 :
      curr_date = base_date + '0' + str(d)
    else :
      curr_date = base_date + str(d)
    if nameId >= 5 :
      weekend = 1
    else:
      weekend = 0
    if curr_date==today:
      is_today = 1
    else:
      is_today = 0
    lItems = dDays[curr_date]
    my_events = []
    for i in lItems :
      cont      = ''
      continued = ''
      startdate = i.visible_start.strftime("%Y.%m.%d")
      enddate  = i.visible_end.strftime("%Y.%m.%d")
      if (enddate != startdate) :
        if startdate == curr_date:
          cont = ' &raquo;&raquo;'
        else:
          continued = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&raquo;&raquo; '
      my_events += [{'cont': cont,
                     'continued': continued,
                     'title': i.item.title,
                     'url': i.item.name}]
    t_monthrow = get_template('app/eventboard/month_row.html')
    cSection = Context ({
                          'weekend'   : weekend,
                          'day'       : str(d),
                          'is_today'  : is_today,
                          'day_name'  : DAYNAME[nameId][:2],
                          'infos'     : my_events,
                          'curr_date' : curr_date
                        })
    content += t_monthrow.render(cSection)
    nameId = ( nameId + 1 ) % 7
  t_monthfoot = get_template('app/eventboard/month_foot.html')
  cSection = Context ({ 'date_cal_prev' : str(date_cal_prev),
                        'date_cal_next' : str(date_cal_next)
                      })
  content += t_monthfoot.render(cSection)
  return content

# -----------------------------------------------------
def get_dayitems(items, this_date):
  items_this_date = []
  for item_cont in items:
    if (item_cont.visible_start.strftime('%Y.%m.%d')<=this_date) and (item_cont.visible_end.strftime('%Y.%m.%d')>=this_date):
      items_this_date.append(item_cont)
  return items_this_date

# -----------------------------------------------------
def get_items_dayview(request, item_container, this_date):
  """ erzeugt die Section-Ansicht der im Terminkalender enthaltenen Ereignisse eines bestimmten Tages """
  # this_date wird im Format YY.mm.dd erwartet.
  t_list = get_template('app/eventboard/eventlist.html')
  content = ''
  t_section = get_template('app/eventboard/eventitem.html')
  items_all = get_folder_content(item_container, 'all', get_ordering(item_container))
  items = get_dayitems(items_all, this_date)
  del items_all
  comment_counts = get_visible_comment_count_by_item_containers(items)
  tmp = this_date.split('.')
  my_date = tmp[2]+'.'+tmp[1]+'.'+tmp[0]
  content_list = t_list.render( Context({'items':items, 'title': _(u'Übersicht'), 'single_date': my_date}) )
  for i in items:
    if i.item.url_more != '':
      more_items = show_link(i.item.url_more, _(u'Weitere Infos ...'), i.item.url_more_extern,
                              url_class='navLink')
    else:
      more_items = ''
    if i.item.app.name == 'dmsEventboard':
      archives.append(show_link(i.get_absolute_url(), i.item.title))
    else:
      visibility = get_visibilty(i)
      last_modified = i.get_last_modified() + visibility
      cSection = Context ({
                            'name'         : i.item.name,
                            'title'        : i.item.title + visibility,
                            'sub_title'    : i.item.sub_title,
                            'text'         : i.item.text.strip(),
                            'user_name'    : i.item.string_1,
                            'email'        : i.item.string_2,
                            'date'         : i.get_last_modified(),
                            'image_url'    : i.item.image_url,
                            'image_url_url': i.item.image_url_url,
                            'image_extern' : i.item.image_extern,
                            'last_modified': i.get_last_modified(),
                            'more_infos'   : more_items,
                            'comments'     : comment_counts[i.item.id]
                          })
      content += t_section.render(cSection)
  return content_list + \
          t_list.render( Context({'title': item_container.item.title,}) ) + \
          content


# -----------------------------------------------------
def get_items_view_simple(request, item_container):
  """ erzeugt eine Ubersicht der im Terminkalender enthaltenen Ereignisse """
  from django.template.loader import get_template
  from django.template import Context
  t_list = get_template('app/folder/section.html')
  content = ''
  item_containers = get_folder_content(item_container, 'new', get_ordering(item_container))
  links = []
  for ic in item_containers:
    links.append(get_link_by_item_container(ic) + get_visibilty(ic))
  if item_container.item.has_user_support and ( item_container.item.integer_4 != 1 or \
     (item_container.item.integer_4 == 1 and request.user.is_authenticated()) ):
    links.append(show_link(get_site_url(item_container, 'index.html') + '/add/eventitem/', _(u'<i>Neuer Termin ...</i>')))
  else:
    links.append(show_link(get_site_url(item_container, 'index.html'), _(u'Zum Terminkalender')))
  content_list = t_list.render( Context({'links':links, 'title': _(u'Terminkalender')}) )
  return content_list

# -----------------------------------------------------
def eventboard_show ( request, item_container ):
  """ zeigt den Inhalt eines Terminkalenders """
  app_name = 'eventboard'
  if request.GET.has_key('single_date'):
    single_date = request.GET['single_date']
  else:
    single_date = None
  if single_date != None:
    # single_date wird im Format YY.mm.dd erwartet.
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_items_dayview(request, item_container, single_date),
                                   get_user_support(item_container))
    return render_to_response ( 'app/base_folderish.html', vars )
  # integer_2 = 0 : Listenansicht
  # integer_2 = 1 : Monatsansicht
  if item_container.item.integer_2==0:
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_items_view(request, item_container),
                                   get_user_support(item_container))
  else:
    if request.GET.has_key('date_calendar'):
      dt_cal = request.GET['date_calendar']
    else:
      dt_cal = None
    vars = get_folderish_vars_show(request, item_container, app_name,
                                   get_items_monthview(request, item_container, dt_cal),
                                   get_user_support(item_container))
  return render_to_response ( 'app/base_folderish.html', vars )

# -----------------------------------------------------
def eventboard_ajax_get_events(request, item_container):
  """ liefert die aktuellen Ereignisse """
  response = ''
  event_path = item_container.item.string_2
  if event_path != '':
    path = item_container.container.path + event_path[1:]
    ic = get_item_container_by_path_and_name(path, '')
    if ic != None:
      response = get_items_view_simple(request, ic)
  return HttpResponse(response, mimetype="text/html; charset=utf-8")
