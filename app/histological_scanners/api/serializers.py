from rest_framework import serializers
from ..models import HistologicalScanners


class HistologicalScannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistologicalScanners
        fields = '__all__'
