from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ExternalUploadFileSerializer
from ..lib.uploading_files import CustomTemporaryFileUploadHandler


class ExternalUploadFileVew(APIView):
    def initialize_request(self, request, *args, **kwargs):
        request.upload_handlers = [CustomTemporaryFileUploadHandler(request)]
        return super().initialize_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        posts_serializer = ExternalUploadFileSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
