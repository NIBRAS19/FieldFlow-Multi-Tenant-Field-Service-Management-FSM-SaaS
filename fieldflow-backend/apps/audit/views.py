from rest_framework import viewsets
from apps.organizations.services import get_current_org
from .models import AuditLog
from .serializers import AuditLogSerializer
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=AuditLogSerializer
    search_fields=['action','resource','resource_id','actor__username']
    def get_queryset(self): return AuditLog.objects.filter(organization=get_current_org(self.request)).select_related('actor')
