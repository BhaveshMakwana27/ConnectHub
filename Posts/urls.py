from django.contrib import admin
from django.urls import path
from Posts import views

urlpatterns = [
    path('', views.handlePosts,name='Posts'),
]
