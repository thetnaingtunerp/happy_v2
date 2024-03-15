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
    #sale

    #report

]