from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    ServiceType, Technician, ServiceRequest, WorkOrder, WorkOrderAssignment,
    ChecklistTemplate, Material, WorkOrderChecklistItem, WorkOrderMaterial,
    Attachment, CustomerSignature, Notification,
)
from .serializers import (
    ServiceTypeSerializer, TechnicianSerializer, ServiceRequestSerializer,
    WorkOrderSerializer, ChecklistTemplateSerializer, MaterialSerializer,
    WorkOrderChecklistSerializer, WorkOrderMaterialSerializer,
    AttachmentSerializer, SignatureSerializer, NotificationSerializer,
)
from .services import next_number, audit, assign_technician, transition
from apps.organizations.services import get_current_org, is_manager
from apps.customers.models import Customer, ServiceLocation, Asset
from apps.accounts.models import User

class OrgMixin:
    def org(self):
        return get_current_org(self.request)

class ServiceTypeViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class = ServiceTypeSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    def get_queryset(self): return ServiceType.objects.filter(organization=self.org())
    def perform_create(self, serializer): serializer.save(organization=self.org())

class TechnicianViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class = TechnicianSerializer
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'employee_code', 'team', 'area']
    ordering_fields = ['user__first_name', 'utilization', 'status']
    def get_queryset(self): return Technician.objects.filter(organization=self.org()).select_related('user')
    @action(detail=True, methods=['post'])
    def status(self, request, pk=None):
        tech = self.get_object(); value = request.data.get('status')
        if value not in dict(Technician.Status.choices): raise ValidationError({'status':'Invalid status.'})
        tech.status = value; tech.save(update_fields=['status'])
        return Response(self.get_serializer(tech).data)

class ServiceRequestViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    search_fields = ['request_no', 'title', 'description', 'customer__name', 'customer__company']
    ordering_fields = ['created_at', 'preferred_date', 'priority', 'status']
    def get_queryset(self):
        qs = ServiceRequest.objects.filter(organization=self.org()).select_related('customer','location','asset','service_type','created_by')
        status_value = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        if status_value: qs = qs.filter(status=status_value)
        if priority: qs = qs.filter(priority=priority)
        return qs
    def perform_create(self, serializer):
        org=self.org(); customer_id=self.request.data.get('customer')
        if not Customer.objects.filter(id=customer_id, organization=org).exists(): raise ValidationError({'customer':'Invalid customer for this organization.'})
        serializer.save(organization=org, created_by=self.request.user, request_no=next_number(ServiceRequest,'request_no','REQ',org))
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        service_request=self.get_object()
        if hasattr(service_request,'work_order'):
            return Response(WorkOrderSerializer(service_request.work_order).data)
        org=self.org()
        work_order=WorkOrder.objects.create(
            organization=org,
            work_order_no=next_number(WorkOrder,'work_order_no','WO',org),
            request=service_request,
            customer=service_request.customer,
            location=service_request.location,
            asset=service_request.asset,
            service_type=service_request.service_type,
            title=service_request.title,
            description=service_request.description,
            priority=service_request.priority,
            status=WorkOrder.Status.UNASSIGNED,
            created_by=request.user,
        )
        service_request.status=ServiceRequest.Status.CONVERTED; service_request.save(update_fields=['status','updated_at'])
        audit(request.user, org, 'convert_request', 'service_request', service_request.id, after={'work_order_id':work_order.id})
        return Response(WorkOrderSerializer(work_order).data, status=201)

class WorkOrderViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    search_fields = ['work_order_no','title','description','customer__name','customer__company']
    ordering_fields = ['created_at','scheduled_start','priority','status']
    def get_queryset(self):
        qs=WorkOrder.objects.filter(organization=self.org()).select_related('customer','location','asset','service_type','request','created_by').prefetch_related('assignments__technician__user','checklist_items','materials','attachments','signature')
        status_value=self.request.query_params.get('status'); tech_id=self.request.query_params.get('technician'); date=self.request.query_params.get('date')
        if status_value: qs=qs.filter(status=status_value)
        if tech_id: qs=qs.filter(assignments__technician_id=tech_id, assignments__unassigned_at__isnull=True)
        if date: qs=qs.filter(scheduled_start__date=date)
        return qs.distinct()
    def perform_create(self, serializer):
        org=self.org(); customer_id=self.request.data.get('customer')
        if not Customer.objects.filter(id=customer_id, organization=org).exists(): raise ValidationError({'customer':'Invalid customer.'})
        serializer.save(organization=org, created_by=self.request.user, work_order_no=next_number(WorkOrder,'work_order_no','WO',org))
    def _get(self, pk): return self.get_object()
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        wo=self._get(pk); technician_id=request.data.get('technician_id')
        tech=Technician.objects.filter(id=technician_id, organization=self.org(), active=True).select_related('user').first()
        if not tech: raise ValidationError({'technician_id':'Invalid technician.'})
        assign_technician(wo, tech, request.user)
        return Response(self.get_serializer(wo).data)
    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        wo=self._get(pk); value=request.data.get('status')
        valid=dict(WorkOrder.Status.choices)
        if value not in valid: raise ValidationError({'status':'Invalid work order status.'})
        if value == WorkOrder.Status.COMPLETED and not hasattr(wo,'signature'):
            # completion without a signature is allowed only for managers
            if not is_manager(request, wo.organization): raise PermissionDenied('Customer signature is required before technician completion.')
        transition(wo, value, request.user)
        return Response(self.get_serializer(wo).data)
    @action(detail=True, methods=['post'])
    def checklist(self, request, pk=None):
        wo=self._get(pk); item=WorkOrderChecklistItem.objects.create(work_order=wo,label=request.data.get('label','Checklist item'),sort_order=request.data.get('sort_order',0),required=request.data.get('required',False))
        return Response(WorkOrderChecklistSerializer(item).data,status=201)
    @action(detail=True, methods=['patch'], url_path='checklist/(?P<item_id>[^/.]+)')
    def update_checklist(self, request, pk=None, item_id=None):
        wo=self._get(pk); item=wo.checklist_items.filter(id=item_id).first()
        if not item: raise ValidationError({'item':'Checklist item not found.'})
        serializer=WorkOrderChecklistSerializer(item,data=request.data,partial=True); serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data)
    @action(detail=True, methods=['post'])
    def materials(self, request, pk=None):
        wo=self._get(pk); material=Material.objects.filter(id=request.data.get('material'), organization=self.org()).first()
        if not material: raise ValidationError({'material':'Invalid material.'})
        item=WorkOrderMaterial.objects.create(work_order=wo,material=material,quantity=request.data.get('quantity',1),unit_cost=request.data.get('unit_cost',material.unit_cost))
        material.stock_quantity = material.stock_quantity - item.quantity; material.save(update_fields=['stock_quantity'])
        return Response(WorkOrderMaterialSerializer(item).data,status=201)
    @action(detail=True, methods=['post'])
    def signature(self, request, pk=None):
        wo=self._get(pk)
        obj,created=CustomerSignature.objects.update_or_create(work_order=wo,defaults={'customer_name':request.data.get('customer_name',''),'signature_data':request.data.get('signature_data',''),'ip_address':request.META.get('REMOTE_ADDR')})
        audit(request.user,self.org(),'customer_signature','work_order',wo.id,after={'signature_id':obj.id})
        return Response(SignatureSerializer(obj).data,status=201 if created else 200)
    @action(detail=True, methods=['post'])
    def attachment(self, request, pk=None):
        wo=self._get(pk)
        if 'file' not in request.FILES: raise ValidationError({'file':'File is required.'})
        attachment=Attachment.objects.create(work_order=wo,file=request.FILES['file'],kind=request.data.get('kind','photo'),caption=request.data.get('caption',''),uploaded_by=request.user)
        return Response(AttachmentSerializer(attachment).data,status=201)

class ChecklistTemplateViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class=ChecklistTemplateSerializer
    def get_queryset(self): return ChecklistTemplate.objects.filter(organization=self.org()).prefetch_related('items')
    def perform_create(self, serializer): serializer.save(organization=self.org())

class MaterialViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class=MaterialSerializer
    search_fields=['sku','name']
    def get_queryset(self): return Material.objects.filter(organization=self.org())
    def perform_create(self, serializer): serializer.save(organization=self.org())

class NotificationViewSet(OrgMixin, viewsets.ModelViewSet):
    serializer_class=NotificationSerializer
    http_method_names=['get','patch','head','options']
    def get_queryset(self): return Notification.objects.filter(organization=self.org(),user=self.request.user).order_by('-created_at')
    def perform_update(self, serializer): serializer.save()

class DashboardView(APIView):
    def get(self, request):
        org=get_current_org(request); today=timezone.localdate(); jobs=WorkOrder.objects.filter(organization=org)
        counts={key:jobs.filter(status=value).count() for key,value in WorkOrder.Status.choices}
        technicians=Technician.objects.filter(organization=org,active=True).count()
        revenue=0
        try:
            from apps.invoices.models import Invoice
            from django.db.models import Sum
            revenue=Invoice.objects.filter(organization=org,status='paid').aggregate(v=Sum('total'))['v'] or 0
        except Exception: pass
        overdue = jobs.filter(sla_due_at__lt=timezone.now()).exclude(status__in=['completed','cancelled']).count()
        return Response({'date':str(today),'jobs_today':jobs.filter(scheduled_start__date=today).count(),'unassigned':counts.get('unassigned',0),'in_progress':counts.get('in_progress',0),'completed':counts.get('completed',0),'overdue':overdue,'technicians':technicians,'paid_revenue':revenue,'status_counts':counts})

class DispatchView(APIView):
    def get(self, request):
        org=get_current_org(request)
        techs=Technician.objects.filter(organization=org,active=True).select_related('user')
        data=[]
        for tech in techs:
            jobs=WorkOrder.objects.filter(assignments__technician=tech,assignments__unassigned_at__isnull=True,organization=org).order_by('scheduled_start')[:20]
            data.append({'id':tech.id,'name':tech.user.get_full_name() or tech.user.username,'status':tech.status,'jobs':WorkOrderSerializer(jobs,many=True).data})
        unassigned=WorkOrder.objects.filter(organization=org,status=WorkOrder.Status.UNASSIGNED).exclude(assignments__unassigned_at__isnull=True)
        return Response({'technicians':data,'unassigned':WorkOrderSerializer(unassigned.distinct(),many=True).data})

class TechnicianTodayView(APIView):
    def get(self, request):
        org=get_current_org(request)
        tech=Technician.objects.filter(organization=org,user=request.user,active=True).first()
        if not tech: raise PermissionDenied('Current user is not a technician in this organization.')
        jobs=WorkOrder.objects.filter(organization=org,assignments__technician=tech,assignments__unassigned_at__isnull=True).order_by('scheduled_start')
        return Response({'technician':TechnicianSerializer(tech).data,'jobs':WorkOrderSerializer(jobs,many=True).data})
