from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.shopping),
    url(r'^ajax_send_pin/$', views.ajax_send_pin)
]