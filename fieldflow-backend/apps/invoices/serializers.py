from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta: model=InvoiceItem; fields='__all__'; read_only_fields=['amount']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model=Payment; fields='__all__'; read_only_fields=['paid_at']
class InvoiceSerializer(serializers.ModelSerializer):
    items=InvoiceItemSerializer(many=True,read_only=True)
    payments=PaymentSerializer(many=True,read_only=True)
    class Meta: model=Invoice; fields='__all__'; read_only_fields=['organization','invoice_no','issue_date','subtotal','total']
