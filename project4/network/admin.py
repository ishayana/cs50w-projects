from django.contrib import admin
from .models import Follow, Post, Like
# Register your models here.



class FollowAdmin(admin.ModelAdmin):
    fields= ['following', 'follower']
admin.site.register(Follow, FollowAdmin)


class PostAdmin(admin.ModelAdmin):
    fields= ['author', 'text']
admin.site.register(Post, PostAdmin)