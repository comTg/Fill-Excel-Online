from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^table/$', views.get_excel),
    url(r'^post$',views.form_action),
    url(r'^table/(?P<article_id>[0-9]+)$',views.article_page)
]