from django.db import models

from django.utils.translation import gettext_lazy as _
from app.series.models import Series
from app.icd_03.models import Icd_03
from app.icd_10.models import Icd_10
from app.scanning.models import Scanning
from app.histological_scanners.models import HistologicalScanners
from app.lib.constants import CHARFIELD_DEFAULT_MAX_LENGTH



class Slide(models.Model):
    slide_id = models.AutoField(primary_key=True)
    slide_name = models.CharField(unique=True,
                                  max_length=CHARFIELD_DEFAULT_MAX_LENGTH, verbose_name='Файл')
    source_slide_name = models.CharField(
        max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True, null=True, verbose_name='Исходное имя')
    series = models.ForeignKey(
        Series, related_name='slides', on_delete=models.CASCADE, verbose_name='Серия')
    Icd_10_code = models.ForeignKey(
        Icd_10, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Код МКБ10')
    Icd_03_code = models.ForeignKey(
        Icd_03, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Код МКБ-О-3')
    scanning = models.ForeignKey(
        Scanning, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Разрешение сканирования')
    histological_scanner = models.ForeignKey(
        HistologicalScanners, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Сканер')
    additional_code = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Дополнительный код')
    index_number = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name='Порядковый номер слайда в серии')
    smb_path = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH,
                                blank=True, null=True, verbose_name='Samba путь')
    path = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH,
                            blank=True, null=True, verbose_name='Путь')
    focus = models.BooleanField(default=False, verbose_name='Фокус')

    def __str__(self):
        return self.slide_name

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        unique_together = ('series', 'index_number',
                           'histological_scanner', 'scanning')


class SlideLoadingState(models.Model):
    class States(models.IntegerChoices):
        QUEUED = 0, _('В очереди')
        LOADING = 1, _('Загружается')
        READY = 2, _('Загружен')
        ERROR = 3, _('Ошибка')

    slide = models.OneToOneField(
        Slide,
        verbose_name='Слайд',
        on_delete=models.CASCADE,
    )
    state = models.IntegerField(
        default=States.QUEUED, choices=States.choices, verbose_name=_('Состояние'))
    percentage = models.PositiveSmallIntegerField(
        default=0,  verbose_name='Процент загрузки')
    error = models.CharField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH,
                             blank=True, null=True, verbose_name='Возможная ошибка')

    def __str__(self):
        return f'{self.slide.slide_name} - {self.get_state_display()}'
