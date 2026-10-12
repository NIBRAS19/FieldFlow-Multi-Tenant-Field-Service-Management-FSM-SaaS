from django.contrib import admin
from .models import Organization, Membership
admin.site.register([Organization,Membership])
