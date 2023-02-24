import os
from celery import shared_task
from django.conf import settings
from django.core.files import File
from django.core.files import temp as tempfile
from django.core.files.uploadedfile import UploadedFile
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from app.external_upload_file.models import ExternalUploadFile


class CustomTemporaryUploadedFile(UploadedFile):
    def __init__(self, name, content_type, size, charset, content_type_extra=None):
        _, ext = os.path.splitext(name)
        file = tempfile.NamedTemporaryFile(
            suffix='.upload' + ext, dir=settings.FILE_UPLOAD_TEMP_DIR, delete=False)
        super().__init__(file, name, content_type, size, charset, content_type_extra)

    def temporary_file_path(self):
        """Return the full path of this file."""
        return self.file.name


class CustomTemporaryFileUploadHandler(TemporaryFileUploadHandler):
    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super().new_file(*args, **kwargs)
        self.file = CustomTemporaryUploadedFile(
            self.file_name, self.content_type, 0, self.charset, self.content_type_extra)


@shared_task
def upload_file(file_name, tmp_file_path, email, description, upload_datetime):
    created_file = ExternalUploadFile(email=email,
                                      description=description,
                                      upload_datetime=upload_datetime
                                      )

    with open(tmp_file_path, 'rb') as tmp_file:
        django_file = File(tmp_file)
        created_file.file.save(file_name, django_file, save=True)

        django_file.close()

    os.remove(tmp_file_path)


def upload_files(files, email, description, upload_datetime):
    for file in files:
        file_name = file.name
        tmp_file_path = file.temporary_file_path()
        file.close()

        upload_file.delay(file_name, tmp_file_path, email,
                          description, upload_datetime)
