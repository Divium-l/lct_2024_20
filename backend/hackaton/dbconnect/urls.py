from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.connect_to_db, name='connect_to_db'),
    path('use-connection/', views.use_saved_connection, name='use_saved_connection'),
    path('get-columns/', views.get_columns, name='get_columns'),
    path('update-columns/', views.update_columns, name='update_columns'),
    path('get-saved-columns/', views.get_saved_columns, name='get_saved_columns'),
]