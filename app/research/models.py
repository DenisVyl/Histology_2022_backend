import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.utils.regex_helper import _lazy_re_compile
from django.core.validators import MinValueValidator, MaxValueValidator

from app.organization.models import Organization
from app.employee.models import Employee

MIN_VALUE_VALIDATOR = 1990
MAX_VALUE_VALIDATOR = 2021
CHARFIELD_DEFAULT_MAX_LENGTH = 1500


class CustomDateField(models.DateField):
    date_re = _lazy_re_compile(
        r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})$'
    )
    default_error_messages = {
        'invalid': _('“%(value)s” value has an invalid date format. It must be '
                     'in DD.MM.YYYY format.'),
        'invalid_date': _('“%(value)s” value has the correct format (DD.MM.YYYY) '
                          'but it is an invalid date.'),
    }

    def _parse_date(self, value):
        """Parse a string and return a datetime.date.

        Raise ValueError if the input is well formatted but not a valid date.
        Return None if the input isn't well formatted.
        """
        match = self.date_re.match(value)
        if match:
            kw = {k: int(v) for k, v in match.groupdict().items()}
            return datetime.date(**kw)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            if settings.USE_TZ and timezone.is_aware(value):
                # Convert aware datetimes to the default time zone
                # before casting them to dates (#17742).
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_naive(value, default_timezone)
            return value.date()
        if isinstance(value, datetime.date):
            return value

        try:
            parsed = self._parse_date(value)
            if parsed is not None:
                return parsed
        except ValueError:
            raise exceptions.ValidationError(
                self.error_messages['invalid_date'],
                code='invalid_date',
                params={'value': value},
            )

        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )


class Research(models.Model):
    research_id = models.AutoField(primary_key=True)
    base_code = models.CharField(
        max_length=20, verbose_name='Основной код')
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(
        MIN_VALUE_VALIDATOR), MaxValueValidator(MAX_VALUE_VALIDATOR)], verbose_name='Год')
    macroscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='Подробное гистологическое описание-макроскопическое описание')
    microscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='Подробное гистологическое описание-микроскопическое описание')
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name='Организация')
    receipt_date = CustomDateField(
        blank=True, null=True, verbose_name='Дата поступления материала')
    return_date = CustomDateField(
        blank=True, null=True, verbose_name='Дата возвращения материала')
    receipt_employee = models.ForeignKey(Employee, related_name='recipient', on_delete=models.PROTECT,
                                         blank=True, null=True, verbose_name='Сотрудник мед. учреждения, выдача')
    return_employee = models.ForeignKey(Employee, related_name='returner', on_delete=models.PROTECT,
                                        blank=True, null=True, verbose_name='Сотрудник мед. учреждения, возвращение')
    operator = models.ForeignKey(Employee, related_name='operator',
                                 on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оператор')

    def __str__(self):
        return self.base_code

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'
        unique_together = ('base_code', 'year', 'organization')
