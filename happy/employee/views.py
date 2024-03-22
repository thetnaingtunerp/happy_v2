from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from .models import *
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum,Count,F
from django.http import HttpResponse
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView,ListView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime


from django.forms import modelformset_factory
from django.urls import reverse


class EmployeeView(View):
    def get(self, request):
        object_list = employee_profile.objects.all()
        fm = EmployeeForm()
        context = {'object_list':object_list, 'form':fm}
        return render(request, 'EmployeeView.html', context)

    def post(self, request):
        fm = EmployeeForm(request.POST)
        if fm.is_valid():
            fm.save()
        return redirect(request.META['HTTP_REFERER'])


class EmpEditView(View):
    def get(self,request, pk):
        pi = employee_profile.objects.get(id=pk)
        fm = EmployeeForm(instance=pi)
        return render(request,'EmployeeView.html', {'form':fm})

    def post(self, request, pk):
        pi = employee_profile.objects.get(id=pk)
        fm = EmployeeForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('employee:EmployeeView')

class DailyAttendance(View):
    def get(self, request):
        ep = employee_profile.objects.all()
        et = employee_attendance.objects.filter(created_at=datetime.datetime.now())
        context ={'ep':ep, 'et':et}
        return render(request, 'DailyAttendance.html', context)
    
    def post(self, request):
        ed = request.POST.get('eid')
        today = datetime.datetime.now()
        emp_obj = employee_profile.objects.get(id=ed)
        ee = employee_attendance(employee=emp_obj, entry_time=today)
        ee.save()
        return redirect(request.META['HTTP_REFERER'])
        

class EmpCheckout(View):
    def post(self, request):
        ed = request.POST.get('eid')
        today = datetime.datetime.now()
        emp_obj = employee_profile.objects.get(id=ed)
        et = employee_attendance.objects.filter(employee=emp_obj).update(checkout_time=today)
        return redirect(request.META['HTTP_REFERER'])

class AttendanceReport(View):
    def get(self, request):
        ep = employee_profile.objects.all()
        et = employee_attendance.objects.all()
        context ={'ep':ep, 'et':et}
        return render(request, 'AttendanceReport.html', context)
    
    def post(self, request):
        sd = request.POST.get('sdate')
        ed = request.POST.get('edate')
        et =employee_attendance.objects.filter(created_at__range=[sd, ed])
        context ={'et':et}
        return render(request, 'AttendanceReport.html', context)

