from datetime import datetime
from rest_framework import serializers
from django.utils import timezone
from ..lib.uploading_files import upload_files
from ..models import CHARFIELD_DEFAULT_MAX_LENGTH


class ExternalUploadFileSerializer(serializers.Serializer):
    files = serializers.ListField()
    email = serializers.EmailField()
    description = serializers.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH)
    datetime = serializers.IntegerField()

    def create(self, validated_data):
        files = validated_data.get('files')
        email = validated_data.get('email')
        description = validated_data.get('description')

        upload_str_timestamp = validated_data.get('datetime')
        upload_timestamp = int(upload_str_timestamp)
        upload_datetime = datetime.fromtimestamp(
            upload_timestamp, tz=timezone.utc)

        upload_files(files, email,
                     description, upload_datetime)

        return validated_data
