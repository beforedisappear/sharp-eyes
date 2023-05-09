from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.contrib.auth import login, logout, authenticate, get_user_model

from .models import *
from .dairy_calendar import Calendar
from .utils import get_date

class MyDiary(ListView):
   model = DayProgress
   template_name = 'mainapp/diary.html'
   context_object_name = "dates"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
      d = get_date(self.request.GET.get('day', None))
      cal = Calendar(d.year, d.month, self.request.user)
      context['calendar'] = cal.formatmonth(withyear=True)
      
      return context
   
   def get_queryset(self, **kwargs):
      return DayProgress.objects.filter(user = self.request.user).order_by("current_date") #.values()
