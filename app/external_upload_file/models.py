import os
import re
from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from app.lib.constants import CHARFIELD_DEFAULT_MAX_LENGTH

MEDIA_ROOT = str(settings.MEDIA_ROOT)


class ExternalUploadFile(models.Model):
    def _upload_to(instance, filename):
        datetime_isoformat = instance.upload_datetime
        datetime_isoformat_for_windows = re.sub(':', '.', datetime_isoformat)

        return f'{instance.email}/{datetime_isoformat_for_windows}/{filename}'

    file = models.FileField(upload_to=_upload_to)
    email = models.EmailField(blank=True, null=True)
    description = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True)
    upload_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        datetime_isoformat = self.upload_datetime
        datetime_isoformat_for_windows = re.sub(':', '.', datetime_isoformat)

        FOLDER = MEDIA_ROOT + '/' + \
            self.email + '/' + datetime_isoformat_for_windows

        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)

        path_to_txt = FOLDER + os.sep + 'Описание.txt'

        if not os.path.exists(path_to_txt):
            with open(path_to_txt, 'w') as wf:
                wf.write(f'{self.email}\n{self.description}')

        message_now = str(self.upload_datetime)
        message_text = f'{message_now}, Загружен новый файл от {self.email}'
        print(f'Sending {message_text}')
        '''send_mail(
            subject=message_text,
            message=message_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )'''

        super(ExternalUploadFile, self).save(*args, **kwargs)
