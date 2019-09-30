
import random
# from django.utils.hashcompat import sha_constructor
from django.contrib.auth.models import User
from hashlib import sha1 as sha_constructor

def gen_username():
    """Generates a random username."""
    while True:
        username = 'user-%s' % sha_constructor(str(random.random())).\
                   hexdigest()[:9]
        if not User.objects.filter(username__iexact=username).exists():
            break
    return username
