from django.contrib import admin
from TSBserv import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^updateuser/$', views.UpdateUser, name='UpdateUser')
]
