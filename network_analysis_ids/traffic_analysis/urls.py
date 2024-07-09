from django.urls import path
from network_analysis_ids import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('results/<int:pcap_file_id>/', views.results_view, name='results'),
    path('analyze/<int:pcap_file_id>/', views.analyze_traffic, name='analyze_traffic'),
    path('task/<str:task_id>/', views.task_status, name='task_status'),
]