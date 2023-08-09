from django.contrib import admin
from django.urls import path,include
from Posts import views 
urlpatterns = [
    path('', views.handlePosts,name='Posts'),
    path('createPost/<str:username>/', views.handlePostCreating,name='createPost'),
    path('like_post/<int:post_id>/', views.handleLikes, name='like_post'),
    path('postComments/',views.handleComments,name='PostComments'),
    path('search/',views.handleSearch,name='Search'),
    path('profile_posts/<str:uname>',views.handleProfilePosts,name='ProfilePosts'),
]
