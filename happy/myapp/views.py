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
        itemname = request.POST.get('itemname')
        category = request.POST.get('category')
        iunit = request.POST.get('iunit')
        purchaseprice = request.POST.get('purchaseprice')
        saleprice = request.POST.get('saleprice')
        superitem = request.POST.get('superitem')
        unpackqty = request.POST.get('unpackqty')

        message = None
        if not itemname:
            message = 'please enter items'
        if not message:
            item = Item(itemname=itemname,category=category, iunit=iunit, saleprice=saleprice,purchaseprice=purchaseprice,superitem=superitem,unpackqty=unpackqty)
            item.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            category = Category.objects.all()
            item_list = Item.objects.all()
            context = {'message': message,'category':category,'item_list':item_list}
            return render(request, 'productcreate.html', context)



class MyCartView(UserRequiredMixin,TemplateView):
    template_name = 'mycartview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        message = 1
        context['message'] = message
        context['cart'] = cart
        context['product_list'] = Item.objects.all().order_by('-id')
        context['queryset'] = Order.objects.filter(created_at=datetime.date.today()).order_by('-id')

        return context

class AddtoCart(View):
    def post(self, request):
        pid = request.POST.get('pid')
        qty = request.POST.get('quantity')

        itm_obj = Item.objects.get(id=pid)
        itm_id = itm_obj.id
        stock = itm_obj.stockbalance
        print(stock)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=itm_obj)
            # Product already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cp_subtotal = int(itm_obj.saleprice) * int(qty)
                cp_stockbalance = int(stock) - int(qty)
                cartproduct.quantity += int(qty)
                cartproduct.subtotal += cp_subtotal
                cartproduct.stockbalance = cp_stockbalance
                cartproduct.save()
                # item table stock balanc update
                itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance)

                cart_obj.total += cp_subtotal
                cart_obj.save()
                return redirect(request.META['HTTP_REFERER'])

            else:
                #new item add to cart
                # item_filter = Item.objects.filter(id=pid)
                cp_stockbalance = int(stock) - int(qty)
                cp_subtotal = int(itm_obj.saleprice) * int(qty)
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=itm_obj,
                                                         rate=itm_obj.saleprice,
                                                         quantity=qty, subtotal=cp_subtotal,
                                                         stockbalance=cp_stockbalance)
                # item table stock balanc update
                itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance)
                # Update Cart Total
                cart_obj.total += cp_subtotal
                cart_obj.save()
                return redirect(request.META['HTTP_REFERER'])

        else:
            cart_obj = Cart.objects.create(total=0, staff=request.user)
            self.request.session['cart_id'] = cart_obj.id
            # item_filter = Item.objects.filter(id=itm_obj)
            cp_stockbalance = int(stock) - int(qty)
            cp_subtotal = int(itm_obj.saleprice) * int(qty)
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=itm_obj,
                                                     rate=itm_obj.saleprice,
                                                     quantity=qty, subtotal=cp_subtotal,
                                                     stockbalance=cp_stockbalance)
            #item table stock balanc update
            itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance)

            #Update Cart Total
            cart_obj.total += cp_subtotal
            cart_obj.save()
            return redirect(request.META['HTTP_REFERER'])



class ManageCartView(UserRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        cp_id = kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            # cp_obj.remain_balance += cp_obj.quantity
            item_balance = cp_obj.stockbalance +cp_obj.quantity
            item_update = Item.objects.filter(id=cp_obj.product.id).update(stockbalance=item_balance)
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('myapp:MyCartView')


class CheckoutView(UserRequiredMixin,CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('myapp:MyCartView')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         print('login....')
    #     else:
    #         return redirect('/login/?next=/checkout/')
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        # print(form.instance.delivery_fee)
        # deli = form.instance.delivery_fee
        dis = form.instance.discount
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            # form.instance.discount = 0
            form.instance.total = cart_obj.total

            # form.instance.ordered_staus = 'Cash'
            # form.instance.tax = cart_obj.tax
            # form.instance.all_total = cart_obj.super_total
            # total_deli = deli + cart_obj.super_total - dis
            # form.instance.all_total_delivery = total_deli

            del self.request.session['cart_id']
        else:
            return redirect('myapp:MyCartView')
        return super().form_valid(form)

class UnpackageView(View):
    def post(self,request):
        i = request.POST.get('pid')
        getitm = Item.objects.get(id=i)
        sup = getitm.superitem
        getitm.stockbalance += getitm.unpackqty
        getitm.save()
        supitm = Item.objects.get(id=sup)
        supitm.stockbalance -=1
        supitm.save()


        return redirect('myapp:MyCartView')

