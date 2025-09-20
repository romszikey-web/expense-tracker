from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Lunch at KFC'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food, Transport...'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }