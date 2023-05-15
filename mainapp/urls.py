from django.urls import path, include
from django.conf.urls import *

from .views import *

#'home'
#'about'
#'logout'
#'account/active/<uidb64>/<token>/'
#'account/reset/<uidb64>/<token>/'
#'social-auth/'
#'profile/'
#'diary/<slug:username>/'

urlpatterns = [
   path('', HomePage.as_view(), name='home'),
   path('profile/<slug:userslug>/', ProfilePage.as_view(), name='profilepage'),
   path('myprogress/<slug:userslug>/', ProgressPage.as_view(), name='progresspage'),
   path('diary/', MyDiary.as_view(), name='diarypage'),
   path('account/active/<uidb64>/<token>/', EmailVerify.as_view(), name='userverify'),
   path('account/reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='userpasswordreset'),
]
