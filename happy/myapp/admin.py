from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(CartProduct)


admin.site.register(pOrder)
admin.site.register(pCartProduct)