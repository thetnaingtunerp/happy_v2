from django import forms
from .models import *


class ULoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }




class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['member', 'discount','payment',]
        widgets = {

            'member': forms.Select(attrs={'class':'form-control custom-select2 col-md-6'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control col-md-4'}),
            'payment': forms.Select(attrs={'class': 'form-control col-md-4'}),
            # 'delivery_system': forms.Select(attrs={'class': 'form-control col-md-6'}),
            # 'deli_payment':forms.BooleanField(),

            # 'id':forms.Textarea

        }



class PurchaseCheckoutForm(forms.ModelForm):
    class Meta:
        model = pOrder
        fields = ['supplier', 'discount','payment',]
        widgets = {

            'supplier': forms.Select(attrs={'class':'form-control custom-select2 col-md-6'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control col-md-4'}),
            'payment': forms.Select(attrs={'class': 'form-control col-md-4'}),
            # 'delivery_system': forms.Select(attrs={'class': 'form-control col-md-6'}),
            # 'deli_payment':forms.BooleanField(),

            # 'id':forms.Textarea

        }




class AdminProductEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemname','category', 'iunit', 'unpackqty','saleprice', 'purchaseprice']
        widgets = {
            'itemname': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'iunit': forms.TextInput(attrs={'class': 'form-control'}),
            'saleprice': forms.TextInput(attrs={'class': 'form-control'}),
            'purchaseprice': forms.TextInput(attrs={'class': 'form-control'}),
            'unpackqty': forms.TextInput(attrs={'class': 'form-control'}),
           

        }

