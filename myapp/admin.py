from django.contrib import admin
from .models import *

admin.site.register(products)
admin.site.register(CartItems)
admin.site.register(UserCart)
# Register your models here.
