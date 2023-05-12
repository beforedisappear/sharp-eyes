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
   path('profile/', ProfilePage.as_view(), name='profilepage'),
   path('myprogress/<slug:user>', ProgressPage.as_view(), name='progress'),
   path('diary/', MyDiary.as_view(), name='diary'),
]
