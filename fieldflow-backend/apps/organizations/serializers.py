from rest_framework import serializers
from .models import Organization, Membership
from apps.accounts.serializers import UserSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['owner','slug']

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Membership
        fields = ['id','organization','user','user_id','role','active','joined_at']
        read_only_fields = ['organization','joined_at']
