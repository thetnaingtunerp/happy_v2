from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=225)

    def __str__(self):
        return self.category_name


class Item(models.Model):
    itemname = models.CharField(max_length=255,blank=True, null=True)
    category = models.CharField(max_length=225)
    iunit = models.CharField(max_length=255,blank=True, null=True)
    saleprice = models.PositiveIntegerField(default=0)
    purchaseprice = models.PositiveIntegerField(default=0)
    stockbalance = models.IntegerField(default=0)
    superitem = models.CharField(max_length=255,blank=True, null=True)
    unpackqty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.itemname

