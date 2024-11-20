from django.contrib import admin

from .models import Priority, Traffic

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('report', 'priority', 'link_id', 'lane_count', 'average_speed', 'passenger_car_traffic', 'bus_traffic', 'truck_traffic', 'traffic', 'is_frozen', 'severity')

@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ('link_id',)