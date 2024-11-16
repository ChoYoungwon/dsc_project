from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),
    path('<int:pk>/', views.InfoDetailView.as_view(), name='detail'),
]