from rest_framework import serializers

from ..models import Icd_03


class Icd_03Serializer(serializers.ModelSerializer):
    class Meta:
        model = Icd_03
        fields = '__all__'
