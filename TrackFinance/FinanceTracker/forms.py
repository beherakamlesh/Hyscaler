from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Income
from django import forms
from .models import Budget
from django.utils import timezone




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Change to Select widget
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'frequency', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
    source = forms.ChoiceField(choices=[('salary', 'Salary'), ('freelancing', 'Freelancing'), ('bonuses', 'Bonuses')], widget=forms.Select(attrs={'class': 'form-control'}))




from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('dining', 'Dining Out'),
        ('transportation', 'Transportation'),
        ('clothing', 'Clothing'),
        ('grocery', 'Grocery'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        # Add other categories as needed
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    month = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']


    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
