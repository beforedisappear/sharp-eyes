from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model


from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, UserChangeForm

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
      
      
class UserChangeCustom(UserChangeForm):
   
   def __init__(self, *args, **kwargs):
      super(UserChangeForm, self).__init__(*args, **kwargs)
      del self.fields['password']
      self.fields["sex"].choices = [("", ""),] + list(self.fields["sex"].choices)[1:]

   class Meta:
      model = get_user_model()
      fields = ('userpic', 'email', 'username', 'birthdate', 'sex', 'notification')
      widgets = {'birthdate': forms.DateInput(attrs={"placeholder": 'ДД.ММ.ГГГГ'}),}


class UserPasswordReset(PasswordResetForm):
   pass  
      
class UserPasswordSet(SetPasswordForm):
   pass