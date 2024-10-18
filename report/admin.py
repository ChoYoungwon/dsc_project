from django.contrib import admin

from report.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'image', 'latitude', 'longitude', 'date')
    list_filter = ('date',)