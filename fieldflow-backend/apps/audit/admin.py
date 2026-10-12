from django.contrib import admin
from .models import AuditLog
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display=('created_at','organization','actor','action','resource','resource_id')
    readonly_fields=[f.name for f in AuditLog._meta.fields]
