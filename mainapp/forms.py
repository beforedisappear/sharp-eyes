from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from .models import *
from .utils import send_mail_for_changing_email


class LowercaseEmailField(forms.EmailField):
   def to_python(self, value):
      value = super(LowercaseEmailField, self).to_python(value)
      
      if isinstance(value, str):
         return value.lower()
      return value
     
    
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
         
   class Meta:
      model = DayProgress
      fields = ('sharpness_vision', 'colorness_vision', 'peripheral_vision', 'binocular_vision', 'additional_info')
      
      
class UserChangeCustom(forms.ModelForm):
   emailfield = LowercaseEmailField(label="Адрес почты")
   
   def __init__(self, *args, **kwargs): 
      super(UserChangeCustom, self).__init__(*args, **kwargs)
      self.fields["sex"].choices = [("", ""),] + list(self.fields["sex"].choices)[1:]
      #filling form existing username after successful attempt
      if len(kwargs) != 0: self.fields["emailfield"].initial = kwargs['instance']
      
         
   def clean(self):
      cleaned_data = super().clean()
      email = cleaned_data['emailfield']
      if str(self.fields["emailfield"].initial) != email:
         if MyUser.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован")
      return cleaned_data
   
   class Meta:
      model = get_user_model()
      fields = ('emailfield', 'username', 'birthdate', 'sex', 'notification')
      widgets = {'birthdate': forms.DateInput(attrs={"placeholder": 'ДД.ММ.ГГГГ'}),}
   

class UserPasswordReset(PasswordResetForm):
   email = LowercaseEmailField(label="Адрес почты")
   

class UserRegistration(UserCreationForm):
   email = LowercaseEmailField(label="Адрес почты", error_messages={'unique': 'Данный Email уже занят!'})
   password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "text-field__input"}))
   password2 = forms.CharField(label="Подтвердите Пароль", widget=forms.PasswordInput(attrs={"class": "text-field__input"}),)
      
   def __init__(self, *args, **kwargs):
      super(UserCreationForm, self).__init__(*args, **kwargs)
      self.fields['username'].help_text = ''
      self.fields['password1'].help_text = ''
      self.fields['password2'].help_text = ''

   # def clean(self):
   #    data = super().clean()
   #    email = data['email']
   #    if email is not None and MyUser.objects.filter(email=email).exists():
   #       raise ValidationError("Данный Email уже занят!")
   #    return self.cleaned_data
        
   class Meta(UserCreationForm.Meta):
      model = get_user_model()
      fields = ('email', 'username', 'password1', 'password2')
     
     
class UserAuthentication(AuthenticationForm):
   username = LowercaseEmailField(label="Адрес почты")
   
   def clean(self):
      email = self.cleaned_data.get("username")
      try:
         user = MyUser.objects.get(email=email)
      except:
         raise ValidationError('Неправильный email')
      
      return self.cleaned_data


class UserPasswordSet(SetPasswordForm):
   pass