from django.db import models
from apps.organizations.models import Organization
from apps.customers.models import Customer
from apps.operations.models import WorkOrder

class Invoice(models.Model):
    class Status(models.TextChoices): DRAFT='draft','Draft'; SENT='sent','Sent'; PARTIAL='partial','Partially Paid'; PAID='paid','Paid'; OVERDUE='overdue','Overdue'; VOID='void','Void'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='invoices')
    invoice_no=models.CharField(max_length=50)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='invoices')
    work_order=models.ForeignKey(WorkOrder,on_delete=models.SET_NULL,null=True,blank=True,related_name='invoices')
    issue_date=models.DateField(auto_now_add=True)
    due_date=models.DateField(null=True,blank=True)
    subtotal=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    tax=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    discount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['organization','invoice_no'],name='uniq_invoice_org')]

class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='items')
    description=models.CharField(max_length=255)
    quantity=models.DecimalField(max_digits=12,decimal_places=2,default=1)
    unit_price=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    amount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    sort_order=models.PositiveIntegerField(default=0)

class Payment(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='payments')
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    method=models.CharField(max_length=50,default='bank_transfer')
    reference=models.CharField(max_length=120,blank=True)
    paid_at=models.DateTimeField(auto_now_add=True)
