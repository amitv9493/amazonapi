from django.contrib import admin
from .models import user_credentials
# Register your models here.



@admin.register(user_credentials)

class user_credentialsAdmin(admin.ModelAdmin):
    pass
