from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .utils import user_directory_path, correct_email

from uuslug import uuslug, slugify


class CustomAccountManager(BaseUserManager):
   
   def create_user(self, email, username, password=None, **extra_fields):
      if not email:
         raise ValueError(_('Please provide an email address'))
      user=self.model(username=username, email=correct_email(email), **extra_fields)
      user.set_password(password)
      user.save()
      return user

   def create_superuser(self, email, username, password, **extra_fields):
      extra_fields.setdefault('is_staff',True)
      extra_fields.setdefault('is_superuser',True)
      extra_fields.setdefault('is_active',True)
      if extra_fields.get('is_staff') is not True:
         raise ValueError(_('Please assign is_staff=True for superuser'))
      if extra_fields.get('is_superuser') is not True:
         raise ValueError(_('Please assign is_superuser=True for superuser'))
      return self.create_user(email, username, password, **extra_fields)
   
class MyUser(AbstractBaseUser, PermissionsMixin):
   id = models.AutoField(_('id'),primary_key=True)
   email = models.EmailField(_('Адрес Почты'), unique=True)
   username = models.CharField(_('Имя Пользователя'), max_length=25, db_index=True)
   is_staff = models.BooleanField(_('Модератор'), default=False)
   is_active = models.BooleanField(_('Активирован'), default=False)
   description = models.CharField(_('Описание'),max_length=150, blank=True)
   userpic = models.ImageField(_('Аватар'), upload_to=user_directory_path, blank=True, default='baseuserpic.jpg')
   date_joined = models.DateTimeField(_("Дата регистрации"), blank=True, null=True, auto_now_add=True)
   birthdate = models.DateTimeField(_("Дата рождения"), blank=True, null=True)
   userslug = models.SlugField(_('userslug'), max_length=150, unique=True, db_index=True)
   SEX = [('Male', 'M'), ('Female', 'F'),]
   sex = models.CharField(_("Пол"), max_length=1, choices=SEX)
   notification = models.BooleanField(_("Уведомления"), default=False)
   
   objects = CustomAccountManager()
   
   USERNAME_FIELD='email' #the name of the field on the user model that is used as the unique identifier
   REQUIRED_FIELDS=['username'] # запрашиваемое поле при вызове createsuperuser

   def __str__(self):
      return self.email
    
   def save(self, *args, **kwargs):
      #superuserslug
      if self.is_superuser:                                                                                                     
         self.userslug = self.username.lower().replace(' ', '-')
      try:
         super(MyUser, self).save(*args, **kwargs)
      except:
         raise ValueError(_('This user already exists!'))
      self.update_user_slug() 
      
   def update_user_slug(self):
      # You now have both access to self.id
      if not self.is_superuser: 
         #now have both access to self.id
         self.userslug = str(self.id) + '-' + slugify(self.username.lower().replace(' ', '-'))
         MyUser.objects.filter(id=self.id).update(userslug=self.userslug)
         
   def get_absolute_url(self):
        return reverse('user-page', args=[self.userslug])
      
      
class Task(models.Model):
   title = models.CharField(_("Заголовок"), max_length=35)
   description = models.CharField(_("Описание"), max_length=85)
   link = models.URLField(_("Ссылка"), max_length=250)
   count = models.IntegerField(_("Количество заданий"), validators=[
      MinValueValidator(1), 
      MaxValueValidator(100)
      ]
   )
   status = models.BooleanField(_("Выполнено"), default=False)


class Instruction(models.Model):
   title = models.CharField(_("Заголовок"), max_length=35)
   file = models.FileField(_("Файл"),upload_to='files/%Y/%m/%d', blank=True)
   status = models.BooleanField(_("Просмотрено"), default=False)
   
   
class Survey(models.Model):
   title = models.CharField(_("Заголовок"), max_length=35)
   link = models.URLField(_("Ссылка"), max_length=250)
   status = models.BooleanField(_("Просмотрено"), default=False)
   
   
class DayProgress(models.Model):
   user = models.ForeignKey(_("Пользователь"), MyUser, on_delete=models.CASCADE)
   sharpness_vision = models.IntegerField(_("Острота зрение"),)
   colorness_vision = models.IntegerField(_("Цветовое зрение"),)
   peripheral_vision = models.IntegerField(_("Переферическое зрение"),)
   binocular_vision  = models.IntegerField(_("Бинокулярное зрение"),)
   additional_info = models.IntegerField(_("Дополнительная информация"),)
   current_date = models.DateField(_("Дата действия"),)
   
class Dictionary(models.Model):
   pass
   