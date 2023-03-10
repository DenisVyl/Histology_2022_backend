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
        'invalid': _('ā%(value)sā value has an invalid date format. It must be '
                     'in DD.MM.YYYY format.'),
        'invalid_date': _('ā%(value)sā value has the correct format (DD.MM.YYYY) '
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
        max_length=20, verbose_name='ŠŃŠ½Š¾Š²Š½Š¾Š¹ ŠŗŠ¾Š“')
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(
        MIN_VALUE_VALIDATOR), MaxValueValidator(MAX_VALUE_VALIDATOR)], verbose_name='ŠŠ¾Š“')
    macroscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='ŠŠ¾Š“ŃŠ¾Š±Š½Š¾Šµ Š³ŠøŃŃŠ¾Š»Š¾Š³ŠøŃŠµŃŠŗŠ¾Šµ Š¾ŠæŠøŃŠ°Š½ŠøŠµ-Š¼Š°ŠŗŃŠ¾ŃŠŗŠ¾ŠæŠøŃŠµŃŠŗŠ¾Šµ Š¾ŠæŠøŃŠ°Š½ŠøŠµ')
    microscopic_description = models.TextField(max_length=CHARFIELD_DEFAULT_MAX_LENGTH, blank=True,
                                               null=True, verbose_name='ŠŠ¾Š“ŃŠ¾Š±Š½Š¾Šµ Š³ŠøŃŃŠ¾Š»Š¾Š³ŠøŃŠµŃŠŗŠ¾Šµ Š¾ŠæŠøŃŠ°Š½ŠøŠµ-Š¼ŠøŠŗŃŠ¾ŃŠŗŠ¾ŠæŠøŃŠµŃŠŗŠ¾Šµ Š¾ŠæŠøŃŠ°Š½ŠøŠµ')
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name='ŠŃŠ³Š°Š½ŠøŠ·Š°ŃŠøŃ')
    receipt_date = CustomDateField(
        blank=True, null=True, verbose_name='ŠŠ°ŃŠ° ŠæŠ¾ŃŃŃŠæŠ»ŠµŠ½ŠøŃ Š¼Š°ŃŠµŃŠøŠ°Š»Š°')
    return_date = CustomDateField(
        blank=True, null=True, verbose_name='ŠŠ°ŃŠ° Š²Š¾Š·Š²ŃŠ°ŃŠµŠ½ŠøŃ Š¼Š°ŃŠµŃŠøŠ°Š»Š°')
    receipt_employee = models.ForeignKey(Employee, related_name='recipient', on_delete=models.PROTECT,
                                         blank=True, null=True, verbose_name='Š”Š¾ŃŃŃŠ“Š½ŠøŠŗ Š¼ŠµŠ“. ŃŃŃŠµŠ¶Š“ŠµŠ½ŠøŃ, Š²ŃŠ“Š°ŃŠ°')
    return_employee = models.ForeignKey(Employee, related_name='returner', on_delete=models.PROTECT,
                                        blank=True, null=True, verbose_name='Š”Š¾ŃŃŃŠ“Š½ŠøŠŗ Š¼ŠµŠ“. ŃŃŃŠµŠ¶Š“ŠµŠ½ŠøŃ, Š²Š¾Š·Š²ŃŠ°ŃŠµŠ½ŠøŠµ')
    operator = models.ForeignKey(Employee, related_name='operator',
                                 on_delete=models.PROTECT, blank=True, null=True, verbose_name='ŠŠæŠµŃŠ°ŃŠ¾Ń')

    def __str__(self):
        return self.base_code

    class Meta:
        verbose_name = 'ŠŃŃŠ»ŠµŠ“Š¾Š²Š°Š½ŠøŠµ'
        verbose_name_plural = 'ŠŃŃŠ»ŠµŠ“Š¾Š²Š°Š½ŠøŃ'
        unique_together = ('base_code', 'year', 'organization')
