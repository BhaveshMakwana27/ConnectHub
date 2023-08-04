from django.contrib import admin
from django.urls import path
from Posts import views

urlpatterns = [
    path('', views.handlePosts,name='Posts'),
    path('createPost/<str:username>/', views.handlePostCreating,name='createPost'),
    path('like_post/<int:post_id>/', views.handleLikes, name='like_post'),
]
