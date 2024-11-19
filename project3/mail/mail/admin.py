from django.contrib import admin
from .models import Email, User
# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ['sender', 'user', 'subject']

admin.site.register(Email, EmailAdmin)