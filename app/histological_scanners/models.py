from django.db import models
from app.organization.models import Organization


CHARFIELD_DEFAULT_MAX_LENGTH = 1500


class HistologicalScanners(models.Model):
    index = models.PositiveIntegerField(
        unique=True, verbose_name='Порядковый номер')
    full_name = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True, verbose_name='Полное название')
    code = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True, verbose_name='Дополнительный код')
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Организация')

    class Meta:
        verbose_name = 'Гистологический сканер'
        verbose_name_plural = 'Гистологические сканеры'

    def __str__(self):
        return self.full_name
