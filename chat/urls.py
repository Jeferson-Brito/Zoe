from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/send/', views.api_chat_message, name='api_chat_message'),
]
