from django.urls import path, include
from django.conf.urls import *

from .views import *

#'about'
#'social-auth/'

urlpatterns = [
   path('', HomePage.as_view(), name='home'),
   path('profile/<slug:userslug>/', ProfilePage.as_view(), name='profilepage'),
   path('myprogress/<slug:userslug>/', ProgressPage.as_view(), name='progresspage'),
   path('diary/', MyDiary.as_view(), name='diarypage'),
   path('logout/', logout_user, name='logout'),
   path('account/active/<uidb64>/<token>/', EmailVerify.as_view(), name='userverify'),
   path('account/reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='userpasswordreset'),
]
