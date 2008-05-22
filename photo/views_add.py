# -*- coding: utf-8 -*-
"""
/dms/photo/views_add.py

.. enthaelt den View zum Ergaenzen eines Photos
         Django content Management System

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  29.10.2007  Beginn der Arbeit
"""

import string
import time
import PIL
import os

from django.utils.encoding  import smart_unicode
from django.http        import HttpResponse, HttpResponseRedirect
from django.shortcuts   import render_to_response
from django             import newforms as forms

from django.utils.translation import ugettext as _

from dms.models         import DmsItem

#from dms.roles          import *
from dms.views_error    import show_error_object_exist

from dms.utils          import get_tabbed_form
from dms.utils          import get_section_choices
from dms.utils          import check_name
from dms.utils          import get_license_choices
from dms.mail           import send_control_email
from dms.utils_form     import get_item_vars_add
from dms.file.utils     import save_file
from dms.image.utils      import get_image_size

from dms.views_error    import show_error_spam

from dms.queries        import save_item_values
from dms.queries        import get_random_question_answer
from dms.queries        import check_answer
from dms.queries        import get_user
from dms.queries        import exist_item
from dms.queries        import get_site_url

from dms.encode_decode  import decode_html
from dms.encode_decode  import encode_html_dir

from dms.photo.help_form  import help_form

from dms_ext.extension    import * # dms-Funktionen ueberschreiben

# -----------------------------------------------------.
def photo_add(request, item_container):
  """ neuen Gaestebucheintrag anlegen """
  question, answer = get_random_question_answer()
  my_user = get_user(request.user.username)
  if my_user != None:
    my_name = my_user.get_full_name()
    my_email = my_user.email
  else:
    my_name = ''
    my_email = ''

  def save_values(name, new, files, my_folder):
    """ Daten sichern """

    def getThumbnail ( filename, width, height, file_extension, width_priority = False ) :
      """ .. skaliert ein gegebenes Bild und speichert die Datei """
      my_path, my_filename = os.path.split ( filename )
      dot = my_filename.rfind('.')
      in_file = my_filename[:dot]
      in_type = my_filename[dot+1:]
      img = PIL.Image.open(filename)
      nWidth  = img.size[0]
      nHeight = img.size[1]
      if nWidth > width :
        nWFactor = 1.0 * nWidth / width
      else :
        nWFactor = 1
      if width_priority:
        nHFactor = nWFactor
        nFactor = nWFactor
      else:
        if nHeight > height:
          nHFactor = nHeight / height
        else:
          nHFactor = 1
        if nWFactor < nHFactor:
          nFactor = nHFactor
        else :
          nFactor = nWFactor
      img.thumbnail( ( nWidth / nFactor, nHeight / nFactor ) )
      thumb = my_path + '/' + in_file + '_' + file_extension + '.' + in_type
      img.save(thumb)
      return thumb

    file_name = save_file(name, files, my_folder)
    file_ext = file_name[file_name.rfind('.')+1:].lower()
    if file_ext in ['jpg', 'jpeg', 'gif', 'png']:
      # --- Siehe from dms.clipboard.get_photo_names
      file_name_small = getThumbnail ( file_name, 160, 420, 'small', width_priority = True )
      file_name_middle = getThumbnail ( file_name, 600, 600, 'middle' )
      width, height = get_image_size(file_name)
      new['integer_1'] = width
      new['integer_2'] = height
    save_item_values(request.user, 'dmsPhoto', name, new, my_folder,
                     not my_folder.item.is_moderated, True)
    send_control_email(item_container)

  class DmsItemForm(forms.Form):
    if my_user == None:
      anti_spam_question = forms.CharField(required=False,
                                widget=forms.HiddenInput(attrs={'value':question}) )
      anti_spam_answer   = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'size':20}) )
    string_1   = forms.CharField(required=False, max_length=60,
                      widget=forms.TextInput(attrs={'size':40}) )
    string_2   = forms.CharField(required=False, max_length=200,
                      widget=forms.TextInput(attrs={'size':60}) )
    fname      = forms.CharField(required=False, max_length=200,
                       widget=forms.FileInput(attrs={'size':40}) )
    title      = forms.CharField(max_length=60,
                       widget=forms.TextInput(attrs={'size':60}) )
    text       = forms.CharField(required=False, widget=forms.Textarea(
                                              attrs={'rows':15, 'cols':60, 'id':'ta', 
                                                    'style':'width:100%;'}) )
    section    = forms.CharField(widget=forms.Select(choices=
                       get_section_choices(item_container.container.sections),
                       attrs={'size':4, 'style':'width:40%'} ) )
    license    = forms.ChoiceField(choices=get_license_choices(item_container),
                       widget=forms.RadioSelect() )

  app_name = 'photo'
  my_title = _(u'Photo anlegen')
  # --- Sind Daten vorhanden oder muessen Sie initialiSiert werden?
  show_errors = ( request.method == 'POST' )
  if show_errors:
    data = request.POST.copy()
  else:
    data = { 'license': 1,}
    if my_user != None:
      data['string_1'] = my_user.get_full_name()
      data['string_2'] = my_user.email
  f = DmsItemForm(data)

  # --- Reihenfolge, Ueberschriften, Hilfetexte

  if request.method == 'POST' and not f.errors:
    #new = encode_html_dir(f.data)
    new = f.data
    if request.user.username == '':
      if new.has_key('anti_spam_question'):
        is_ok = check_answer(new['anti_spam_question'], new['anti_spam_answer'])
    else:
      is_ok = True
    if is_ok:
      name = check_name(request.FILES['fname']['filename'], True)
      if not exist_item(item_container, name):
        save_values(name, f.data, request.FILES, item_container)
        return HttpResponseRedirect(get_site_url(item_container, 'index.html'))
      else :
        return show_error_object_exist(request, item, name)
    else:
      return show_error_spam(request, item_container)
  else:
    if my_user == None:
      tabs = [ ('tab_base', [ 'string_1', 'string_2', 'fname', 'title', 'text', 'section',
                              'anti_spam_question', 'anti_spam_answer' ]),
               ( 'tab_license'   , [ 'license', ] ),
             ]
    else:
      tabs = [ ('tab_base', [ 'string_1', 'string_2', 'fname', 'title', 'text', 'section' ]), 
               ( 'tab_license'   , [ 'license', ] ),
             ]
    content = get_tabbed_form(tabs, help_form, app_name, f)
    if item_container.item.is_moderated:
      moderated_text = help_form['moderated_text']['info']
    else:
      moderated_text = ''
    vars = get_item_vars_add(request, item_container, app_name, my_title, content, show_errors)
    vars['moderated_text'] = moderated_text
    return render_to_response ( 'app/file/manage_edit.html', vars )
