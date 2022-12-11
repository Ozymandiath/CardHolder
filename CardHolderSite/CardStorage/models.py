from django.db import models


class Card(models.Model):
    series = models.PositiveIntegerField(verbose_name="Серия")
    number = models.CharField(max_length=20, verbose_name="Номер")
    release_date = models.DateTimeField(verbose_name="Дата создания")
    end_date = models.DateTimeField(verbose_name="Дата окончания активации")
    status = models.BooleanField(verbose_name="Статус")


class CardTransaction(models.Model):
    card_id = models.ForeignKey("Card", on_delete=models.CASCADE, verbose_name="Карта")
    date_use = models.DateTimeField(verbose_name="Дата использования")
    amount = models.IntegerField(verbose_name="Сумма")
