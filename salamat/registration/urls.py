
from django.conf.urls import url
from django.contrib.auth import views as core_auth_views
from django.views.generic import TemplateView

from userena import views as userena_views
from userena import settings as userena_settings
from userena.compat import auth_views_compat_quirks, password_reset_uid_kwarg

from registration import views as auth_views


def merged_dict(dict_a, dict_b):
    """Merges two dicts and returns output. It's purpose is to ease use of
    ``auth_views_compat_quirks``
    """
    dict_a.update(dict_b)
    return dict_a

urlpatterns = [

    # Authentication

    url(r'^signin/$', auth_views.signin, name='userena_signin'),
    url(r'^signin/error/$',
        TemplateView.as_view(template_name='registration/signin_error.html'),
        name='auth_signin_error'),
    url(r'^signout/$', userena_views.signout, name='userena_signout'),

    # RESET PASSWORD

    url(r'^password/reset/$', core_auth_views.password_reset,
        merged_dict({'template_name': 'userena/password_reset_form.html',
                    'email_template_name': 'userena/emails/password_reset_message.txt',
                    'extra_context': {'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES}
                   }, auth_views_compat_quirks['userena_password_reset']), name='userena_password_reset'),

    url(r'^password/reset/done/$', core_auth_views.password_reset_done,
        {'template_name': 'userena/password_reset_done.html'},
        name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        core_auth_views.password_reset_confirm,
        {'template_name': 'userena/password_reset_confirm_form.html'},
        name='userena_password_reset_confirm'),

    url(r'^password/reset/confirm/complete/$',
        core_auth_views.password_reset_complete,
        {'template_name': 'userena/password_reset_complete.html'},
        name='password_reset_complete'),

    # SIGNUP

    url(r'^signup/$', auth_views.signup, name='userena_signup'),

    url(r'^(?P<username>[-\w]+)/signup/complete/$',
        userena_views.direct_to_user_template,
        {'template_name': 'userena/signup_complete.html',
        'extra_context': {
            'userena_activation_required':
            userena_settings.USERENA_ACTIVATION_REQUIRED,
            'userena_activation_days':
            userena_settings.USERENA_ACTIVATION_DAYS}},
        name='userena_signup_complete'),

    url(r'^activate/(?P<activation_key>\w+)/$', userena_views.activate, {
        'success_url': '/me/'}, name='userena_activate'),
    # Disabled account
    url(r'^(?P<username>[\@\.\+\w-]+)/disabled/$', userena_views.disabled_account,
        {'template_name': 'userena/disabled.html'}, name='userena_disabled'),
]
