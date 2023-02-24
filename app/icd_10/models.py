from django.db import models

CHARFIELD_DEFAULT_MAX_LENGTH = 1500


class Icd_10(models.Model):
    code = models.CharField(unique=True, max_length=10,
                            verbose_name='Код', default='')
    diagnosis = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, verbose_name='Диагноз', default='')
    parent = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Родитель', default='')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Справочник МКБ-10'
