from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from .models import Budget
from .forms import BudgetForm
from django.db.models import Sum
from datetime import date

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'FinanceTracker/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'FinanceTracker/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')

@login_required
def home(request):
    return render(request, 'FinanceTracker/home.html')

@login_required
def expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()
    user_expenses = Expense.objects.filter(user=request.user)
    return render(request, 'FinanceTracker/expenses.html', {'form': form, 'expenses': user_expenses})

@login_required
def income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income')
    else:
        form = IncomeForm()

    incomes = Income.objects.filter(user=request.user)
    return render(request, 'FinanceTracker/income.html', {'form': form, 'incomes': incomes})

@login_required
def transactions(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')  # Sort expenses by date (newest first)
    income = Income.objects.filter(user=request.user).order_by('-date')  # Sort income by date (newest first)
    return render(request, 'FinanceTracker/transactions.html', {'expenses': expenses, 'income': income})

@login_required
def budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget')
    else:
        form = BudgetForm()

    current_month = date.today().replace(day=1)
    budgets = Budget.objects.filter(user=request.user, month__year=current_month.year, month__month=current_month.month)
    expenses = Expense.objects.filter(user=request.user, date__year=current_month.year, date__month=current_month.month).values('category').annotate(total_amount=Sum('amount'))

    expense_dict = {expense['category']: expense['total_amount'] for expense in expenses}

    budget_data = []
    total_budget = 0
    total_spent = 0
    for budget in budgets:
        spent = expense_dict.get(budget.category, 0)
        total_budget += budget.amount
        total_spent += spent
        remaining = budget.amount - spent
        progress = int((spent / budget.amount) * 100) if budget.amount > 0 else 0
        budget_data.append({
            'category': budget.category,
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': remaining,
            'progress': progress
        })

    overall_progress = int((total_spent / total_budget) * 100) if total_budget > 0 else 0

    return render(request, 'FinanceTracker/budget.html', {'form': form, 'budget_data': budget_data, 'overall_progress': overall_progress})
