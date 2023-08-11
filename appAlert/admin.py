from django.contrib import admin

# Register your models here.
from .models import UserTokens
admin.site.register(UserTokens)