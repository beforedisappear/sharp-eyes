# Generated by Django 4.1.5 on 2023-06-14 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_myuser_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='userpic',
        ),
    ]
