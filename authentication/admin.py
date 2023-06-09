from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Geolocation

User = get_user_model()

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    
    list_display = (
        'id', 'avatar', 'gender', 'email', 'first_name', 'last_name', 
        'date_joined',
    )
    search_fields = ('email', 'first_name', 'last_name')
    empty_value_display = '-нет-'

class GeolocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude')
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)    
admin.site.register(Geolocation, GeolocationAdmin)