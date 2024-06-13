from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario



# Register your models here.
class UsuarioAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'departamento', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('first_name','last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering =('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Usuario, UsuarioAdmin)

