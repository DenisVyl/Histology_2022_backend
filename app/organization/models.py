from django.db import models

ADMIN_ORGANIZATION_CODE = 'RCUD'


class Organization(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name='Полное наименование')
    name = models.CharField(
        unique=True, max_length=200, verbose_name='Краткое наименование')
    code = models.CharField(
        unique=True, max_length=20, verbose_name='Учётный код мед. учреждения')

    def __str__(self):
        return self.code

    @property
    def is_admin_organization(self):
        return self.code == ADMIN_ORGANIZATION_CODE

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
