from rest_framework import serializers

from ..models import Icd_10


class Icd_10Serializer(serializers.ModelSerializer):
    class Meta:
        model = Icd_10
        fields = '__all__'
