from celery import shared_task
from .models import Traffic, Priority
from report.models import Report
from .gis_convert.gis_conversion import gps_to_link_id
import requests
import os
from django.conf import settings

@shared_task
def make_priority_table(report_id):
    try:
        report_instance = Report.objects.get(id=report_id)
        latitude = report_instance.latitude
        longitude = report_instance.longitude
        link_id, distance = gps_to_link_id(latitude, longitude)
        priority = None
        type = "-1"

        # try:
        #     url = 'http://13.125.218.18:5000/predict'
        #     image_path = os.path.join(settings.MEDIA_ROOT, report_instance.image.path)
        #
        #     with open(image_path, 'rb') as image_file:
        #         files = {'file': image_file}
        #         response = requests.post(url, files=files)
        #
        #     if response.status_code == 200:
        #         json_data = response.json()
        #         if json_data:
        #             type = "2"
        #     else:
        #         print(f"Unexpected status code: {response.status_code}")
        #
        # except requests.exceptions.RequestException as e:
        #     print("Error fetching data:", e)

        Priority.objects.create(
            report = report_instance,
            link_id = link_id,
            distance = distance,
            priority=priority,
            type=type,
            traffic=None,
        )
    except Report.DoesNotExist:
        print("Report 인스턴스가 없습니다.")

