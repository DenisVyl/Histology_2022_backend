from rest_framework import serializers
from ..models import Employee
from app.organization.api.serializers import OrganizationSerializer
from app.role.api.serializers import RoleSerializer
from app.position.api.serializers import PositionSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    organization = OrganizationSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
