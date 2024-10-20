from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'report'
urlpatterns = [
    path('', views.ReportCreateView.as_view(), name='report_create'),
    path('report_success/', views.ReportSuccessView.as_view(), name='report_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)