from rest_framework import serializers
from ..models import Research
from app.series.api.serializers import SeriesSlidesSerializer


class ResearchSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    receipt_employee = serializers.StringRelatedField()
    return_employee = serializers.StringRelatedField()
    operator = serializers.StringRelatedField()

    class Meta:
        model = Research
        fields = '__all__'


class ResearchSeriesSerializer(ResearchSerializer):
    series = SeriesSlidesSerializer(many=True)
