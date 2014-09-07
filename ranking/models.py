from django.db import models


# Create your models here.
class Stock(models.Model):
    exchange = models.CharField(max_length=5)
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)


# class EODHistoricalPrices(models.Model):
#     pass
#
#
# class Performance(models.Model):
#     pass