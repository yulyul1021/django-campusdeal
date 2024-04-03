from . import views
from django.urls import path

# app_name = 'chat'

urlpatterns = [
    path('', views.create_room, name='create_room'),
    path('<str:room_name>/<str:username>/', views.message_view, name='room'),
]