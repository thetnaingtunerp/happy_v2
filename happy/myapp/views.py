import datetime

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum,Count,F
from django.http import HttpResponse
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import *
from .models import *

#html2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
def test(request):
    return render(request, 'base.html')


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = ULoginForm
    success_url = reverse_lazy('myapp:MyCartView')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        usr = authenticate(username=username, password=password)

        if usr is not None:
            login(self.request, usr)

        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid user login!'})
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('myapp:UserLoginView')


class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('myapp:UserLoginView')
        return super().dispatch(request, *args, **kwargs)


class CategoryCreate(View):
    def get(self,request):
        category = Category.objects.all()
        item_list = Item.objects.all()
        message = None
        context = {'item_list': item_list, 'category': category, 'message': message}
        return render(request, 'categorycreate.html', context)
    def post(self,request):
        category_name = request.POST.get('category_name')
        message = None
        if not category_name:
            message = 'please enter category name'
        if not message:
            cate = Category(category_name=category_name)
            cate.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            category = Category.objects.all()
            message = 'please enter category name'
            return render(request, 'categorycreate.html', {'message':message,'category':category})

class CreateMember(View):
    def get(self, request):
        fm = MemberForm()
        m = Member.objects.all()
        return render(request, 'CreateMember.html', {'m':m, 'form':fm})

    def post(self, request):
        fm = MemberForm(request.POST)
        if fm.is_valid():
            fm.save()
        return redirect(request.META['HTTP_REFERER'])


class ProductCreate(View):
    def get(self,request):
        category = Category.objects.all()
        item_list = Item.objects.all()
        message = None
        context = {'item_list':item_list,'category':category,'message':message}
        return render(request, 'productcreate.html', context)
    def post(self,request):
        item_name = request.POST.get('item_name')
        category = request.POST.get('category')
        iunit = request.POST.get('iunit')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        superitem = request.POST.get('superitem')
        unpackqty = request.POST.get('unpackqty')

        message = None
        if not item_name:
            message = 'please enter items'
        if not message:
            item = Item(item_name=item_name,category=category, iunit=iunit, pruchase_price=purchase_price,sell_price=sale_price,superitem=superitem,unpackqty=unpackqty)
            item.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            category = Category.objects.all()
            item_list = Item.objects.all()
            context = {'message': message,'category':category,'item_list':item_list}
            return render(request, 'productcreate.html', context)


