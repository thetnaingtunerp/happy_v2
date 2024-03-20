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
   