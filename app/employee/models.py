from django.db import models

from django.contrib.auth.models import User
from app.organization.models import Organization
from app.position.models import Position
from app.role.models import Role


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Логин')
    surname = models.CharField(
        max_length=20, verbose_name='Фамилия')
    first_name = models.CharField(
        max_length=20, verbose_name='Имя')
    patronymic = models.CharField(
        max_length=20, blank=True, default='', verbose_name='Отчество')
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Организация')
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Должность')
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Роль')
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        unique_together = ('user', 'surname', 'first_name',
                           'patronymic', 'organization', 'position')
