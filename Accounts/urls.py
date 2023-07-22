from django.contrib import admin
from django.urls import path
from Accounts import views

urlpatterns = [
    path('', views.handleAccount,name='Account'),
    path('signin/', views.handleSignin,name='Signin'),
    path('login/', views.handleLogin,name='Login'),
    path('logout/', views.handleLogout,name='Logout'),
    path('profile/<str:uname>/', views.userProfileHandle,name='ViewProdile'),
    path('edit-profile/<str:uname>/', views.editProfileHandle,name='EditProfile'),
]
