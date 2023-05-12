from typing import Any, Optional
from django.db import models
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView, CreateView
from django.contrib.auth import login, logout, authenticate, get_user_model

from .models import *
from .forms import *
from .dairy_calendar import Calendar
from .utils import get_date, prev_month, next_month
from datetime import datetime

from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView


class HomePage(TemplateView):
   template_name = "mainapp/index.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      return context
   
   def post(self, request):
      return HttpResponse('correct')


class ProfilePage(DetailView):
   template_name = "mainapp/profilepage.html"
   model = get_user_model()
   

#CreateView + UpdateView, get_object overriding
class ProgressPage(UpdateView):
   template_name = "mainapp/progress.html"
   model = DayProgress
   slug_field = "user__userslug"
   slug_url_kwarg = "user"
   form_class = ProgressFilling
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      return context
   
   def get(self, request, *args, **kwargs):
      user = get_object_or_404(MyUser, userslug = kwargs['user'])
      if user is not None and user == request.user:
         return super(ProgressPage, self).get(request, *args, **kwargs)
      else:
         raise PermissionDenied #redirect to login page
   
   def post(self, request, user):
      form = self.get_form()
      if form.is_valid():
         return self.form_valid(form)
      else:
         return self.form_invalid(form)
      
   def form_valid(self, form):
      #form.instance.user = self.request.user
      #progress = DayProgress.objects.get(user=self.request.user)
      # progress.sharpness_vision = form['sharpness_vision'].value()
      # progress.colorness_vision = form['colorness_vision'].value()
      # progress.peripheral_vision = form['peripheral_vision'].value()
      # progress.binocular_vision = form['binocular_vision'].value()
      # progress.additional_info = form['additional_info'].value()
      # progress.save()
      #return HttpResponseRedirect(self.get_success_url())
      obj = DayProgress.objects.get(user=self.request.user)
      obj.delete()
      form.instance.user = self.request.user
      return super(ProgressPage, self).form_valid(form)
      
   def get_success_url(self, **kwargs):
      return reverse_lazy("progress", kwargs={'user': self.request.user.userslug})
   
   def get_object(self, queryset=None):
      obj = DayProgress.objects.filter(user=self.request.user, current_date=datetime.today().date())
      if not obj.exists():
         new_obj = DayProgress.objects.create(user=self.request.user)
         return obj
      else:
         return obj.first()



class MyDiary(ListView):
   model = DayProgress
   template_name = "mainapp/diary.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      d = get_date(self.request.GET.get('month', None))
      if d is None:
         raise Http404
      cal = Calendar(d.year, d.month, self.get_queryset())
      context['calendar'] = cal.formatmonth(withyear=True)
      context['prev_month'] = prev_month(d)
      context['next_month'] = next_month(d)
      return context
   
   def get_queryset(self):
      return DayProgress.objects.filter(user=self.request.user)
