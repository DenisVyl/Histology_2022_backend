from django.db import models

CHARFIELD_DEFAULT_MAX_LENGTH = 1500


class Scanning(models.Model):
    index = models.PositiveIntegerField(
        unique=True, verbose_name='Порядковый номер')
    value = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True, verbose_name='Значение')

    class Meta:
        verbose_name = 'Разрешение сканирования'
        verbose_name_plural = 'Разрешения сканирования'

    def __str__(self):
        return self.value
