# -*- coding: utf-8 -*-
"""
/dms/resource/views_show.py

.. zeigt den Inhalt einer Ressourcenverwaltung an
         Django content Management System

Werner Fabian
w.fabian@afl.hessen.de

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  28.01.2008  Uebernahme von Folder
....  ....
0.05  31.03.       Step 1,2,3
0.06  14.04.       ein- und mehrtaegig als Reiter
...
0.08  30.04.       Anzeige Kategorien und Ressourcen,
                   Kategorien anlegen, löschen
0.09  20.05.2008   get_userfolder_org_id (hr)
"""

import datetime

from django             import newforms as forms

from django.template        import Context
from django.template.loader import get_template

from django.shortcuts   import render_to_response
#from django.http        import HttpResponseRedirect
#from django.views.decorators.vary import vary_on_headers

from django.utils.translation import ugettext as _

#from dms.utils          import get_link_by_item_container
from dms.utils          import get_tabbed_form
from dms.utils          import clean_data
from dms.utils_base     import convert_str_to_date
from dms.utils_base     import show_link

from dms.utils_form     import get_folderish_vars_add
from dms.utils_form     import get_folderish_vars_edit
from dms.utils_form     import get_folderish_vars_show

#from dms.queries        import is_protected
from dms.queries        import get_org_by_username
from dms.queries        import get_user

#from dms.folder.utils   import get_folder_content
#from dms.projectgroup.utils   import get_user_support

from dms_ext.extension        import * # dms-Funktionen ueberschreiben

from dms.resource.utils       import feedback_vars
from dms.resource.utils       import get_app_name
from dms.resource.help_form   import help_form

from dms.queries              import get_userfolder_org_id
from dms.resource.queries     import exist_settings_org_id
from dms.resource.queries     import get_org_settings
from dms.resource.queries     import append_event
from dms.resource.queries     import get_my_events
from dms.resource.queries     import get_resource
from dms.resource.queries     import get_type_of_resource
from dms.resource.queries     import get_resource_list
from dms.resource.queries     import delete_event
from dms.resource.queries     import append_type
from dms.resource.queries     import delete_type
from dms.resource.queries     import append_resource

from dms.resource.utils       import get_type_res_list
from dms.resource.utils       import get_form_tab_row
from dms.resource.utils       import get_periods_by_id
from dms.resource.utils       import get_free_resource_list
from dms.resource.utils       import resource_unused

import mx.DateTime

# -----------------------------------------------------
def get_types_form_list(my_types):
  """ """
  ret = []
  for item in my_types:
    ret.append( (item[0].id, item[0].description, item[1]) )
  return ret
  
# -----------------------------------------------------
def get_periods_form_list(org_id):
  """ """
  ret = []
  for per in get_org_settings(org_id):
    ret.append( (per.id, per.name) )
  return ret

# -----------------------------------------------------
def get_var_list_OBSOLETE(var_name, n_count): # evtl. fuer spaeter
  """ baut eine Liste mit Variablennamen zusammen """
  var_list = []
  for n in xrange(n_count):
    var_list.append(var_name + '_%02i' % n)
  return var_list

# -----------------------------------------------------
def get_datetimes(org_id, clean_post):
  is_ok = False
  days = 0 # *eintaegig als Standard*
  if clean_post.has_key('res_time'):
    restime = clean_post['res_time']
  else:
    restime = ''
  if clean_post['res_day']!='' and restime!='':
    is_ok = True
  # Falls beide ausgefuellt, wird 'eintaegig' genommen.
  elif clean_post['date_start']!='' and clean_post['date_end']!='':
    days = 1 # *mehrtaegig*
    is_ok = True
  elif (clean_post['res_day']=='' and restime=='') and (clean_post['date_start']!='' or clean_post['date_end']!=''):
    days = 1 # *mehrtaegig*
  else:
    pass
  if not is_ok:
    return (0,0,days)
    # Rueckgabewert fuer Vorbesetzung?
  elif days == 0: # *eintaegig*
    date_start  = clean_post['res_day']
    date_end    = date_start
    my_res_time = clean_post['res_time']
    
    if type(my_res_time)!=type([]):
      my_res_time = [my_res_time]
    my_times = get_periods_by_id(org_id, my_res_time)
    time_start = my_times[0][0]
    if my_times[1][2]==0:
      time_end = my_times[1][0]
    else:
      time_end = my_times[1][1]
  else: # days : *mehrtaegig*
    date_start = clean_post['date_start']
    date_end   = clean_post['date_end']
    time_start = "00:00"
    time_end   = "23:59" # inclusive letzter Tag
  my_datetime_start = date_start + " " + time_start    #NICHT  + ":00"
  my_datetime_end   = date_end   + " " + time_end      #NICHT  + ":00"
  return my_datetime_start, my_datetime_end, days

# -----------------------------------------------------
def resource_show_my_events(request, item_container):
  """ zeigt das Eingabeformular fuer Reservierung """
  app_name = get_app_name()
  my_user_id = get_user(request.user.username).id
  my_events_0 = get_my_events(my_user_id)
  my_events = []
  for e in my_events_0:
    dummy, my_typedescr   = get_type_of_resource(e.resource_id)
    my_resdescr    = get_resource(e.resource_id).description
    datetime_start = e.datetime_start.strftime("%d.%m.%Y %H:%M")
    my_event = {'id':e.id, 'typedescr':my_typedescr, 'resdescr':my_resdescr, 'dtstart':datetime_start}
    date_start = e.datetime_start.strftime("%d.%m.%Y")
    date_end   = e.datetime_end.strftime("%d.%m.%Y")
    if date_start!=date_end:
      datetime_end = e.datetime_end.strftime("%d.%m.%Y %H:%M")
    else:
      datetime_end = e.datetime_end.strftime("%H:%M")
    my_event['dtend'] = datetime_end
    if mx.DateTime.Parser.DateTimeFromString(datetime_start)<mx.DateTime.now():
      my_event['in_use'] = 1
    my_events += [ my_event ]
  vars = get_folderish_vars_show(request, item_container, app_name, '', 
                                  False)
  vars['title'] = _(u"Ressourcenverwaltung: Übersicht")
  vars['next'] = item_container.get_absolute_url() + '/show_my_events/'
  if len(my_events)>0:
    vars['my_events'] = my_events
    vars['next_del'] = item_container.get_absolute_url() + "/del_event/"
  vars['action_block'] = show_link(item_container.get_absolute_url(), _(u'Reservieren'))
  #'<a href="index.html">Reservieren</a>'
  return render_to_response('app/resource/my_reservations.html', vars)

# -----------------------------------------------------
def resource_del_event(request, item_container):
  """ loescht eine oder mehrere eigene Ressource(n) """
  app_name = get_app_name()
  clean_post = clean_data( request.POST.copy() )
  if clean_post.has_key('event'):
    my_events = clean_post['event']
    if  type(my_events)!=type([]):
      my_events = [my_events]
    for i in my_events:
      delete_event( int(i))
    vars = feedback_vars(request, item_container, app_name, _(u"Die markierten Ressourcen wurden frei gegeben."), '')
  else:
    vars = feedback_vars(request, item_container, app_name, _(u"Es waren keine Ressourcen zur Freigabe markiert."), '')
  vars['next'] = item_container.get_absolute_url() + '/show_my_events/'
  return render_to_response('app/resource/feedback.html', vars)
  
# -----------------------------------------------------
def show_input_form(request, item_container, org_id, app_name, step, clean_post):
  """ zeigt das Eingabeformular fuer Reservierung """
  if step == 1:
    class DmsItemForm(forms.Form):
      """ Elemente des Eingabeformulars """
      res_day            = forms.DateField(required=False, input_formats=['%d.%m.%Y'],
                          widget=forms.TextInput(attrs={'size':15}))
      res_time           = forms.MultipleChoiceField(required=False, 
                          choices=get_periods_form_list(org_id),
                          widget=forms.CheckboxSelectMultiple() )
      date_start       = forms.DateField(required=False, input_formats=['%d.%m.%Y'],
                          widget=forms.TextInput(attrs={'size':20}))
      date_end         = forms.DateField(required=False, input_formats=['%d.%m.%Y'],
                          widget=forms.TextInput(attrs={'size':20}))
    data = { 'res_day': datetime.datetime.now().strftime('%d.%m.%Y'),}
    f = DmsItemForm(data)
    tab_cluster = {}
    my_title = "Gemeinsame Verwaltung von Ressourcen (Geräte, Räume, etc.)"
  
    tabs = [
            ( 'tab_reserve'   , [ 'res_day'   , 'res_time'], ), # eintägig
            ( 'tab_reserve_m' , [ 'date_start', 'date_end'], ), # mehrtägig
          ]
    content = get_tabbed_form(tabs, help_form, app_name, f)
    vars = get_folderish_vars_edit(request, item_container, app_name, my_title, content, f)
    vars['next'] = item_container.get_absolute_url() + "?step=2"
    vars['action_block'] = show_link(item_container.get_absolute_url() + '/show_my_events/', 
                                     _(u'eigene Reservierungen'))
    #'<a href="index.html?step=10">eigene Reservierungen</a>'
    vars['submit'] = "Reservierung von Ressourcen (1/2)"
    return render_to_response ( 'app/base_edit.html', vars )

  elif (step==2): # *Schritt 2*
    #clean_post=clean_data( request.POST.copy() )
    my_datetime_start, my_datetime_end, days = get_datetimes(org_id, clean_post)
    if (my_datetime_start!=0) and (my_datetime_end!=0):
      if mx.DateTime.Parser.DateTimeFromString(my_datetime_end) <= mx.DateTime.Parser.DateTimeFromString(my_datetime_start):
        vars = feedback_vars(request, item_container, app_name, _(u"Falsche Eingabe: Der Endzeitpunkt darf nicht vor dem Anfangszeitpunkt liegen."), 'days='+str(days))
        return render_to_response('app/resource/feedback.html', vars)
      if mx.DateTime.Parser.DateTimeFromString(my_datetime_start) < mx.DateTime.now():
        vars = feedback_vars(request, item_container, app_name, _(u"Falsche Eingabe: Der Anfangszeitpunkt darf nicht in der Vergangenheit liegen."), 'days='+str(days))
        return render_to_response('app/resource/feedback.html', vars)
    else:
      vars = feedback_vars(request, item_container, app_name, _(u"Die gemachten Zeitangaben sind unvollständig."), 'days='+str(days))
      return render_to_response('app/resource/feedback.html', vars)
      
    my_user_id = get_user(request.user.username).id
    
    t_form = get_template('app/resource/step2_content.html')
    this_section = {}
    form_objs = [] # Ressource
    section = ''
    objs      = [] # Typ / Kategorie
    my_types   = get_types_form_list(get_type_res_list(org_id, all=False))
    
    curr = 0
    missing_types = []
    for mytype in my_types:
      if section != mytype[1]:                         # Name der Kategorie
        if this_section != {}:
          this_section['forms'] = form_objs
          objs.append(this_section)
          this_section = {}
          curr += 1
          form_objs = []
        section = mytype[1]
        this_section['name'] = section
        this_section['tab']  = curr
        if curr == 0:
          this_section['selected'] = True
      free_resources, used_resources = get_free_resource_list(mytype[0], my_datetime_start, my_datetime_end)
      form_objs.append(get_form_tab_row(mytype[1], free_resources, 0))
      if len(free_resources)==0:
        missing_types += [mytype[1]]
    if this_section != {}:
      this_section['forms'] = form_objs
      objs.append(this_section)
    text_missing = ""
    if len(missing_types)>0:
      if len(missing_types)==len(my_types):
        vars = feedback_vars(request, item_container, app_name, _(u"Die gewünschten Ressourcen sind zu diesem Zeitpunkt alle belegt."), 'days=1')
        return render_to_response('app/resource/feedback.html', vars)
      else:
        text_missing = _(u"In folgenden Kategorien sind alle Ressourcen belegt: ")
        l_len = len(text_missing)
        for mt in missing_types:
          if len(text_missing)>l_len:
            text_missing += _(u', ')
          text_missing += mt
        # Info fuer Formular
    elif len(objs)==0:
      vars = feedback_vars(request, item_container, app_name, _(u"Es wurden noch keine Ressourcen definiert. Bitte wenden Sie sich an die/den Systemverwalter/in."), 'days=1')
      return render_to_response('app/resource/feedback.html', vars)
    d_context                   = {'objs'   : objs}
    d_context['next']           = item_container.get_absolute_url()
    d_context['submit']         = _(u"Reservierung vornehmen")
    d_context['datetime_start'] = my_datetime_start
    d_context['datetime_end']   = my_datetime_end
    d_context['user_id']        = my_user_id
    form_context = Context( d_context )
    #assert False
    vars = get_folderish_vars_show(request, item_container, app_name, t_form.render(form_context), 
                                  False)
    # Korrektur fuer get_folderish_vars_show (Notloesung) TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vars['show_errors'] = False # TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Korrektur fuer get_folderish_vars_show (Notloesung) TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if len(text_missing)>0:
      vars['text_intro'] = text_missing
    return render_to_response('app/resource/step2_form.html', vars)
  elif (step==3):                 # (step==3) : abspeichern
    # in Schleife über alle gewählten Ressourcen
    dt_start = convert_str_to_date(clean_post['datetime_start'])
    dt_end   = convert_str_to_date(clean_post['datetime_end'])
    for mytype, myres0 in clean_post.iteritems():
      if mytype[:5]=='type_':
        if type(myres0) == type([]):
          my_res = myres0
        else:
          my_res = [myres0]
        for item in my_res:
          append_event(str(item), dt_start, dt_end, clean_post['user_id'])
          
    vars = feedback_vars(request, item_container, app_name, _(u"Die gewünschten Ressourcen wurden reserviert."), '')
    return render_to_response('app/resource/feedback.html', vars)

# -----------------------------------------------------
#@vary_on_headers('Accept-Language')
def resource_show(request, item_container):
  """ Reservierung von Ressourcen (Schritte 1, 2, 3) """
  app_name   = 'resource'
  #org        = get_org_by_username(request.user.username)
  org_id = get_userfolder_org_id(item_container)
  is_periods = exist_settings_org_id(org_id) # sollte nicht mehr noetig sein
  get        = request.GET.copy()
  clean_post = clean_data( request.POST.copy() )
  if get.has_key('days'):
    days = int(get['days']) # mehrtägig
  else:
    days = 0                # eintägig
  if not ((get.has_key('step')) or (clean_post.has_key('step'))):
    return show_input_form(request, item_container, org_id, app_name, 1, clean_post)
  try:
    step = int(get['step'])
  except:
    step = int(clean_post['step'])
  return show_input_form(request, item_container, org_id, app_name, step, clean_post)
