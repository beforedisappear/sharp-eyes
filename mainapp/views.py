from typing import Any, Dict, Optional
from django.db import models
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, TemplateView, UpdateView, CreateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator as gtoken
from django.views.generic.edit import FormMixin, FormView

from .models import *
from .forms import *
from .dairy_calendar import Calendar
from .utils import get_date, prev_month, next_month, send_mail_for_reset
from datetime import datetime
from base64 import urlsafe_b64decode



class HomePage(TemplateView):
   template_name = "mainapp/index.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      return context
   
   def post(self, request):
      return HttpResponse('correct')


class ProfilePage(UpdateView):
   template_name = "mainapp/profilepage.html"
   model = get_user_model()
   #The name of the field on the model that contains the slug.22
   slug_field = "userslug"
   #The name of the URLConf keyword argument that contains the slug. 
   slug_url_kwarg = "userslug"
   form_class = UserChangeCustom
   
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["thisuser"] = self.request.user
      context["title"] = "SHARP EYES | Личный кабинет"
      return context
      
   def get(self, request, *args, **kwargs):
      user = get_object_or_404(MyUser, userslug = kwargs['userslug'])
      if user is not None and user == request.user:
         return super(ProfilePage, self).get(request, *args, **kwargs)
      else:
         raise PermissionDenied #redirect to login page
   
   def get_success_url(self, **kwargs):
      return reverse_lazy("profilepage", kwargs={'userslug': self.request.user.userslug})
     
   def post(self, request, *args, **kwargs):
      if len(request.POST) == 1:
         send_mail_for_reset(request, request.user)
         return HttpResponseRedirect(self.get_success_url())
      
      form = UserChangeCustom(request.POST, request.FILES, instance=request.user)
      
      if form.is_valid():
         #username = form.cleaned_data.get('username')
         #return JsonResponse(data={}, status=201) 
         form.save()
         return HttpResponseRedirect(self.get_success_url())         
      else:
         #err = form.errors
         #return JsonResponse(data={'errors': err, }, status=400)
         form = UserChangeCustom()
         return HttpResponse('incorrect')
         

#CreateView + UpdateView, get_object overriding
class ProgressPage(UpdateView):
   template_name = "mainapp/progress.html"
   model = DayProgress
   slug_field = "user__userslug"
   slug_url_kwarg = "userslug"
   form_class = ProgressFilling
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = "SHARP EYES | Мой прогресс"
      return context
   
   def get(self, request, *args, **kwargs):
      user = get_object_or_404(MyUser, userslug = kwargs['userslug'])
      if user is not None and user == request.user:
         return super(ProgressPage, self).get(request, *args, **kwargs)
      else:
         raise PermissionDenied #redirect to login page
   
   def post(self, request, userslug):
      form = self.get_form()
      if form.is_valid():
         return self.form_valid(form)
      else:
         return self.form_invalid(form)
      
   def form_valid(self, form):
      form_values = form.cleaned_data
      progress = DayProgress.objects.get(user=self.request.user, current_date=datetime.today().date())
      progress.sharpness_vision = form_values['sharpness_vision']
      progress.colorness_vision = form_values['colorness_vision']
      progress.peripheral_vision = form_values['peripheral_vision']
      progress.binocular_vision = form_values['binocular_vision']
      progress.additional_info = form_values['additional_info']
      progress.save()
      return HttpResponseRedirect(self.get_success_url())
      
      # obj = DayProgress.objects.get(user=self.request.user, current_date=datetime.today().date())
      # obj.delete()
      # form.instance.user = self.request.user
      # return super(ProgressPage, self).form_valid(form)
      
   def form_invalid(self, form):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form))

   def get_success_url(self, **kwargs):
      return reverse_lazy("progresspage", kwargs={'userslug': self.request.user.userslug})
   
   def get_object(self, queryset=None):
      try:
         obj = DayProgress.objects.get(user=self.request.user, current_date=datetime.today().date())
      except:
         return DayProgress.objects.create(user=self.request.user)
      else:
         return obj


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


def logout_user(request):
   logout(request)
   return redirect('/')

class EmailVerify(LoginView):

   def get(self, request, uidb64, token):
      user = self.get_user(uidb64)
      if user is not None and gtoken.check_token(user, token):
         #user.email_verify = True
         #user.save()
         #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
         return redirect('home')
      else:
         return HttpResponse('error registration')
    
   def get_user(self, uidb64):
      try:
         uid = urlsafe_b64decode(uidb64[1::]).decode()
         user = MyUser.objects.get(pk = uid)
      except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
         user = None
      return user
     
     
     
INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

class PasswordResetConfirm(FormView):
   form_class = UserPasswordSet
   success_url = reverse_lazy("home")
   template_name = "mainapp/password_reset_confirm.html"
   reset_url_token = "set-password"
    
   def dispatch(self, *args, **kwargs):
      self.validlink = False
      self.user = self.get_user(kwargs['uidb64'])
        
      if self.user is not None:
         token = kwargs["token"]
         if token == self.reset_url_token:
            session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
            if gtoken.check_token(self.user, session_token):
               self.validlink = True
               return super().dispatch(*args, **kwargs)
            
         else:
            if gtoken.check_token(self.user, token):
               self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
               redirect_url = self.request.path.replace(token, self.reset_url_token)
               return HttpResponseRedirect(redirect_url)    
        
      return HttpResponse('reset error')
    
   def get_user(self, uidb64):
      try:
         uid = urlsafe_b64decode(uidb64[1::]).decode()   
         user = MyUser.objects.get(pk = uid)
      except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
         user = None
      return user
    
   def get_form_kwargs(self):
      kwargs = super().get_form_kwargs()
      kwargs['user'] = self.user 
      return kwargs
    
   def form_valid(self, form):
      user = form.save()
      del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
      login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
      return super().form_valid(form)