from django.db import models
from apps.organizations.models import Organization

class Customer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=180)
    company = models.CharField(max_length=180, blank=True)
    contact_name = models.CharField(max_length=180, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    secondary_phone = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.company or self.name

class ServiceLocation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='locations')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=180)
    address_line = models.TextField()
    city = models.CharField(max_length=100, default='Abu Dhabi')
    emirate = models.CharField(max_length=100, default='Abu Dhabi')
    country = models.CharField(max_length=80, default='United Arab Emirates')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    access_instructions = models.TextField(blank=True)
    contact_name = models.CharField(max_length=180, blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    operating_hours = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)

class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE='active','Active'; MAINTENANCE_DUE='maintenance_due','Maintenance Due'; OUT_OF_SERVICE='out_of_service','Out of Service'; RETIRED='retired','Retired'
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='assets')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='assets')
    location = models.ForeignKey(ServiceLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    asset_id = models.CharField(max_length=80)
    category = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=120, blank=True)
    model = models.CharField(max_length=120, blank=True)
    serial_number = models.CharField(max_length=120, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.UniqueConstraint(fields=['organization','asset_id'], name='uniq_asset_org')]
