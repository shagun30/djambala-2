from django import oldforms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext as _

from dms.auth.decorators import login_required
from dms.auth import LOGIN_URL, REDIRECT_FIELD_NAME

from dms.auth.forms     import AuthenticationForm
from dms.auth.forms     import PasswordResetForm, PasswordChangeForm
from dms.views          import get_my_item_container
from dms.utils          import get_navigation_left
from dms.utils          import encode_email

def login(request, template_name='registration/login.html'):
    "Displays the login form and handles the login action."
    manipulator = AuthenticationForm(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.POST:
        try:
          org_id = request.POST['org_id']
        except:
          org_id = 0
        errors = manipulator.get_validation_errors(request.POST)
        if not errors:
            # Light security check -- make sure redirect_to isn't garbage.
            #if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
            if not redirect_to or ' ' in redirect_to:
                redirect_to = '/accounts/profile/'
            from dms.auth import login
            login(request, manipulator.get_user())
            request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        errors = {}
        try:
          org_id = request.GET['org_id']
        except:
          org_id = 0
    request.session.set_test_cookie()
    item_container = get_my_item_container(request, 'login')
    return render_to_response(template_name, {
        'form': oldforms.FormWrapper(manipulator, request.POST, errors),
        REDIRECT_FIELD_NAME: redirect_to,
        #'site_name': Site.objects.get_current().name,
        'site': item_container.container.site,
        'no_top_main_navigation': True,
        'navigation_left': get_navigation_left(item_container),
        'footer_email': encode_email(item_container.owner.email,
                               item_container.owner.get_full_name(), 'nav'),
        'last_modified': item_container.last_modified.strftime('%d.%m.%Y %H:%M'),
        'org_id': org_id
    }, context_instance=RequestContext(request))

def logout(request, next_page=None, template_name='registration/logged_out.html'):
    "Logs out the user and displays 'You are logged out' message."
    from dms.auth import logout
    logout(request)
    if next_page is None:
        return render_to_response(template_name, {'title': _(u'Logged out')},
                      context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def logout_then_login(request, login_url=LOGIN_URL):
    "Logs out the user if he is logged in. Then redirects to the log-in page."
    return logout(request, login_url)

def redirect_to_login(next, login_url=LOGIN_URL):
    "Redirects the user to the login page, passing the given 'next' page"
    return HttpResponseRedirect(u'%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, next))

def password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html'):
    new_data, errors = {}, {}
    form = PasswordResetForm()
    if request.POST:
        new_data = request.POST.copy()
        errors = form.get_validation_errors(new_data)
        if not errors:
            if is_admin_site:
                form.save(domain_override=request.META['HTTP_HOST'])
            else:
                form.save(email_template_name=email_template_name)
            return HttpResponseRedirect(u'%sdone/' % request.path)
    return render_to_response(template_name, {'form': oldforms.FormWrapper(form, new_data, errors)},
        context_instance=RequestContext(request))

def password_reset_done(request, template_name='registration/password_reset_done.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def password_change(request, template_name='registration/password_change_form.html'):
    new_data, errors = {}, {}
    form = PasswordChangeForm(request.user)
    if request.POST:
      new_data = request.POST.copy()
      next = new_data['next']
      errors = form.get_validation_errors(new_data)
      if not errors:
        form.save(new_data)
        return HttpResponseRedirect(next)
    else:
      data = request.GET.copy()
      next = data['next']
    item_container = get_my_item_container(request, 'password_change')
    return render_to_response(template_name, {'form': oldforms.FormWrapper(form, new_data, errors),
        'site': item_container.container.site,
        'navigation_left': get_navigation_left(item_container.container),
        'footer_email': encode_email(item_container.owner.email, item_container.owner.get_full_name(), 'nav'),
        'last_modified': item_container.last_modified.strftime('%d.%m.%Y %H:%M'),
        'errors': errors,
        'next': next})

def password_change_done(request, template_name='registration/password_change_done.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))
