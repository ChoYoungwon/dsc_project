> [!NOTE] DSC 오픈 데이터 활용 스타트업 챌린지
> 주제 : AI 기반 도로 정비 분석 시스템
> 기간 : '24년 10~11월
> 
>필요성: 
>1. 도로 보수의 필요성 증가(기후 변화, 포트홀 증가, 관련 예산 증가)
>2. 비효율적인 도로 보수 시스템(인력 및 자원 부족, 도로 보수 탐색 차량이 한정적)
>
 활용 데이터
>1. AI HUB 고해상도 도로노면 이미지 데이터
>	1. 23년, 노면상태를 촬영한 고해상도 도로노면 이미지 데이터셋)
>2. View-T의 교통자료(노드 링크로 저장되어있음) - 22년도 전일 데이터
>	1. 설명 : 차량 gps 데이터 + 모바일 통신 데이터 + 대중교통 카드 데이터로 구성
>	2. 차종별 교통량
>	3. 평균 속도 데이터
>3. 행정안전부_상습 결빙 구간

## 1. 구현 설계
![[Pasted image 20241010194338.png]]

## 1-1. 시스템 전체 구성
![[Pasted image 20241122001354.png]]


## 2. 필요 기능
> [!NOTE] 필요 기능
> 2-1 도로 손상 부분 신고 기능
> 2-2 현재 위치 전송기능 (지도 사용)
   2-3 사진 메타데이터 이용, 신고 위치 추출(보류) 
   2-4 관리자 페이지 구성(지도, 표로 구성) 
   >   -> 우선 순위 시각화
   
(참고 자료)
[기술문서 | 네이버 지도 API v3 (navermaps.github.io)](https://navermaps.github.io/maps.js.ncp/docs/)
[[Python] 이미지 파일에서 메타데이터(Metadata) 추출하기 (tistory.com)](https://mentha2.tistory.com/270)
[AI-HUB](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71781)
[N클라우드](https://www.ncloud.com/)
[네이버 지도 API](https://navermaps.github.io/maps.js.ncp/docs/tutorial-2-Getting-Started.html)

## 3. 화면 설계
(참고)
[맨 인 블랙박스 : 영상제보하기 : SBS](https://programs.sbs.co.kr/culture/maninblackbox/report/55744)
![[Pasted image 20241108143359.png]]
![[Pasted image 20241108143419.png]]

## 4. 테이블 설계

### 4.1 Report(models.Model) : 도로 신고 테이블
| 필드명       | 타입                  | 제약조건               | 설명             |
| --------- | ------------------- | ------------------ | -------------- |
| id        | AutoField           | PK, AutoIncrement  | 기본키            |
| image     | ThumbnailImageField | -                  | 사진             |
| latitude  | FloatField          | -                  | 위도             |
| longitude | FloatField          | -                  | 경도             |
| date      | DateTimeField       | auto_now_add       | 등록일자           |
### 4.2 Priority : 신고별 우선순위
| 필드명                   | 타입            | 제약조건                         | 설명           |
| --------------------- | ------------- | ---------------------------- | ------------ |
| report                | OneToOneField | PK, on_delete=models.CASCADE | 신고페이지 기본키 참조 |
| priority              | FloatField    | -                            | 우선순위(가중치 적용) |
| link_id               | IntegerField  | -                            | 링크 아이디       |
| lane_count            | IntegerField  | -                            | 차선수          |
| average_speed         | FloatField    | -                            | 평균 속력        |
| passenger_car_traffic | IntegerField  | -                            | 일반 차량 교통량    |
| bus_traffic           | IntegerField  | -                            | 버스 교통량       |
| truck_traffic         | IntegerField  | -                            | 트럭 교통량       |
| traffic               | IntegerField  | -                            | 전체 교통량       |
| is_frozen             | IntegerField  | -                            | 결빙여부         |
| severity              | FloatField    | -                            | 심각도          |
| date                  | DateTimeField | auto_now_add                 | 등록일자         |
* 1차 정렬 : priority 기준으로 내림차순
* 2차 정렬 : date 기준으로 오름차순

## 5. URL 설계
| URL 패턴                   | 뷰 이름                                | 템플릿 파일명                    | 설명         |
| ------------------------ | ----------------------------------- | -------------------------- | ---------- |
| /                        | ReportCreateView(CreateView)        | report/main.html           | 제보페이지      |
| /enter-gps/<int:pk>/     | ReportCreateView2(FormView)         | report/enter_gps.html      | 위치 등록 페이지  |
| /maps                    | ReportMapView(TemplateView)         | report/maps.html           | 지도         |
| /report_success/<int:pk> | ReportSuccessView(DetailView)       | report_success.html        | 제보 성공      |
| /success                 | ReportSuccessView<br>(TemplateView) | report/report_success.html | 제보 등록 완료   |
| /info                    | InfoView(ListView)                  | info/info.html             | 시각호 페이지    |
| /info/<int:pk>           | InfoDetailView(DetailView)          | info/info_detail.html      | 제보별 상세 페이지 |


## 6. 필요 라이브러리
geopandas
shapely
celery
redis

## 7. 직접 넣어 줘야 할 파일
1. .env
2. info/gis_convert (용량 문제)
3. media(장고에서 자동으로 사진 파일 저장)

## 8. Mysql 스키마
##### 데이터베이스
traffic_info 

**테이블**
| road_average_speed_data |
| road_data               |

**road_data 테이블**
+-----------------------+---------------+------+-----+---------+-------+
| Field                 | Type          | Null | Key | Default | Extra |
+-----------------------+---------------+------+-----+---------+-------+
| id                    | int           | NO   | PRI | NULL    |       |
| link_id               | varchar(1000) | YES  |     | NULL    |       |
| road_grade            | varchar(50)   | YES  |     | NULL    |       |
| road_name             | varchar(255)  | YES  |     | NULL    |       |
| region                | varchar(100)  | YES  |     | NULL    |       |
| length_km             | float         | YES  |     | NULL    |       |
| lane_count            | int           | YES  |     | NULL    |       |
| total_traffic         | int           | YES  |     | NULL    |       |
| passenger_car_traffic | int           | YES  |     | NULL    |       |
| bus_traffic           | int           | YES  |     | NULL    |       |
| truck_traffic         | int           | YES  |     | NULL    |       |
| is_frozen             | tinyint(1)    | YES  |     | 0       |       |
+-----------------------+---------------+------+-----+---------+-------+
12 rows in set (0.00 sec)

**road_average_speed_data 테이블**
+---------------+---------------+------+-----+---------+-------+
| Field         | Type          | Null | Key | Default | Extra |
+---------------+---------------+------+-----+---------+-------+
| id            | int           | NO   | PRI | NULL    |       |
| link_id       | varchar(1000) | YES  |     | NULL    |       |
| average_speed | int           | YES  |     | NULL    |       |
+---------------+---------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

api 서버 테스트용

36.7875983(위도), 127.1498846(경도) : 청수 호수공원
-> 가장 가까운 링크 ID: 3010226900
    거리: 47.821220138962

postman양식
```
# 전송 url(post)
http://34.64.246.251:5000/linkStatus
# raw 데이터 양식
{
    "latitude": 36.7875983,
    "longitude": 127.1498846
}
```
