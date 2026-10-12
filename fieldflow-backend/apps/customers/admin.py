from django.contrib import admin
from .models import Customer, ServiceLocation, Asset
admin.site.register([Customer,ServiceLocation,Asset])
