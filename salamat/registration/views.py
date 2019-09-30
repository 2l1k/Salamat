
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from userena import views as userena_views
from registration.forms import AuthenticationForm, SignupForm


def signin(request):
    is_account_form = True
    if 'cancel' in request.POST:
        return HttpResponsePermanentRedirect('/')
    return userena_views.signin(request, auth_form=AuthenticationForm,
                                extra_context={
                                    'is_account_form': is_account_form
                                })


def signup(request):
    is_account_form =True
    if 'cancel' in request.POST:
        return HttpResponsePermanentRedirect('/')
    return userena_views.signup(request, signup_form=SignupForm,
                                extra_context={
                                    'is_account_form': is_account_form
                                })
