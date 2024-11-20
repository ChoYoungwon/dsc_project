# from .gis_convert.gis_conversion import gps_to_link_id
from celery import shared_task
from .models import Traffic, Priority
from .api_call import link_id_api, yolo_api
from report.models import Report

@shared_task
def make_priority_table(report_id):
    try:
        report_instance = Report.objects.get(id=report_id)
        latitude = report_instance.latitude
        longitude = report_instance.longitude
        data_link = link_id_api(latitude, longitude)
        print(report_id)
        data_yolo = yolo_api(report_id)
        print("yolo 전송 데이터 : ", data_yolo)

        link_id = None
        lane_count = None
        average_speed = None
        passenger_car_traffic = None
        bus_traffic = None
        truck_traffic = None
        traffic = None
        is_frozen = None
        severity = None

        if data_yolo:
            severity = float(data_yolo.get('result'))

        if data_link.get("result") == "ok":
            link_id = data_link.get("link_id")
            lane_count = int(data_link.get("lane_count"))
            average_speed = float(data_link.get("average_speed"))
            passenger_car_traffic = int(data_link.get("passenger_car_traffic"))
            bus_traffic = int(data_link.get("bus_traffic"))
            truck_traffic = int(data_link.get("truck_traffic"))
            is_frozen = int(data_link.get("is_frozen"))

        # 최종 우선순위 연산
        if data_link.get("result") == "ok":
            if is_frozen:
                priority = severity * (((1 * passenger_car_traffic) + (100 * bus_traffic) + (truck_traffic * 270)) * average_speed) * 0.35 / lane_count * 1.2
                traffic = passenger_car_traffic * average_speed + bus_traffic + truck_traffic
            else:
                priority = severity * (((1 * passenger_car_traffic) + (100 * bus_traffic) + (truck_traffic * 270)) * average_speed) * 0.35 / lane_count
                traffic = passenger_car_traffic * average_speed + bus_traffic + truck_traffic
        else:
            link_id = data_link.get("link_id")
            priority = severity
            average_speed = -1

        Priority.objects.create(
            report = report_instance,
            priority = priority,
            link_id = link_id,
            lane_count = lane_count,
            average_speed = average_speed,
            passenger_car_traffic = passenger_car_traffic,
            bus_traffic = bus_traffic,
            truck_traffic = truck_traffic,
            traffic = traffic,
            is_frozen = is_frozen,
            severity = severity,
        )

    except Report.DoesNotExist:
        print("Report 인스턴스가 없습니다.")

