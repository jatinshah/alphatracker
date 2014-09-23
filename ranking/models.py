from django.db import models


# Create your models here.
class Stock(models.Model):
    exchange = models.CharField(max_length=5)
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.exchange + ":" + self.symbol