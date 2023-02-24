from rest_framework import serializers

from ..models import Series
from app.icd_10.api.serializers import Icd_10Serializer
from app.icd_03.api.serializers import Icd_03Serializer
from app.slide.api.serializers import SlideSerializer


class SeriesSerializer(serializers.ModelSerializer):
    Icd_10_code = Icd_10Serializer()
    Icd_03_code = Icd_03Serializer()

    class Meta:
        model = Series
        fields = '__all__'


class SeriesSlidesSerializer(SeriesSerializer):
    slides = SlideSerializer(many=True)
