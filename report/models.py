from django.db import models
from report.fields import ThumbnailImageField

class Report(models.Model):
    image = ThumbnailImageField(upload_to='report/%Y/%m', null=True, blank=True)
    latitude = models.FloatField('LATITUDE', null=True, blank=True)
    longitude = models.FloatField('LONGITUDE', null=True, blank=True)
    date = models.DateField('DATE', auto_now_add=True)
    class Meta:
        ordering = ('date',)
