from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_gps_info(image):
    # 이미지 파일에서 EXIF 데이터를 추출해 GPS 정보를 반환.
    try:
        img = Image.open(image)
        exif_data = img._getexif()

        if not exif_data:
            return None

        # EXIF 데이터에서 GPSInfo 추출
        gps_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                for key in value:
                    gps_tag = GPSTAGS.get(key, key)
                    gps_info[gps_tag] = value[key]

        # GPS 좌표 변환
        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            latitude = convert_to_degrees(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
            longitude = convert_to_degrees(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
            return latitude, longitude
        return None
    except Exception as e:
        print(f"Error extracting GPS info: {e}")
        return None

def convert_to_degrees(value, ref):
    # GPS 좌표를 도(degree) 단위로 변환.
    d, m, s = value
    degrees = d + (m / 60.0) + (s / 3600.0)
    if ref in ['S', 'W']:  # 남반구나 서반구의 경우 음수로 변환
        degrees *= -1
    return degrees