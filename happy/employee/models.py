from django.db import models

# Create your models here.

class gender(models.Model):
    gender = models.CharField(max_length=255)
    def __str__(self):
        return self.gender


class employee_profile(models.Model):
    employee_name = models.CharField(max_length=225, blank=True, null=True)
    nrc_no = models.CharField(max_length=225, unique=True)
    fathername = models.CharField(max_length=225)
    mothername = models.CharField(max_length=225)
    phone = models.CharField(max_length=225, blank=True, null=True)
    address = models.TextField()
    gender = models.ForeignKey(gender, on_delete=models.CASCADE)
    dob = models.DateField()
    marital = models.CharField(max_length=225, blank=True, null=True)
    entrydate = models.DateField()
    salary = models.PositiveIntegerField(default=0)
    daily_rate = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    familytable = models.ImageField(upload_to='', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_name


class employee_attendance(models.Model):
    employee = models.ForeignKey(employee_profile, on_delete=models.CASCADE)
    entry_time = models.DateTimeField()
    checkout_time = models.DateTimeField(blank=True, null=True)
    att_hr = models.FloatField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.employee_name




