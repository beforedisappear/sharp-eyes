from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, UpdateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.core.validators import validate_email
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .utils import next_month, send_mail_for_verify, send_mail_for_reset, err_list
from .utils import get_date, prev_month, get_social_media, messages, jsn_cfg
from .utils import default_token_generator as gtoken
from .dairy_calendar import Calendar
from datetime import datetime
from base64 import urlsafe_b64decode


class HomePage(TemplateView):
   template_name = "mainapp/index.html"
   
   def get(self, request, *args, **kwargs):
      try:
         kwargs["message"] = self.request.session.get('data')
         del self.request.session['data']
      except:
         pass
      return super().get(request, *args, **kwargs)
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = "SHARP EYES | Главная страница"
      return context

   def post(self, request):
      #authorization
      if len(request.POST) == 3:
         form = UserAuthentication(None, data=request.POST)
         if form.is_valid():
            fv = form.cleaned_data
            user = authenticate(username=fv["username"], password=fv["password"])
            if user is not None:
               login(request, user)
               return JsonResponse(data={"success": user.get_absolute_url()}, status=201)
            else:
               return JsonResponse(data={"errors": messages["email"]}, status=400, json_dumps_params=jsn_cfg)
         else:
            errors = err_list(form.errors)
            return JsonResponse(data={"errors": errors }, status=400, json_dumps_params=jsn_cfg)
        
      #registration
      elif len(request.POST) == 5:
         self.form = UserRegistration(request.POST)
         if self.form.is_valid():
            self.object = self.form.save()
            send_mail_for_verify(request, self.object)
            return JsonResponse(data={"success": messages["reg"]}, status=201, json_dumps_params=jsn_cfg)
         
         else:
            errors = err_list(self.form.errors)
            return JsonResponse(data={"errors": errors}, status=400, json_dumps_params=jsn_cfg)
           
      #restoring account access
      elif len(request.POST) == 2:
         self.form = UserPasswordReset(request.POST)
         if self.form.is_valid():
            data = self.form.cleaned_data.get('email')
            try:
               user = MyUser.objects.get(email = data, is_active = True)
               send_mail_for_reset(request, user)
               return JsonResponse(data={"success": messages["res"]}, status=201, json_dumps_params=jsn_cfg) 
            
            except:
               return JsonResponse(data={"errors": messages["act"]}, status=400, json_dumps_params=jsn_cfg)
         else:
            errors = err_list(self.form.errors)
            return JsonResponse(data={"errors": errors}, status=400, json_dumps_params=jsn_cfg)
                       
      else:
         return JsonResponse(data={"errors": messages["err"] }, status=400, json_dumps_params=jsn_cfg)


class LandingPage(TemplateView):
   template_name = "mainapp/about.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = "SHARP EYES | О проекте"
      return context

class LoginPage(TemplateView):
   template_name = "mainapp/login.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = "SHARP EYES | Авторизация"
      return context
   
class RegisterPage(TemplateView):
   template_name = "mainapp/register.html"
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = "SHARP EYES | Регистрация"
      return context

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
      context["title"] = "SHARP EYES | Личный кабинет"
      context["social"] = get_social_media(self.request.user)
      context["tasks"] = Task.objects.all()
      context["instructions"] = Instruction.objects.all()
      context["surveys"] = Survey.objects.all()
      return context
      
   def get(self, request, *args, **kwargs):
      user = get_object_or_404(MyUser, userslug = kwargs['userslug'])
      if user is not None and user == request.user:
         return super(ProfilePage, self).get(request, *args, **kwargs)
      else:
         raise PermissionDenied
     
   def post(self, request, *args, **kwargs):
      if request.method == "POST" and len(request.POST) == 1:
         send_mail_for_reset(request, request.user)
         return JsonResponse(data={"success": messages["res"]}, status=201, json_dumps_params=jsn_cfg)
      
      else:
      
         form = UserChangeCustom(request.POST, request.FILES, instance=request.user)
      
         if form.is_valid():
            form.save()
            email = form.data['emailfield'].lower()
            if email != request.user.email:
               send_mail_for_changing_email(self.request, self.request.user, email)
               return JsonResponse(data={"success": messages["upd-em"]}, status=201, json_dumps_params=jsn_cfg)
         
            return JsonResponse(data={"success": messages["upd"]}, status=201, json_dumps_params=jsn_cfg)
      
         else:
            errors = [{k : v[0]} for k, v in form.errors.items()]
            form = UserChangeCustom()
            return JsonResponse(data={"errors": errors}, status=400, json_dumps_params=jsn_cfg)
      
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
         raise PermissionDenied
   
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
      return JsonResponse(data={"success": messages["svd"]}, status=201, json_dumps_params=jsn_cfg)
      
      # return HttpResponseRedirect(progress.get_absolute_url())
      # obj = DayProgress.objects.get(user=self.request.user, current_date=datetime.today().date())
      # obj.delete()
      # form.instance.user = self.request.user
      # return super(ProgressPage, self).form_valid(form)
      
   def form_invalid(self, form):
      self.object = self.get_object()
      return JsonResponse(data={"errors": messages["err"]}, status=400, json_dumps_params=jsn_cfg)
   
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
   
   @method_decorator(login_required(login_url='/'), name="dispatch")
   def dispatch(self, *args, **kwargs):
        return super(MyDiary, self).dispatch(*args, **kwargs)
     
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = "SHARP EYES | Дневник самоконтроля"
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

   @method_decorator(sensitive_post_parameters())
   @method_decorator(never_cache)
   def get(self, request, uidb64, token):
      user = self.get_user(uidb64)
      if user is not None and gtoken.check_token(user, token):
         user.is_active = True
         user.save()
         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
         data = { "success": {"mes": messages["scs"]} }
         self.request.session['data'] = data
         return redirect('home')
      else:
         raise BadRequest
    
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
   
   @method_decorator(sensitive_post_parameters())
   @method_decorator(never_cache)
   def dispatch(self, *args, **kwargs):
      if "uidb64" not in kwargs or "token" not in kwargs:
         raise BadRequest
            
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

      data = {"errors": {"mes": messages["lnk"] }}
      self.request.session['data'] = data
      return redirect('home')
    
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
      data = { "success": {"mes": messages["scs2"]} }
      self.request.session["data"] = data
      return super().form_valid(form)
   
class EmailChanging(TemplateView):

   @method_decorator(sensitive_post_parameters())
   @method_decorator(never_cache)
   def get(self, request, uidb64, token, newemail):
      user = self.get_user(uidb64)
      if user is not None and gtoken.check_token(user, token):
         try:
            email_address = urlsafe_b64decode(newemail[1::]).decode()
            validate_email(email_address)
            user.email = email_address
            user.save()
            data = { "success": {"mes": messages["scs1"]} }
            self.request.session["data"] = data
            return redirect('home')
         except:
            raise BadRequest
            
      else:
         data = { "errors": {"mes": messages["lnk"]} }
         self.request.session["data"] = data
         return redirect('home')
    
   def get_user(self, uidb64):
      try:
         uid = urlsafe_b64decode(uidb64[1::]).decode()
         user = MyUser.objects.get(pk = uid)
      except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
         user = None
      return user