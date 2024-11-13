from celery import shared_task
from .models import Traffic, Priority
from report.models import Report
from .gis_convert.gis_conversion import gps_to_link_id

@shared_task
def make_priority_table(report_id):
    try:
        report_instance = Report.objects.get(id=report_id)
        latitude = report_instance.latitude
        longitude = report_instance.longitude
        link_id, distance = gps_to_link_id(latitude, longitude)
        priority = None
        type = None
        traffic = None

        Priority.objects.create(
            report = report_instance,
            link_id = link_id,
            distance = distance,
            priority=priority,
            type=type,
            traffic=traffic,
        )
    except Report.DoesNotExist:
        print("Report 인스턴스가 없습니다.")

