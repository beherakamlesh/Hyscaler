from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Expense, Income ,Budget

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Budget)
