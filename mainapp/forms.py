from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

from .models import *

class ProgressFilling(forms.ModelForm):

      
   class Meta:
      model = DayProgress
      fields = ['sharpness_vision', 'colorness_vision', 'peripheral_vision', 'binocular_vision', 'additional_info']