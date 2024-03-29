# Generated by Django 4.1.5 on 2023-05-15 19:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mainapp.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Адрес Почты')),
                ('username', models.CharField(db_index=True, max_length=25, verbose_name='Имя Пользователя')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Модератор')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активирован')),
                ('description', models.CharField(blank=True, max_length=150, verbose_name='Описание')),
                ('userpic', models.ImageField(blank=True, default='baseuserpic.jpg', upload_to=mainapp.utils.user_directory_path, verbose_name='Аватар')),
                ('date_joined', models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('userslug', models.SlugField(max_length=150, unique=True, verbose_name='userslug')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Пол')),
                ('notification', models.BooleanField(default=False, verbose_name='Уведомления')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35, verbose_name='Заголовок')),
                ('file', models.FileField(blank=True, upload_to='files/%Y/%m/%d', verbose_name='Файл')),
                ('status', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступно')),
            ],
            options={
                'verbose_name': 'Инструкцию',
                'verbose_name_plural': 'Инструкции',
                'ordering': ['time_create'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35, verbose_name='Заголовок')),
                ('link', models.URLField(max_length=250, verbose_name='Ссылка')),
                ('status', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступно')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'ordering': ['time_create'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=85, verbose_name='Описание')),
                ('link', models.URLField(max_length=250, verbose_name='Ссылка')),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Количество заданий')),
                ('status', models.BooleanField(default=False, verbose_name='Выполнено')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступно')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
                'ordering': ['time_create'],
            },
        ),
        migrations.CreateModel(
            name='DayProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharpness_vision', models.IntegerField(blank=True, null=True, verbose_name='Острота зрение')),
                ('colorness_vision', models.IntegerField(blank=True, null=True, verbose_name='Цветовое зрение')),
                ('peripheral_vision', models.IntegerField(blank=True, null=True, verbose_name='Переферическое зрение')),
                ('binocular_vision', models.IntegerField(blank=True, null=True, verbose_name='Бинокулярное зрение')),
                ('additional_info', models.CharField(blank=True, max_length=150, null=True, verbose_name='Дополнительная информация')),
                ('current_date', models.DateField(auto_now_add=True, verbose_name='Дата действия')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прогресс',
                'verbose_name_plural': 'Прогресс пользователей',
            },
        ),
    ]
