from social_core.exceptions import AuthAlreadyAssociated, AuthException, AuthForbidden
from social_django.models import UserSocialAuth
from django.shortcuts import redirect


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
    
    
#overriding   
def user_details(strategy, details, backend, user=None, *args, **kwargs):
  """Update user details using data from provider."""
  if not user:
    return
    
  if backend.name == "telegram":
    user.is_active = True

  changed = False  # flag to track changes

  # Default protected user fields (username, id, pk and email) can be ignored
  # by setting the SOCIAL_AUTH_NO_DEFAULT_PROTECTED_USER_FIELDS to True
  if strategy.setting('NO_DEFAULT_PROTECTED_USER_FIELDS') is True:
    protected = ()
  else:
    protected = ('username', 'id', 'pk', 'email', 'password',
                 'is_active', 'is_staff', 'is_superuser',)

  protected = protected + tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

  # Update user model attributes with the new data sent by the current
  # provider. Update on some attributes is disabled by default, for
  # example username and id fields. It's also possible to disable update
  # on fields defined in SOCIAL_AUTH_PROTECTED_USER_FIELDS.
  field_mapping = strategy.setting('USER_FIELD_MAPPING', {}, backend)
  for name, value in details.items():
    # Convert to existing user field if mapping exists
    name = field_mapping.get(name, name)
    if value is None or not hasattr(user, name) or name in protected:
      continue

    current_value = getattr(user, name, None)
    if current_value == value:
      continue

    immutable_fields = tuple(strategy.setting('IMMUTABLE_USER_FIELDS', []))
    if name in immutable_fields and current_value:
      continue

    changed = True
    setattr(user, name, value)

  if changed:
    strategy.storage.user.changed(user)
    

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
  
  
def stay(strategy, entries, *args, **kwargs):
  return redirect(kwargs['user'].get_absolute_url())