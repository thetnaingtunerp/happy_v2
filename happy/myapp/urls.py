from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('',views.test, name='test'),
    path('login/', UserLoginView.as_view(), name = 'UserLoginView'),
    path('logout/', UserLogoutView.as_view(), name='UserLogoutView'),
    #setup
    path('CreateMember/', CreateMember.as_view(), name='CreateMember'),
    path('CategoryCreate',CategoryCreate.as_view(), name='CategoryCreate'),
    path('ProductCreate/', ProductCreate.as_view(), name='ProductCreate'),
    path('UnpackageView/', UnpackageView.as_view(), name='UnpackageView'),
    #sale
    path('mycart/', MyCartView.as_view(), name='MyCartView'),
    path('AddtoCart/', AddtoCart.as_view(), name='AddtoCart'),
    path('manage/<int:cp_id>/', ManageCartView.as_view(), name='ManageCartView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),


    #report

]