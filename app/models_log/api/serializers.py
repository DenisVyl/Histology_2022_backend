from rest_framework import serializers
from models_logging.models import Change


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = '__all__'
