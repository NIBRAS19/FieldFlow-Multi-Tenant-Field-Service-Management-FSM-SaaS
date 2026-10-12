from decimal import Decimal
from django.db import transaction
from .models import Invoice, InvoiceItem

def next_invoice_no(org):
    last=Invoice.objects.filter(organization=org).order_by('-id').values_list('invoice_no',flat=True).first()
    n=1
    if last:
        try:n=int(str(last).split('-')[-1])+1
        except Exception:n=Invoice.objects.filter(organization=org).count()+1
    return f'INV-{n:08d}'

def recalc(invoice):
    subtotal=sum((x.amount for x in invoice.items.all()), Decimal('0'))
    total=subtotal - invoice.discount + invoice.tax
    invoice.subtotal=subtotal; invoice.total=total; invoice.save(update_fields=['subtotal','total'])
    return invoice
