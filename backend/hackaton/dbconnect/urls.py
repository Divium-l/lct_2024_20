from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.connect_to_db, name='connect_to_db'),
    path('use-connection/', views.use_saved_connection, name='use_saved_connection'),
    path('scanResult/', views.get_columns, name='scanResult'),
    path('updateScanResult', views.update_columns, name='updateScanResult'),
    path('getSavedColumns/', views.get_saved_columns, name='getSavedColumns'),
]