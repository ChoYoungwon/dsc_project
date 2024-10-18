from django.db import models
from report.fields import ThumbnailImageField

class Report(models.Model):
    name = models.CharField('NAME', max_length=20)
    phone = models.CharField('PHONE', max_length=14)
    email = models.CharField('EMAIL', max_length=254)
    image = ThumbnailImageField(upload_to='report/%Y/%m')
    latitude = models.IntegerField('LATITUDE')
    longitude = models.IntegerField('LONGITUDE')
    date = models.DateField('DATE', auto_now_add=True)

    class Meta:
        ordering = ('date',)
