from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from .models import *
from .utils import correct_email
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm

    
class ProgressFilling(forms.ModelForm):

   def __init__(self, *args, **kwargs):
      super(ProgressFilling, self).__init__(*args, **kwargs)
      instance = getattr(self, 'instance', 'None')
      if instance and instance.sharpness_vision:
         self.fields['sharpness_vision'].widget.attrs['readonly'] = True
      if instance and instance.colorness_vision:
         self.fields['colorness_vision'].widget.attrs['readonly'] = True
      if instance and instance.peripheral_vision:
         self.fields['peripheral_vision'].widget.attrs['readonly'] = True
      if instance and instance.binocular_vision:
         self.fields['binocular_vision'].widget.attrs['readonly'] = True

         
   # def clean(self):
   #    data = self.cleaned_data
   #    for key, field in self.fields.items():
   #       if data[key] is not None:
   #          print(self.fields[key])
   #    return data     
         
   class Meta:
      model = DayProgress
      fields = ['sharpness_vision', 'colorness_vision', 'peripheral_vision', 'binocular_vision', 'additional_info']
      
      
class UserChangeCustom(forms.ModelForm):
   emailfield = forms.EmailField(label="Адрес почты")
   
   def __init__(self, *args, **kwargs):
      super(UserChangeCustom, self).__init__(*args, **kwargs)
      self.fields["sex"].choices = [("", ""),] + list(self.fields["sex"].choices)[1:]
      try:
         self.fields["emailfield"].initial = kwargs['instance']
      except:
         self.fields["emailfield"].initial = ""
         

   def clean(self):
      cleaned_data = super().clean()
      email = cleaned_data['emailfield']
      if MyUser.objects.filter(email=correct_email(email)).exclude(email=self.instance.email).exists():
         raise ValidationError("Пользователь с таким email уже зарегистрирован")
      else:
         return cleaned_data
   
   class Meta:
      model = get_user_model()
      fields = ('userpic','emailfield', 'username', 'birthdate', 'sex', 'notification')
      widgets = {'birthdate': forms.DateInput(attrs={"placeholder": 'ДД.ММ.ГГГГ'}),}
   

class UserPasswordReset(PasswordResetForm):
   pass  
      
      
class UserPasswordSet(SetPasswordForm):
   pass


class UserRegistration(UserCreationForm):
   
   password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "text-field__input"}))
   password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class": "text-field__input"}),)
      
   def __init__(self, *args, **kwargs):
      super(UserCreationForm, self).__init__(*args, **kwargs)
      self.fields['username'].help_text = ''
      self.fields['password1'].help_text = ''
      self.fields['password2'].help_text = ''

   def clean(self):
      email = self.cleaned_data.get('email')
      if email is not None and MyUser.objects.filter(email=email.lower()).exists():
         raise ValidationError("Данный Email уже занят!")
      return self.cleaned_data
        
   class Meta(UserCreationForm.Meta):
      model = get_user_model()
      fields = ['email', 'username', 'password1']
      widgets = {'email': forms.TextInput(attrs={"class": "text-field__input"}),
                 'username': forms.TextInput(attrs={"class": "text-field__input"}),
      }
      
      
class UserAuthentication(AuthenticationForm):
   # email = username
   def clean(self):
      data = self.data.copy()
      data['username'] = data['username'].lower()
      return data
   
