from django.contrib import admin
from django.urls import path, include
from FinanceTracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),  # Root URL for login page
    path('logout/', views.user_logout, name='logout'),
    path('expenses/', views.expenses, name='expenses'),
    path('income/', views.income, name='income'),
    path('budget/', views.budget, name='budget'),
    path('transactions/', views.transactions, name='transactions'),
]
