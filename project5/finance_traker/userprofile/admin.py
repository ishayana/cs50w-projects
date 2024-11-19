from django.contrib import admin
from .models import Budget , Transaction, Category
# Register your models here.

class BudgetAdmin(admin.ModelAdmin):
    fields = ['category', 'amount']

admin.site.register(Budget, BudgetAdmin)

class TransactionAdmin(admin.ModelAdmin):
    fields = ['name', 'amount', 'category', 'transcaction_type']

admin.site.register(Transaction, TransactionAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Category, CategoryAdmin)