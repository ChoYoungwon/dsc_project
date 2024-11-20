import requests
from django.conf import settings
from report.models import Report
import os
import json

def link_id_api(latitude, longitude):
    try:
        url = "http://34.64.246.251:5000/linkStatus"
        data = {
            "latitude": latitude,
            "longitude": longitude
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            data = response.json()
            print("link_id 받은 데이터:", data)
            return data
        else:
            print(f"link_id 요청 실패: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)

# def yolo_api(report_id):
#     try:
#         url = 'http://43.203.198.73:5000/predict'
#         report_instance = Report.objects.get(id=report_id)
#         image_path = os.path.join(settings.MEDIA_ROOT, report_instance.image.path)
#         print("이미지 주소: ", image_path)
#         with open(image_path, 'rb') as image_file:
#             files = {'file': image_file}
#             response = requests.post(url, files=files)
#
#         if response.status_code == 200:
#             data = response.json()
#             print("yolo 받은 데이터:", data)
#             return data
#         else:
#             print(f"yolo 요청 실패: {response.status_code}")
#
#     except requests.exceptions.RequestException as e:
#         print("Error fetching data:", e)

def yolo_api(report_id):
    try:
        url = 'http://43.202.64.33:5000/predict'
        report_instance = Report.objects.get(id=report_id)

        if not report_instance.image:
            print("Error: No image associated with this report instance.")
            return

        image_path = report_instance.image.path
        print("이미지 주소: ", image_path)

        if not os.path.exists(image_path):
            print("Error: Image file does not exist at the specified path.")
            return

        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            print("YOLO 받은 데이터:", data)
            return data
        else:
            print(f"YOLO 요청 실패: {response.status_code}, 응답 내용: {response.text}")

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    except Report.DoesNotExist:
        print("Error: Report instance does not exist.")
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == '__main__':
    link_id_api(36.7875983,127.1498846)
    yolo_data = yolo_api(75)