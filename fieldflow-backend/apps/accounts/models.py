from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        OPERATIONS = 'operations', 'Operations Manager'
        DISPATCHER = 'dispatcher', 'Dispatcher'
        TECHNICIAN = 'technician', 'Technician'
        FINANCE = 'finance', 'Finance'
        CUSTOMER = 'customer', 'Customer'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TECHNICIAN)
    phone = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    timezone = models.CharField(max_length=64, default='Asia/Dubai')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name() or self.username
