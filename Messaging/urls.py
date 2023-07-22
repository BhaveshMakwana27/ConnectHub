from django.contrib import admin
from django.urls import path
from Messaging import views

urlpatterns = [
    path('', views.handleMessages,name='Message'),
]
