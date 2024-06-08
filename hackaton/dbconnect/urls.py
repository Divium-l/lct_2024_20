from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.connect_to_db, name='connect_to_db'),
]