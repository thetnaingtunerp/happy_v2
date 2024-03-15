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


class Cart(models.Model):
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    super_total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    typeunit = models.CharField(max_length=255,null=True, blank=True)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    stockbalance = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Cart : "+ str(self.cart.id)+ "CartProduct : " + str(self.id)



PAYMENT_TYPE = (
    ("Cash","Cash"),
("Credit","Credit"),

)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    discount = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    payment = models.CharField(max_length=225, choices=PAYMENT_TYPE, default='Cash')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order : " + str(self.id)







