from django.conf.urls import url, include
from django.contrib import admin

from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^table/$', views.get_excel),
    url(r'^post$', views.form_action),
    url(r'^table/(?P<table_id>[0-9]+)$', views.get_excel),
    url(r'^download/$', views.get_file),
    url(r'^download/(?P<file>.+)$', views.download_excel)
]
