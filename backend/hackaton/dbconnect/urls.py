import os
import time

from django.urls import path
from . import views
from .celery_app import learn_model
from .views import saved_data
import threading
import redis

urlpatterns = [
    path('connect/', views.connect_to_db, name='connect_to_db'),
    path('use-connection/', views.use_saved_connection, name='use_saved_connection'),
    path('scanResult/', views.get_columns, name='scanResult'),
    path('updateScanResult', views.update_columns, name='updateScanResult'),
    path('getSavedColumns/', views.get_saved_columns, name='getSavedColumns'),
    path('startMasking/', views.depersonalize_data, name='startMasking'),
]


def infinite_learn(saved_data):
    while True:
        time.sleep(43200)
        learn_model(saved_data)
def r():
    r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))
    t = r.get("learning")
    if t is not None:
        return
    else:
        t = threading.Thread(target=infinite_learn, args=(saved_data,), daemon=True)
        r.set("learning", "true".encode())
        t.start()
r()