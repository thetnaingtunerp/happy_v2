from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('test/',views.test, name='test'),
    path('', DashboardView.as_view(), name='DashboardView'),
    path('login/', UserLoginView.as_view(), name = 'UserLoginView'),
    path('logout/', UserLogoutView.as_view(), name='UserLogoutView'),
    
    #setup
    path('DashSetupView/', DashSetupView.as_view(), name='DashSetupView'),
    path('CreateMember/', CreateMember.as_view(), name='CreateMember'),
    path('CreateSupplier/', CreateSupplier.as_view(), name='CreateSupplier'),
    path('CategoryCreate',CategoryCreate.as_view(), name='CategoryCreate'),
    path('ProductCreate/', ProductCreate.as_view(), name='ProductCreate'),
    path('UnpackageView/', UnpackageView.as_view(), name='UnpackageView'),
    path('ProductEditView/<int:pk>/', ProductEditView.as_view(), name='ProductEditView'),
    path('ProductDeleteView/<int:pk>/', ProductDeleteView.as_view(), name='ProductDeleteView'),
    path('UnitCreateView/', UnitCreateView.as_view(), name='UnitCreateView'),
    #sale
    path('mycart/', MyCartView.as_view(), name='MyCartView'),
    path('AddtoCart/', AddtoCart.as_view(), name='AddtoCart'),
    path('manage/<int:cp_id>/', ManageCartView.as_view(), name='ManageCartView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('InvoicesView/', InvoicesView.as_view(), name='InvoicesView'),

    path('pdf_invoice_create/<int:id>/', pdf_invoice_create, name='pdf_invoice_create'),
    path('InvoiceDetailView/<int:pk>/', InvoiceDetailView.as_view(), name='InvoiceDetailView'),
    path('InvoiceThermalPrintView/<int:pk>/', InvoiceThermalPrintView.as_view(), name='InvoiceThermalPrintView'),


    #report
    path('SaleReportView/', SaleReportView.as_view(), name='SaleReportView'),

    #purchase
    path('PurchaseView/', PurchaseView.as_view(), name='PurchaseView'),
    path('PurchaseCart/', PurchaseCart.as_view(), name='PurchaseCart'),

]