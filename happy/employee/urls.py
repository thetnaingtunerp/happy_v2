from django.urls import path
from .views import *
from . import views
app_name = 'employee'
urlpatterns = [
    path('EmployeeView/', EmployeeView.as_view(), name='EmployeeView'),
    path('EmpEditView/<int:pk>/', EmpEditView.as_view(), name='EmpEditView'),
    path('DailyAttendance/', DailyAttendance.as_view(), name='DailyAttendance'),
    path('EmpCheckout/', EmpCheckout.as_view(), name='EmpCheckout'),
    path('AttendanceReport/', AttendanceReport.as_view(), name='AttendanceReport'),

    path('EmployeeProfileUpdate/', EmployeeProfileUpdate.as_view(), name='EmployeeProfileUpdate'),
    path('EmpDeleteView/', EmpDeleteView.as_view(), name='EmpDeleteView'),
]