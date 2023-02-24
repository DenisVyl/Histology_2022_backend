from rest_framework import serializers

from ..models import Scanning


class ScanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scanning
        fields = '__all__'
