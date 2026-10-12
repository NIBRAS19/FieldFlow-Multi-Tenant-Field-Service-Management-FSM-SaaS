from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Customer, ServiceLocation, Asset
from .serializers import CustomerSerializer, ServiceLocationSerializer, AssetSerializer
from apps.organizations.services import get_current_org

class OrgViewSetMixin:
    organization_field='organization'
    def get_org(self): return get_current_org(self.request)

class CustomerViewSet(OrgViewSetMixin, viewsets.ModelViewSet):
    serializer_class=CustomerSerializer
    search_fields=['name','company','contact_name','email','phone']
    ordering_fields=['name','created_at']
    def get_queryset(self): return Customer.objects.filter(organization=self.get_org())
    def perform_create(self, serializer): serializer.save(organization=self.get_org())

class ServiceLocationViewSet(OrgViewSetMixin, viewsets.ModelViewSet):
    serializer_class=ServiceLocationSerializer
    search_fields=['name','address_line','city']
    def get_queryset(self): return ServiceLocation.objects.filter(organization=self.get_org()).select_related('customer')
    def perform_create(self, serializer):
        org=self.get_org(); customer_id=self.request.data.get('customer')
        if not Customer.objects.filter(id=customer_id, organization=org).exists(): raise PermissionDenied('Invalid customer.')
        serializer.save(organization=org)

class AssetViewSet(OrgViewSetMixin, viewsets.ModelViewSet):
    serializer_class=AssetSerializer
    search_fields=['asset_id','category','manufacturer','model','serial_number']
    def get_queryset(self): return Asset.objects.filter(organization=self.get_org()).select_related('customer','location')
    def perform_create(self, serializer): serializer.save(organization=self.get_org())
