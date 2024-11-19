from django.db import models
from accounts.models import User
from django.db.models import Sum



class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Budget(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=13)
    current_amount = models.DecimalField(decimal_places=2, max_digits=13)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budget')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount}"
    
    
class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=225, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=13)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=7)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.transaction_type}"
    
    @classmethod
    def total_income(cls):
        result = cls.objects.filter(transaction_type='income').aggregate(total=Sum('amount'))
        return result['total'] or 0
    
    
    @classmethod
    def total_expense(cls):
        result = cls.objects.filter(transaction_type='expense').aggregate(total=Sum('amount'))
        return result['total'] or 0