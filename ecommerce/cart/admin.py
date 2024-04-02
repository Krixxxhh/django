from django.contrib import admin
from django.http import HttpResponse
from cart.models import Cart,Account,Order
# Register your models here.
admin.site.register(Cart)
admin.site.register(Account)
admin.site.register(Order)