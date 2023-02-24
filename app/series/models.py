from django.db import models

from app.icd_03.models import Icd_03
from app.icd_10.models import Icd_10
from app.research.models import Research


CHARFIELD_DEFAULT_MAX_LENGTH = 1500


class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    main_code = models.CharField(
        max_length=20, verbose_name='Основной код (серия препаратов)')
    research = models.ForeignKey(
        Research, related_name='series', on_delete=models.CASCADE, verbose_name='Исследование')
    macroscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='Подробное гистологическое описание-макроскопическое описание')
    microscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='Подробное гистологическое описание-микроскопическое описание')
    Icd_10_code = models.ForeignKey(
        Icd_10, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Код МКБ10')
    Icd_03_code = models.ForeignKey(
        Icd_03, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Код МКБ-О-3')
    histological_diagnosis = models.TextField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True, verbose_name='Гистологический диагноз')
    number_of_slides = models.PositiveSmallIntegerField(
        blank=True, default=0, verbose_name='Количество слайдов в серии')

    def __str__(self):
        return self.main_code

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        unique_together = ('research', 'main_code')
