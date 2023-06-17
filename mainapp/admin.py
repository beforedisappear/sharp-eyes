from .models import *
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class StaffPermissionMixin:
        
    def has_delete_permission(self, request, obj=None):
        user = request.user
        if user.is_staff and not user.is_superuser: return False
        return True
    
    def has_add_permission(self, request, obj=None):
        return False
    
class UserAdmin(StaffPermissionMixin, BaseUserAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)
    #display custom fields
    fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),
    (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (_('Important dates'), {'fields': ('last_login', 'date_joined', 'birthdate')}),
    (_('Дополнительная информация'), {'fields': ('sex', 'description', 'userslug')}),
    )
    readonly_fields = ["date_joined", "is_superuser"]
   
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        
        disabled_fields = ['email', 'is_active', 'user_permissions', 'userslug']
        if obj is not None and obj.is_superuser:
            disabled_fields.extend(('username', 'is_staff'))
            
        if obj is not None and obj == user:
            disabled_fields.extend(('is_staff',))
                
        if not user.is_superuser and user.is_staff:
            for f in disabled_fields:
                form.base_fields[f].disabled = True

        return form
    

admin.site.register(MyUser, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link', 'count', 'is_active', 'time_create')

admin.site.register(Task, TaskAdmin)


class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'is_active', 'time_create')

admin.site.register(Instruction, InstructionAdmin)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'is_active', 'time_create')

admin.site.register(Survey, SurveyAdmin)


class DayProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_date', 'sharpness_vision', 'colorness_vision', 'peripheral_vision', 'binocular_vision')
    list_filter = ('user', 'current_date')
    
    def has_add_permission(self, request, obj=None):
        user = request.user
        if user.is_staff and not user.is_superuser:
            return False
        return True

admin.site.register(DayProgress, DayProgressAdmin)

admin.site.site_title = "SharpEyes"
admin.site.site_header = "SharpEyes"