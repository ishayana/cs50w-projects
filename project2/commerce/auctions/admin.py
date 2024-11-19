from django.contrib import admin
from .models import User, Listing, Bids, Comment, Category

# Register your models here.
admin.site.register(User)

class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'bid', 'category']

admin.site.register(Listing, ListingAdmin)


class BidsAdmin(admin.ModelAdmin):
    list_display = ['amount', 'listing', 'user']

admin.site.register(Bids, BidsAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'listing', 'text']

admin.site.register(Comment, CommentAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)