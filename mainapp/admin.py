from .models import *
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
   list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)
   #display custom fields
   fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),
    (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    (_('Дополнительная информация'), {'fields': ('userpic', 'description', 'userslug')}),
   )
   readonly_fields = ["date_joined", "is_superuser"]

admin.site.register(MyUser, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)


class InstructionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Instruction, InstructionAdmin)


class SurveyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Survey, SurveyAdmin)


class DayProgressAdmin(admin.ModelAdmin):
    pass

admin.site.register(DayProgress, DayProgressAdmin)