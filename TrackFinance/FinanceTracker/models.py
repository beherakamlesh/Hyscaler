from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('groceries', 'Groceries'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('transportation', 'Transportation'),
        ('others', 'Others'),
    ]

    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'

class Income(models.Model):
    FREQUENCY_CHOICES = [
        ('one-time', 'One-time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.source} - {self.amount}'
    

class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('dining', 'Dining Out'),
        ('transportation', 'Transportation'),
        ('clothing', 'Clothing'),
        ('grocery', 'Grocery'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        # Add other categories as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.month.strftime('%Y-%m')}"
    

