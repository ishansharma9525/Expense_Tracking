from django.db import models
from datetime import datetime

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    expense_list = models.ManyToManyField('Expense', blank=True)

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0.0)
    date = models.DateField(default=datetime.now)
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(default=0.0, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    monthly_expenses = models.FloatField(default=0.0, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses')


    def calculate_monthly_expenses(self):
        if self.long_term:
            if self.interest_rate == 0:
                return self.amount / ((self.end_date - self.date)/ 30)
            else:
                months = (self.end_date.year - datetime.now().year) * 12 + self.end_date.month - datetime.now().month
                monthly_rate = self.interest_rate / 12 /100
                monthly_expense = (self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
                return round(monthly_expense, 2)
        else:
            return self.monthly_expense