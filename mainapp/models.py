from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .utils import user_directory_path

from uuslug import slugify


class CustomAccountManager(BaseUserManager):
   
   def create_user(self, email, username, password=None, **extra_fields):
      if not email:
         raise ValueError(_('Please provide an email address'))
      print(email)
      user=self.model(username=username, email=email.lower(), **extra_fields)
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
   userpic = models.ImageField(_('Аватар'), upload_to=user_directory_path, 
                               blank=True, default='baseuserpic.jpg') #mediafile
   date_joined = models.DateField(_("Дата регистрации"), blank=True, null=True, auto_now_add=True)
   birthdate = models.DateField(_("Дата рождения"), blank=True, null=True)
   userslug = models.SlugField(_('userslug'), max_length=150, unique=True, db_index=True)
   SEX = [('M', 'М'), ('F', 'Ж'),]
   sex = models.CharField(_("Пол"), max_length=1, choices=SEX, blank=True)
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
      return reverse('profilepage', kwargs={"userslug": self.userslug})
     
   class Meta:
      verbose_name = 'Пользователь'
      verbose_name_plural = 'Пользователи'
      
      
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
   time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
   is_active = models.BooleanField(_("Доступно"), default=True)
   
   def __str__(self):
      return self.title
      
   class Meta:
      verbose_name = 'Задание'
      verbose_name_plural = 'Задания'
      ordering = ['time_create']


class Instruction(models.Model):
   title = models.CharField(_("Заголовок"), max_length=35)
   file = models.FileField(_("Файл"),upload_to='files/%Y/%m/%d', blank=True) #mediafile
   status = models.BooleanField(_("Просмотрено"), default=False)
   time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
   is_active = models.BooleanField(_("Доступно"), default=True)
   
   class Meta:
      verbose_name = 'Инструкцию'
      verbose_name_plural = 'Инструкции'
      ordering = ['time_create']
   
   def __str__(self):
      return self.title
   
class Survey(models.Model):
   title = models.CharField(_("Заголовок"), max_length=35)
   link = models.URLField(_("Ссылка"), max_length=250)
   status = models.BooleanField(_("Просмотрено"), default=False)
   time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
   is_active = models.BooleanField(_("Доступно"), default=True)
   
   class Meta:
      verbose_name = 'Опрос'
      verbose_name_plural = 'Опросы'
      ordering = ['time_create']
   
   def __str__(self):
      return self.title
   
class DayProgress(models.Model):
   #many dayprogess to one user
   user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
   sharpness_vision = models.IntegerField(_("Острота зрение"),null=True, blank=True)
   colorness_vision = models.IntegerField(_("Цветовое зрение"),null=True, blank=True)
   peripheral_vision = models.IntegerField(_("Переферическое зрение"),null=True, blank=True)
   binocular_vision  = models.IntegerField(_("Бинокулярное зрение"),null=True, blank=True)
   additional_info = models.CharField(_("Дополнительная информация"), max_length=150, null=True, blank=True)
   current_date = models.DateField(_("Дата действия"), auto_now_add=True)
   
   def __str__(self):
      return f"{self.user.username} | {self.current_date.strftime('%d.%m.%Y')}"
   
   class Meta:
      verbose_name = 'Прогресс'
      verbose_name_plural = 'Прогресс пользователей'
      