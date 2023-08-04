from django.contrib import admin
from django.urls import path
from Messaging import views

urlpatterns = [
    path('', views.handleMessageRoomList,name='MessageRoomList'),
    path('do_message/<str:room_name>/', views.handleMessages,name='Message'),
]
