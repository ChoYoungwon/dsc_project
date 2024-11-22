from django.db import models
from django.forms import IntegerField
from report.models import Report

class Traffic(models.Model):
    link_id = models.IntegerField(null=True, blank=True)

class Priority(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='priority', primary_key=True)
    priority = models.FloatField(null=True, blank=True)
    link_id = models.CharField(max_length=255, null=True, blank=True)
    lane_count = models.IntegerField(null=True, blank=True)
    average_speed = models.FloatField(null=True, blank=True)
    passenger_car_traffic = models.IntegerField(null=True, blank=True)
    bus_traffic = models.IntegerField(null=True, blank=True)
    truck_traffic = models.IntegerField(null=True, blank=True)
    traffic = models.IntegerField(null=True, blank=True)
    is_frozen = models.IntegerField(null=True, blank=True)
    severity = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-priority', 'date')
