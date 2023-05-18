#not safety, should modify PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator as token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from sharpeyes.settings import EMAIL_HOST_USER, SECRET_KEY
from social_django.models import UserSocialAuth
from datetime import datetime, timedelta, date
from base64 import urlsafe_b64encode
from calendar import monthrange


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/user_<username>/<filename>
    return 'users/user_{0}/{1}'.format(instance.username, filename)
   
 
def correct_email(email):
    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name.lower() + "@" + domain_part.lower()
    return email

  
def send_mail_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
      'user': user,
      'domain': current_site.domain,
      'uid': urlsafe_b64encode(force_bytes(user.pk)),
      #'token': token.make_token(user),
      'token': token._make_token_with_timestamp(user, token._num_seconds(token._now()), SECRET_KEY),
    }
    message = render_to_string('mainapp/email-verification.html', context = context)
    send_mail('SHARPEYES | Код подтверждения', message, EMAIL_HOST_USER, [user.email], fail_silently=False)
   

def send_mail_for_reset(request, user):
    current_site = get_current_site(request)
    context = {
      'domain': current_site.domain,
      'uid': urlsafe_b64encode(force_bytes(user.pk)),
      #'token': token.make_token(user),
      'token': token._make_token_with_timestamp(user, token._num_seconds(token._now()), SECRET_KEY),
    }
    message = render_to_string('mainapp/email-password-reset.html', context = context)
    send_mail('SHARPEYES | Восстановление доступа', message, EMAIL_HOST_USER, [user.email], fail_silently=False)
 

def get_date(req_month):
    if req_month:
        #request restriction
        cur_date = datetime.strptime(req_month, "%Y-%m").date()
        limit_date = date(2023, 1, 1)
        if cur_date > get_current_date() or cur_date < limit_date : return None
        year, month = (int(x) for x in req_month.split('-'))
        return datetime.strptime(f"{year}{month}1", '%Y%m%d').date()
    return datetime.today()


def get_current_date():
    return datetime.today().date()


def prev_month(d):
    #display limit
    if d.strftime('%Y-%m') == "2023-01": return None
    
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    #display limit
    if d.strftime('%Y-%m') == get_current_date().strftime('%Y-%m') :
        return None
    
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


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