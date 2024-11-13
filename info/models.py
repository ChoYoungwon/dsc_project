from django.db import models
from report.models import Report

class Traffic(models.Model):
    link_id = models.IntegerField(null=True, blank=True)

class Priority(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='priority', primary_key=True)
    # link_id = models.ForeignKey(Traffic, null=True, blank=True, on_delete=models.SET_NULL, related_name='link_id')
    link_id = models.IntegerField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    traffic = models.IntegerField(null=True, blank=True)
