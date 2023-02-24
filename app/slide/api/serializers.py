from rest_framework import serializers
from app.histological_scanners.api.serializers import HistologicalScannersSerializer
from app.scanning.api.serializers import ScanningSerializer

from ..models import Slide, SlideLoadingState


class SlideSerializer(serializers.ModelSerializer):
    histological_scanner = HistologicalScannersSerializer(read_only=True)
    scanning = ScanningSerializer(read_only=True)

    class Meta:
        model = Slide
        fields = '__all__'


class SlideForStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ('slide_name',)


class SlideLoadingStateSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='get_state_display')
    slide = SlideForStateSerializer(read_only=True)

    class Meta:
        model = SlideLoadingState
        fields = '__all__'
