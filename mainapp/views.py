from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied, BadRequest
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator as gtoken
from django.views.generic.edit import FormMixin, FormView
from django.core.validators import validate_email

from .models import *
from .forms import *
from .dairy_calendar import Calendar
from .utils import get_date, prev_month, next_month, send_mail_for_verify, send_mail_for_reset, get_social_media, send_mail_for_changing_email
from datetime import datetime
from base64 import urlsafe_b64decode


class HomePage(FormMixin, TemplateView):
   template_name = "mainapp/index.html"
   form_class = UserAuthentication
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      return context

   def post(self, request):
      
      #authorization
      if len(request.POST) == 3:
         self.form = self.get_form()
         if self.form.is_valid():
            fv = self.form.cleaned_data
            user = authenticate(username=fv["username"], password=fv["password"])
            if user is not None:  #and user.email_verify == True:
               login(request, user)
               #return JsonResponse(data={}, status=201)
               return HttpResponseRedirect(ProfilePage.get_success_url(self))
            else:
               #return JsonResponse(data={'errors':{'email': 'Аккаунт не активен!'}}, status=400)
               return HttpResponse('incorrect email adress or password')
         else:
            #return JsonResponse(data={'errors': self.form.errors, }, status=400)
            return HttpResponse('invalid form')
        
      #registration
      elif len(request.POST) == 5:
         self.form_class = UserRegistration
         self.form = self.get_form()
         if self.form.is_valid():
            self.object = self.form.save()
            mail = self.form.cleaned_data.get('email')
            self.object.email = mail.lower()
            self.object.save()
            send_mail_for_verify(request, self.object)
            #return JsonResponse(data={}, status=201)
            return HttpResponse('the letter has been sent to your email')
            
         else:
            #return JsonResponse(data={'errors': self.form.errors,}, status=400)
            return HttpResponse('invalid form')
           
      #restoring account access
      elif len(request.POST) == 2:
         self.form_class = PasswordResetForm
         self.form = self.get_form()
         if self.form.is_valid():
            data = self.form.cleaned_data.get('email').lower()
            try:
               user = MyUser.objects.get(email = data)
               send_mail_for_reset(request, user)
               #return JsonResponse(data={}, status=201)
               return HttpResponse('the letter has been sent to your email')
            except:
               #return JsonResponse(data={'errors': {'email': 'Аккаунт не найден!'}}, status=400)
               return HttpResponse('the user with this email address does not exist')
         else:
            #return JsonResponse(data={'errors': {'email': 'Некорректный email адрес!'}}, status=400)
            return HttpResponse('invalid form')
            
      else:
         return HttpResponse('error!')


class LandingPage(TemplateView):
   template_name = "mainapp/about.html"


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
      thisuser = self.request.user
      context["thisuser"] = thisuser
      context["title"] = "SHARP EYES | Личный кабинет"
      context['social'] = get_social_media(thisuser)
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
         form.save()
         send_mail_for_changing_email(self.request, self.request.user, form.cleaned_data.get('emailfield'))
         #return HttpResponseRedirect(self.get_success_url())
         #return JsonResponse(data={}, status=201)          
         return HttpResponse("Мы отправили письмо для подтверждения нового адреса")
      else:
         err = form.errors
         #return JsonResponse(data={'errors': err, }, status=400)
         form = UserChangeCustom()
         return HttpResponse(err.values())
      

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
         user.is_active = True
         user.save()
         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
     
     
#PasswordResetConfirmView overriding
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
         # If the token is valid, display the password reset form.
         if token == self.reset_url_token:
            session_token = self.request.session.get("_password_reset_token")
            if gtoken.check_token(self.user, session_token):
               self.validlink = True
               return super().dispatch(*args, **kwargs) # get and post request

         #token validation and redirect to new url (w/o token) 
         else:
            if gtoken.check_token(self.user, token):
               self.request.session["_password_reset_token"] = token
               redirect_url = self.request.path.replace(token, self.reset_url_token)
               return HttpResponseRedirect(redirect_url) #get request
        
      return HttpResponse('the link is invalid')
    
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
      del self.request.session["_password_reset_token"]
      login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
      return super().form_valid(form)
   
   
class EmailChanging(TemplateView):

   def get(self, request, uidb64, token, newemail):
      user = self.get_user(uidb64)
      if user is not None and gtoken.check_token(user, token):
         try:
            email_address = urlsafe_b64decode(newemail[1::]).decode()
            validate_email(email_address)
            user.email = email_address
            user.save()
            return redirect('home')
         except:
            raise BadRequest
            
      else:
         return HttpResponse('the link is invalid')
    
   def get_user(self, uidb64):
      try:
         uid = urlsafe_b64decode(uidb64[1::]).decode()
         user = MyUser.objects.get(pk = uid)
      except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
         user = None
      return user