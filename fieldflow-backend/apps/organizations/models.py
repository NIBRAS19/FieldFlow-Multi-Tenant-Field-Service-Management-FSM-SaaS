from django.conf import settings
from django.db import models
from apps.accounts.models import User

class Organization(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='organizations/', blank=True, null=True)
    industry = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=80, default='United Arab Emirates')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    timezone = models.CharField(max_length=64, default='Asia/Dubai')
    currency = models.CharField(max_length=3, default='AED')
    tax_number = models.CharField(max_length=80, blank=True)
    workday_start = models.TimeField(default='08:00')
    workday_end = models.TimeField(default='18:00')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.name) or 'organization'
            slug = base
            i = 2
            while Organization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{i}'; i += 1
            self.slug = slug
        return super().save(*args, **kwargs)

class Membership(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=User.Role.choices, default=User.Role.TECHNICIAN)
    active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['organization','user'], name='uniq_org_user')]
