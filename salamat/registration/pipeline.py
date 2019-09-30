
from social_auth.backends.pipeline import user as user_pipeline
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.contrib.vk import VKOAuth2Backend
from userena.managers import ASSIGNED_PERMISSIONS
from guardian.shortcuts import assign

from facebook import api as fb_api
from vkontakte import api as vk_api
from users import tasks as user_tasks


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    result = user_pipeline.create_user(backend, details, response, uid,
                                       username, user, *args, **kwargs)
    if result:
        user = result.get('user')
        isnew = result.get('is_new', False)
        if user and isnew:
            # Give permissions to view and change itself.
            for perm in ASSIGNED_PERMISSIONS['user']:
                assign(perm[0], user, user)
    return result


def update_user_details(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    result = user_pipeline.update_user_details(backend, details, response,
                                               user, is_new, *args, **kwargs)
    if response and isinstance(backend, FacebookBackend):
        access_token = response.get('access_token')

        if access_token:
            # Get facebook friends.

            def got_friends(data):
                if data and 'data' in data:
                    friend_ids = [friend['id'] for friend in data['data']]
                    if friend_ids:
                        # Send task to celery.
                        user_tasks.find_friends_from_social.delay(
                            user.pk, friend_ids, backend.name)
            fb_api.friends(access_token, done=got_friends)
            user.profile.fb = dict(response)  # Save fb info in profile.
            user.profile.save()

    if response and isinstance(backend, VKOAuth2Backend):
        access_token = response.get('access_token')
        if access_token:
            def got_user_data(data):
                if data and 'response' in data:
                    user.profile.vk = dict(data['response'][0])
                    user.profile.vk.update(dict(access_token=access_token))
                    user.profile.save()

            def got_friends(data):
                if data and 'response' in data:
                    friend_ids = data['response']
                    if friend_ids:
                        # Send task to celery.
                        user_tasks.find_friends_from_social.delay(
                            user.pk, friend_ids, backend.name)

            uid = response.get('uid')
            if uid:
                vk_api.get_users_photo(access_token, uid, done=got_user_data)
                vk_api.friends(uid, done=got_friends)

    return result
