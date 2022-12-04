from django.contrib import admin
from django.urls import path
from . import views

app_name = "lifehack"
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.Login, name="login"),
    path('register/', views.Register, name="register"),
    path('logout/', views.Logout, name="logout"),

    path('profile/', views.profile, name="profile"),

    path('create-group/', views.groupCreate, name="group-create"),

    path('chat/<str:room_id>', views.chat, name="chat-room"),
    path('chat/', views.chatPage, name="chat-page"),
    path('chat/search/', views.chatSearch, name="chat-search"),
    path('audio/', views.audio, name="audio"),

    path('virtual-assistant/', views.vAssist, name="vassist"),
    path('run-assistant/', views.runAssist, name="run-assist"),
    path('audiobook/', views.audiobook, name="audiobook"),
]
