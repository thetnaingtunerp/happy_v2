from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('test/',views.test, name='test'),
    path('dashboard/', DashboardView.as_view(), name='DashboardView'),
    path('login/', UserLoginView.as_view(), name = 'UserLoginView'),
    path('logout/', UserLogoutView.as_view(), name='UserLogoutView'),
    path('AdminUserLoginView/', AdminUserLoginView.as_view(), name='AdminUserLoginView'),
    
    #setup
    path('DashSetupView/', DashSetupView.as_view(), name='DashSetupView'),
    path('CreateMember/', CreateMember.as_view(), name='CreateMember'),
    path('CreateSupplier/', CreateSupplier.as_view(), name='CreateSupplier'),

    path('CategoryCreate',CategoryCreate.as_view(), name='CategoryCreate'),
    path('CateEditView/',CateEditView.as_view(), name='CateEditView'),
    path('CateDeleteView/',CateDeleteView.as_view(), name='CateDeleteView'),

    path('ProductCreate/', ProductCreate.as_view(), name='ProductCreate'),
    path('UnpackageView/<int:pk>/', UnpackageView.as_view(), name='UnpackageView'),
    path('ProductEditView/<int:pk>/', ProductEditView.as_view(), name='ProductEditView'),
    path('ProductDeleteView/<int:pk>/', ProductDeleteView.as_view(), name='ProductDeleteView'),

    path('UnitCreateView/', UnitCreateView.as_view(), name='UnitCreateView'),
    path('UnitEditView/', UnitEditView.as_view(), name='UnitEditView'),
    path('UnitDeleteView/', UnitDeleteView.as_view(), name='UnitDeleteView'),
    #sale
    path('', MyCartView.as_view(), name='MyCartView'),
    path('AddtoCart/', AddtoCart.as_view(), name='AddtoCart'),
    path('manage/<int:cp_id>/', ManageCartView.as_view(), name='ManageCartView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('InvoicesView/', InvoicesView.as_view(), name='InvoicesView'),

    path('pdf_invoice_create/<int:id>/', pdf_invoice_create, name='pdf_invoice_create'),
    path('InvoiceDetailView/<int:pk>/', InvoiceDetailView.as_view(), name='InvoiceDetailView'),
    path('InvoiceThermalPrintView/<int:pk>/', InvoiceThermalPrintView.as_view(), name='InvoiceThermalPrintView'),


    #report
    path('SaleReportView/', SaleReportView.as_view(), name='SaleReportView'),
    path('SaleInvoiceReportView/', SaleInvoiceReportView.as_view(), name='SaleInvoiceReportView'),
    path('ReportHome/', ReportHome.as_view(), name='ReportHome'),
    path('PurchaseReportView/', PurchaseReportView.as_view(), name='PurchaseReportView'),

    #purchase
    path('PurchaseView/', PurchaseView.as_view(), name='PurchaseView'),
    path('PurchaseCart/', PurchaseCart.as_view(), name='PurchaseCart'),
    path('PurchaseCheckoutView/', PurchaseCheckoutView.as_view(), name='PurchaseCheckoutView'),
    path('PurchaseInvoiceDetailView/<int:pk>/', PurchaseInvoiceDetailView.as_view(), name='PurchaseInvoiceDetailView'),

]