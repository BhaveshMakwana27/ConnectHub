from django.contrib import admin
from django.urls import path
from Followers import views

urlpatterns = [
    path('', views.handleFollowers,name='Followers'),
    path('profiles_list/',views.list_profiles,name='ListProfiles'),
    path('visit_profile/<str:uname>/',views.visit_profile,name='ListProfiles')
]
