from django.contrib import admin
from django.contrib.auth.models import User
from .models import AdditionalUserData, Device, Sim , M2M_Device_Sim, Permission_type, Permissions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserDataInLine(admin.StackedInline):
    model = AdditionalUserData
    verbose_name_plural = "Additional User Data"

class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserDataInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Device)
admin.site.register(Sim)
admin.site.register(M2M_Device_Sim)
admin.site.register(Permissions)
admin.site.register(Permission_type)
