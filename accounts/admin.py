from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Permiso, Rol

class PermisoAdmin(admin.ModelAdmin):
    list_display = ('clase', 'nombre')
    list_filter = ('clase',) 

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'name', 'apellidos', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'roles')
    search_fields = ('username', 'name', 'apellidos', 'email')
    ordering = ('id',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'name', 'apellidos', 'email', 'password')}),
        ('Información de permisos', {'fields': ('is_staff', 'is_active', 'roles')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'apellidos', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'roles')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Permiso, PermisoAdmin) 
admin.site.register(Rol)
