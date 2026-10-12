from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Invoice, InvoiceItem, Payment
from .serializers import InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer
from .services import next_invoice_no,recalc
from apps.organizations.services import get_current_org
from apps.customers.models import Customer

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class=InvoiceSerializer
    search_fields=['invoice_no','customer__name','customer__company']
    ordering_fields=['issue_date','due_date','total','status']
    def get_org(self): return get_current_org(self.request)
    def get_queryset(self): return Invoice.objects.filter(organization=self.get_org()).select_related('customer','work_order').prefetch_related('items','payments')
    def perform_create(self, serializer):
        org=self.get_org(); customer_id=self.request.data.get('customer')
        if not Customer.objects.filter(id=customer_id,organization=org).exists(): raise ValidationError({'customer':'Invalid customer.'})
        invoice=serializer.save(organization=org,invoice_no=next_invoice_no(org)); recalc(invoice)
    @action(detail=True,methods=['post'])
    def items(self,request,pk=None):
        invoice=self.get_object(); qty=request.data.get('quantity',1); price=request.data.get('unit_price',0); item=InvoiceItem.objects.create(invoice=invoice,description=request.data.get('description','Service'),quantity=qty,unit_price=price,amount=qty*price,sort_order=request.data.get('sort_order',0)); recalc(invoice); return Response(InvoiceItemSerializer(item).data,status=201)
    @action(detail=True,methods=['post'])
    def payments(self,request,pk=None):
        invoice=self.get_object(); payment=Payment.objects.create(invoice=invoice,amount=request.data.get('amount'),method=request.data.get('method','bank_transfer'),reference=request.data.get('reference','')); paid=sum(x.amount for x in invoice.payments.all()); invoice.status=Invoice.Status.PAID if paid>=invoice.total else Invoice.Status.PARTIAL; invoice.save(update_fields=['status']); return Response(PaymentSerializer(payment).data,status=201)
    @action(detail=True,methods=['post'])
    def mark_paid(self,request,pk=None):
        invoice=self.get_object(); invoice.status=Invoice.Status.PAID; invoice.save(update_fields=['status']); Payment.objects.create(invoice=invoice,amount=max(invoice.total-sum(x.amount for x in invoice.payments.all()),0),method=request.data.get('method','manual'),reference=request.data.get('reference','')); return Response(self.get_serializer(invoice).data)
