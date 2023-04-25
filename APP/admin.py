from django.contrib import admin

# Register your models here.

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password')


admin.site.register(MyUser, MyUserAdmin)
