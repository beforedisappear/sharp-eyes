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
#'progress/<slug:username>/'
#'diary/<slug:username>/'

urlpatterns = [
   path('diary/', MyDiary.as_view(), name='diary'),
]
