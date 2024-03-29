from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = employee_profile
        fields = ['employee_name', 'nrc_no', 'fathername', 'mothername', 'phone', 'gender', 'dob', 'address', 'entrydate', 'photo', 'salary']
        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nrc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'fathername': forms.TextInput(attrs={'class': 'form-control'}),
            'mothername': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control '}),
            # 'marital': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={"type": "date", 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'entrydate': forms.DateInput(attrs={"type": "date", 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # 'familytable': forms.FileInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'daily_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }




class DateFilterForm(forms.Form):
    start_date = forms.DateInput(attrs={"type": "date", 'class': 'form-control'}),
    end_date = forms.DateInput(attrs={"type": "date", 'class': 'form-control'}),



