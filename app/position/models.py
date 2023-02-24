from django.db import models


class Position(models.Model):
    name = models.CharField(unique=True,
                            max_length=20, verbose_name='Название должности')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
