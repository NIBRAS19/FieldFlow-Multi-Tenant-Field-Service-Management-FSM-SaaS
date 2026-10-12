from rest_framework import serializers
from .models import Customer, ServiceLocation, Asset

class CustomerSerializer(serializers.ModelSerializer):
    locations_count = serializers.IntegerField(source='locations.count', read_only=True)
    class Meta: model = Customer; fields = '__all__'; read_only_fields=['organization']

class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta: model = ServiceLocation; fields='__all__'; read_only_fields=['organization']

class AssetSerializer(serializers.ModelSerializer):
    class Meta: model=Asset; fields='__all__'; read_only_fields=['organization']
