from django.urls import path
from .views import *
from . import views
app_name = 'employee'
urlpatterns = [
    path('EmployeeView/', EmployeeView.as_view(), name='EmployeeView'),
]