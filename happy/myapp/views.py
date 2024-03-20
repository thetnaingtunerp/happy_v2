import datetime

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum,Count,F
from django.http import HttpResponse
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView,ListView
# import generic UpdateView
from django.views.generic.edit import DeleteView

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

class DashboardView(TemplateView):
    template_name = "dashboard.html"


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = ULoginForm
    success_url = reverse_lazy('myapp:DashboardView')

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


class CategoryCreate(UserRequiredMixin, View):
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

class CreateMember(UserRequiredMixin, View):
    def get(self, request):
        fm = MemberForm()
        m = Member.objects.all()
        return render(request, 'CreateMember.html', {'m':m, 'form':fm})

    def post(self, request):
        fm = MemberForm(request.POST)
        if fm.is_valid():
            fm.save()
        return redirect(request.META['HTTP_REFERER'])


class CreateSupplier(UserRequiredMixin, View):
    def get(self, request):
        fm = SupplierForm()
        m = Supplier.objects.all()
        return render(request, 'CreateSupplier.html', {'m':m, 'form':fm})

    def post(self, request):
        fm = SupplierForm(request.POST)
        if fm.is_valid():
            fm.save()
        return redirect(request.META['HTTP_REFERER'])


class UnitCreateView(View):
    def post(self, request):
        iunit = request.POST.get('iunit')
        u = Unit(unit=iunit)
        u.save()
        return redirect(request.META['HTTP_REFERER'])

class ProductCreate(UserRequiredMixin, View):
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


class DashSetupView(UserRequiredMixin, View):
    def get(self,request):
        category = Category.objects.all()
        item_list = Item.objects.all()
        unt = Unit.objects.all()
        message = None
        context = {'item_list':item_list,'category':category,'message':message, 'unt':unt}
        return render(request, 'dsetupview.html', context)
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

class ProductEditView(UserRequiredMixin,View):
    def get(self,request, pk):
        pi = Item.objects.get(id=pk)
        fm = AdminProductEditForm(instance=pi)
        return render(request,'productedit.html', {'form':fm})

    def post(self, request, pk):
        pi = Item.objects.get(id=pk)
        fm = AdminProductEditForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('myapp:DashSetupView')




class ProductDeleteView(DeleteView):
    model = Item
    success_url = "/"
    template_name= 'item_confirm_delete.html'


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

class AddtoCart(UserRequiredMixin, View):
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
        getitm.stockbalance -= 1
        getitm.save()
        supitm = Item.objects.get(id=sup)
        supitm.stockbalance += getitm.unpackqty
        supitm.save()
        return redirect('myapp:MyCartView')


class InvoicesView(UserRequiredMixin,TemplateView):
    template_name = 'InvoicesView.html'
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



# ================= xhtml2pdf ===============
def pdf_invoice_create(request,id):
    ord_obj = Order.objects.get(id=id)
    template_path = 'pdf_invoice.html'
    context = {'ord_obj':ord_obj}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html,dest=response,
    )
    if pisa_status.err:
        return HttpResponse('have a error pdf')
    return response
    
class InvoiceDetailView(UserRequiredMixin,DetailView):
    template_name = 'invoicedetail.html'
    model = Order
    context_object_name = 'ord_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['allstatus'] = STATUS

        return context


class InvoiceThermalPrintView(UserRequiredMixin, DetailView):
    template_name = 'test_slip.html'
    model = Order
    context_object_name = 'ord_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['allstatus'] = STATUS

        return context


# ================================= Report ==================================

class SaleReportView(UserRequiredMixin, ListView): 
   
    # specify the model for list view 
    model = Order 
    template_name = 'SaleReportView.html'
   
    def get_queryset(self, *args, **kwargs): 
        qs = super(SaleReportView, self).get_queryset(*args, **kwargs) 
        qs = qs.order_by("-id") 
        return qs

class SaleInvoiceReportView(View):
    def get(self, request):
        ord = Order.objects.all()
        context ={'ord':ord}
        return render(request, 'SaleInvoiceReportView.html', context)

class ReportHome(TemplateView):
    template_name = 'ReportHome.html'

class PurchaseReportView(UserRequiredMixin, ListView):
    template_name = 'PurchaseReportView.html'
    model = pOrder

    def get_queryset(self, *args, **kwargs): 
        qs = super(PurchaseReportView, self).get_queryset(*args, **kwargs) 
        qs = qs.order_by("-id") 
        return qs


################################# Purchase #######################################
class PurchaseView(UserRequiredMixin,TemplateView):
    template_name = 'PurchaseView.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_pur = self.request.session.get('cart_pur', None)
        if cart_pur:
            pcart = pCart.objects.get(id=cart_pur)
        else:
            pcart = None
        
        context['pcart'] = pcart
        context['product_list'] = Item.objects.all().order_by('-id')
        context['queryset'] = pOrder.objects.filter(created_at=datetime.date.today()).order_by('-id')
        return context



class PurchaseCart(UserRequiredMixin, View):
    def post(self, request):
        pid = request.POST.get('pid')
        pprice = request.POST.get('price')
        qty = request.POST.get('quantity')

        itm_obj = Item.objects.get(id=pid)
        itm_id = itm_obj.id
        stock = itm_obj.stockbalance
        print(stock)
        cart_pur = self.request.session.get("cart_pur", None)
        if cart_pur:
            cart_obj = pCart.objects.get(id=cart_pur)
            this_product_in_pcart = cart_obj.pcartproduct_set.filter(product=itm_obj)
            # Product already exists in cart
            if this_product_in_pcart.exists():
                cartproduct = this_product_in_pcart.last()
                cp_subtotal = int(itm_obj.saleprice) * int(qty)
                cp_stockbalance = int(stock) + int(qty)
                cartproduct.quantity += int(qty)
                cartproduct.subtotal += cp_subtotal
                cartproduct.stockbalance = cp_stockbalance
                cartproduct.save()
                # item table stock balanc update
                itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance,purchaseprice=pprice )

                cart_obj.total += cp_subtotal
                cart_obj.save()
                return redirect(request.META['HTTP_REFERER'])

            else:
                #new item add to cart
                # item_filter = Item.objects.filter(id=pid)
                cp_stockbalance = int(stock) + int(qty)
                cp_subtotal = int(itm_obj.saleprice) * int(qty)
                cartproduct = pCartProduct.objects.create(cart=cart_obj, product=itm_obj,
                                                         rate=itm_obj.saleprice,
                                                         quantity=qty, subtotal=cp_subtotal,
                                                         stockbalance=cp_stockbalance)
                # item table stock balanc update
                itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance, purchaseprice=pprice)
                # Update Cart Total
                cart_obj.total += cp_subtotal
                cart_obj.save()
                return redirect(request.META['HTTP_REFERER'])

        else:
            cart_obj = pCart.objects.create(total=0, staff=request.user)
            self.request.session['cart_pur'] = cart_obj.id
            # item_filter = Item.objects.filter(id=itm_obj)
            cp_stockbalance = int(stock) + int(qty)
            cp_subtotal = int(itm_obj.saleprice) * int(qty)
            cartproduct = pCartProduct.objects.create(cart=cart_obj, product=itm_obj,
                                                     rate=itm_obj.saleprice,
                                                     quantity=qty, subtotal=cp_subtotal,
                                                     stockbalance=cp_stockbalance)
            #item table stock balanc update
            itm_update = Item.objects.filter(id=pid).update(stockbalance=cp_stockbalance, purchaseprice=pprice)

            #Update Cart Total
            cart_obj.total += cp_subtotal
            cart_obj.save()
            return redirect(request.META['HTTP_REFERER'])



class PurchaseCheckoutView(UserRequiredMixin,CreateView):
    template_name = 'pcheckout.html'
    form_class = PurchaseCheckoutForm
    success_url = reverse_lazy('myapp:PurchaseView')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         print('login....')
    #     else:
    #         return redirect('/login/?next=/checkout/')
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_pur = self.request.session.get("cart_pur", None)
        if cart_pur:
            cart_obj = pCart.objects.get(id=cart_pur)
        else:
            cart_obj = None
        context['pcart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_pur = self.request.session.get('cart_pur')
        # print(form.instance.delivery_fee)
        # deli = form.instance.delivery_fee
        dis = form.instance.discount
        if cart_pur:
            cart_obj = pCart.objects.get(id=cart_pur)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            # form.instance.discount = 0
            form.instance.total = cart_obj.total

            # form.instance.ordered_staus = 'Cash'
            # form.instance.tax = cart_obj.tax
            # form.instance.all_total = cart_obj.super_total
            # total_deli = deli + cart_obj.super_total - dis
            # form.instance.all_total_delivery = total_deli

            del self.request.session['cart_pur']
        else:
            return redirect('myapp:PurchaseView')
        return super().form_valid(form)


class PurchaseInvoiceDetailView(UserRequiredMixin,DetailView):
    template_name = 'PurchaseInvoiceDetailView.html'
    model = pOrder
    context_object_name = 'ord_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['allstatus'] = STATUS

        return context




