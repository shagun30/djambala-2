#-*-coding: utf-8 -*-
"""
/dms/form_system.py

.. enthaelt Modifikationen des Django-Formular-Systems
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.01.2007  Beginn der Dokumentation
0.02  13.09.2007  Adresse der Hilfeseiten
0.03  14.09.2007  Fehlerkorrektur fuer Hilfefenster
0.04  07.12.2007  Unicode-Fehler bei Fehlertexten behoben
                  autocomplete-Optionen
"""

import  string, re
from    settings import HELP_URL

from django.utils.encoding  import smart_unicode
from django.utils.safestring  import SafeData, mark_safe, SafeUnicode

from django.utils.translation import ugettext as _

from dms.encode_decode  import encode_html

# -----------------------------------------------------
class form_system :

  def encode(self, text):
    text = string.replace(text, '\n', ' ')
    text = string.replace(text, "'", '"')
    text = string.replace(text, '"', '&quot;')
    text = encode_html(text)
    return text

  def getJsHelp(self, rHelp, text, title, rAnchor):
    """ zeigt Hilfe in einem PopUp-Fenster an """
    if string.strip(text) == '':
      return ''
    text  = self.encode(text)
    title = _('Kurzhilfe: ') + self.encode(title)
    #url = 'JavaScript:showHelp(\'' + rHelp + '#' + rAnchor + '\');" '
    url = "JavaScript:showHelp('%s#%s');\" " % (rHelp, rAnchor)
    #url += 'class="overlay" \n'
    url += 'onMouseOver="return overlib('
    url += "'" + text + "'"
    url += ",CAPTION,'" + title + "',TEXTSIZE,2,CAPTIONSIZE,2,SNAPX,16,SNAPY,4," 
    url += 'ol_vpos=ABOVE,ol_fgcolor=\'#f0f0ff\',ol_width=400)" onMouseOut="nd();"'

    return '&nbsp;<a href="' + url + '>...?</a>\n'

  def modify_form ( self, rId, rForm, valign, max_cols, rError='' ) :
    """ """
    def convert_date(s):
      cStart = 'value="'
      nLen = len(cStart)
      nStart  = string.find(s, cStart)
      nEnd    = min(string.find(s, '"', nStart+nLen+1), string.find(s, ' ', nStart+nLen+1))
      n_end_2 = string.find(s, '"', nStart+nLen+1)
      d = s[nStart+nLen:nEnd]
      arr = string.splitfields(d, '-')
      if len(arr) == 3 :
        dGerman = u'%s.%s.%s' % (arr[2],arr[1],arr[0])
      else :
        dGerman = d
      return s[:nStart+nLen] + dGerman + s[n_end_2:] + """ <a href="javascript: void(0);"
   onclick="return getCalendar(document.form_input.id_""" + rId + """);"><img
   src="/dms_media/javascript/calendar/calendar.png" border="0" /></a>"""

    def convert_date_time(s):
      cStart = 'value="'
      nLen = len(cStart)
      nStart = string.find(s, cStart)
      nEnd   = string.find(s, '"', nStart+nLen+1)
      d = s[nStart+nLen:nEnd]
      a = string.splitfields(d, ' ')
      arr = string.splitfields(a[0], '-')
      if len(arr) == 3 :
        dGerman = u'%s.%s.%s' % (arr[2],arr[1],arr[0])
      else :
        dGerman = d
      dGerman += ' ' + a[1][:a[1].rfind(':')]  # Sekunden abschneiden
      return s[:nStart+nLen] + dGerman + s[nEnd:]

    myType = smart_unicode(type(rForm.field))
    nPos = string.rfind ( myType, '.' )
    myType = myType[nPos+1:-2]
    if rError:
      error = u''
      #t = type(rError)
      for err in smart_unicode(rError):
        error += mark_safe(err)
      form = u'%s<br /><span class="red"><b>%s</b></span>' % \
               (smart_unicode(rForm), smart_unicode(error))
    else :
      form = smart_unicode(rForm)
    # --- soll das Eingabeobjekt horizontal angezeigt werden?
    if not valign and string.find(form, '<ul>') >= 0:
      form = string.replace(form, '<ul>', '')
      form = string.replace(form, '</ul>', '')
      form = string.replace(form, '<li>', '')
      form = string.replace(form, '</li>', '')
    if string.find(form, 'type="hidden"') >= 0:
      v = 'value="'
      obj = re.search(v+'.*?"', form, re.S)
      form += ' ' + form[obj.start()+len(v):obj.end()-1]
      form = form.replace('&lt;br /&gt;', '<br />')
      form = form.replace('&lt;ul&gt;', '<ul>')
      form = form.replace('&lt;/ul&gt;', '</ul>')
      form = form.replace('&lt;li&gt;', '<li>')
      form = form.replace('&lt;/li&gt;', '</li>')
      form = form.replace('&amp;', '&')
    #if not myType in ['DateField', 'DateTimeField']:
    if not myType in ['DateField']:
      return form
    if myType == 'DateTimeField':
      return convert_date_time(form)
    return convert_date(form)

  def get_form ( self, rFormList, rFormDict, app_name, rForm,
                       tab_cluster, valign, max_cols, show_errors):
    """ """
    from django.template.loader import get_template
    from django.template import Context
    h = get_template('app/form_header.html')
    hm = get_template('app/form_header_multiple.html')
    i = get_template('app/form_input.html')
    im = get_template('app/form_input_multiple.html')
    inf = get_template('app/form_info.html')
    t = get_template('app/form_table_start.html')
    my_help_url = HELP_URL + app_name + '/'
    if show_errors:
      my_errors = rForm.errors
    else:
      my_errors = {}
    c = Context ( {} )
    ret = t.render(c)
    for my_id in rFormList:
      if tab_cluster.has_key(my_id):
        my_data = tab_cluster[my_id]
        my_info = my_data[0]['title']
        my_cols = my_data[0]['cols']
        my_rows = my_data[0]['rows']
        my_show_cols = my_data[0]['show_cols']
        if my_data[0].has_key('valign'):
          my_valign = my_data[0]['valign']
        else:
          my_valign = valign
        my_cells = my_data[1]
        c = Context ( {} )
        ret += t.render(c)
        if my_info != '':
          c = Context ( { 'cols': 1+len(my_cols), 'info': my_info} )
          ret += inf.render(c)
        if my_show_cols:
          c = Context ( { 'headers': my_cols, } )
          ret += hm.render(c)
        n_row = 0
        for row in my_rows:
          if my_show_cols:
            inputs = []
            for c in my_cols:
              cell_id = my_cells[n_row]
              if my_errors.has_key(cell_id):
                err_info = my_errors[cell_id][0]
                is_proxy = str(type(err_info)).find('<class') >=0
                if is_proxy:
                  err_info = u'Es trat ein unbekannter Fehler auf.'
                my_form = self.modify_form(cell_id, rForm[cell_id],
                                           my_valign, max_cols, err_info)
              else :
                my_form = self.modify_form(cell_id, rForm[cell_id], my_valign, max_cols)
              inputs.append(my_form)
              n_row += 1
            c = Context ( { 'title'   : row,
                            'label'   : cell_id,
                            'inputs'  : inputs,
                            'max_cols': max_cols,
                          } )
            ret += im.render(c)
          else:
            inputs = []
            for c in my_cols:
              cell_id = my_cells[n_row]
              if my_errors.has_key(cell_id):
                err_info = my_errors[cell_id][0]
                is_proxy = str(type(err_info)).find('<class') >=0
                if is_proxy:
                  err_info = u'Es trat ein unbekannter Fehler auf.'
                my_form = self.modify_form(cell_id, rForm[cell_id],
                                           my_valign, max_cols, err_info)
              else :
                my_form = self.modify_form(cell_id, rForm[cell_id], my_valign, max_cols)
              inputs.append(my_form)
              n_row += 1
            c = Context ( { 'title'   : row,
                            'label'   : cell_id,
                            'inputs'  : inputs,
                            'max_cols': max_cols,
                          } )
            ret += im.render(c)
      else:
        form = rFormDict[my_id]
        if form.has_key('valign'):
          valign = form['valign']
        if my_errors.has_key(my_id):
          my_form = self.modify_form(my_id, rForm[my_id], valign, max_cols, my_errors[my_id])
        else :
          my_form = self.modify_form(my_id, rForm[my_id], valign, max_cols)
        has_autocomplete = form.has_key('auto_complete')
        if has_autocomplete:
          try:
            max_length = rForm[my_id].form[my_id].field.max_length
          except:
            max_length = 40
          if max_length > 50:
            max_length = 50
        else:
          max_length = -1
        c = Context ( { 'title'   : form['title'],
                        'label'   : my_id,
                        'input'   : my_form,
                        'help'    : self.getJsHelp(my_help_url, form['help'], 
                                                   form['title'], my_id),
                        'max_cols': max_cols,
                        'has_autocomplete': has_autocomplete,
                        'max_length': max_length,
                      } )
        ret += i.render(c)
    ret += '</table>\n'
    return ret
