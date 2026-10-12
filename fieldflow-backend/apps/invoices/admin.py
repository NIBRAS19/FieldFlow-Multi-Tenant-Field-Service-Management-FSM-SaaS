from django.contrib import admin
from .models import Invoice,InvoiceItem,Payment
admin.site.register([Invoice,InvoiceItem,Payment])
