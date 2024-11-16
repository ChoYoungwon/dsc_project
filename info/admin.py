from django.contrib import admin

from .models import Priority, Traffic

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('report', 'link_id', 'distance', 'priority', 'type', 'traffic', 'date')

@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ('link_id',)