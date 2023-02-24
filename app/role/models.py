from django.db import models


class Role(models.Model):
    name = models.CharField(unique=True,
                            max_length=20, verbose_name='Название полномочия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
