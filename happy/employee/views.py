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


class SuperUserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated & request.user.is_superuser:
            pass
        else:
            return redirect('myapp:UserLoginView')
        return super().dispatch(request, *args, **kwargs)



class EmployeeView(SuperUserRequiredMixin,View):
    def get(self, request):
        object_list = employee_profile.objects.all()
        et = employee_attendance.objects.filter(created_at=datetime.datetime.now())
        fm = EmployeeForm()
        context = {'object_list':object_list, 'form':fm, 'et':et}
        return render(request, 'EmployeeView.html', context)

    def post(self, request):
        employee_name = request.POST.get('employee_name')
        nrc_no = request.POST.get('nrc_no')
        fathername = request.POST.get('fathername')
        mothername = request.POST.get('mothername')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        entrydate = request.POST.get('entrydate')
        salary = request.POST.get('salary')
        photo = request.FILES['photo']
        e = employee_profile(employee_name=employee_name, nrc_no=nrc_no, fathername=fathername,mothername=mothername, phone=phone, address=address, dob=dob, entrydate=entrydate, photo=photo, salary=salary)
        e.save()
        return redirect(request.META['HTTP_REFERER'])


class EmpEditView(SuperUserRequiredMixin, View):
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

class DailyAttendance(SuperUserRequiredMixin, View):
    def get(self, request):
        ep = employee_profile.objects.all()
        et = employee_attendance.objects.filter(created_at=datetime.datetime.now())
        context ={'ep':ep, 'et':et}
        return render(request, 'EmployeeView.html', context)
    
    def post(self, request):
        ed = request.POST.get('eid')
        today = datetime.datetime.now()
        cdate = datetime.date.today()
        emp_obj = employee_profile.objects.get(id=ed)
        ea = employee_attendance.objects.filter(employee=emp_obj, created_at=cdate)
        if ea:
            return redirect(request.META['HTTP_REFERER'])
        else:
            ee = employee_attendance(employee=emp_obj, entry_time=today)
            ee.save()
            return redirect(request.META['HTTP_REFERER'])

        

class EmpCheckout(SuperUserRequiredMixin, View):
    def post(self, request):
        ed = request.POST.get('aid')
        today = datetime.datetime.now()
        et = employee_attendance.objects.filter(id=ed).update(checkout_time=today)
        return redirect(request.META['HTTP_REFERER'])

class AttendanceReport(SuperUserRequiredMixin, View):
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
        return render(request, 'EmployeeView.html', context)

