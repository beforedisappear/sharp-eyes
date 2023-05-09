from social_core.exceptions import AuthAlreadyAssociated, AuthException, AuthForbidden
from social_django.models import UserSocialAuth


def custom_associate_by_email(backend, details, user=None, *args, **kwargs):
  if user:
    return None

  if backend.name == "telegram":
    email = details.get('username')
  else:
    email = details.get('email')
      
  if email:
    users = list(backend.strategy.storage.user.get_users_by_email(email))
    if len(users) == 0:
      return None
    elif len(users) > 1:
      raise AuthException(
        backend,
        'The given email address is associated with another account'
      )
    else:
      return {'user': users[0],
        'is_new': False}

def email_preparation(backend, user, response, *args, **kwargs):
  if backend.name == "telegram":
    response['email'] = response['id']
    del response['id']
    kwargs['details']['email'] = response['email']
    

def get_social_media(user):
    try:
        telegram_login = user.social_auth.get(provider='telegram')
    except UserSocialAuth.DoesNotExist:
        telegram_login = None
        
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None
            
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
        
    auth_context = {'google': google_login, "tg": telegram_login, 'can_disconnect': can_disconnect, }
    return auth_context