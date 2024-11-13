from django.contrib import admin

from report.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'latitude', 'longitude', 'date')
    list_filter = ('date',)