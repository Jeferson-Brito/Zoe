from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('session/<uuid:session_id>/', views.chat_view, name='chat_session'),
    path('new/', views.new_session_view, name='new_session'),
    path('delete/<uuid:session_id>/', views.delete_session_view, name='delete_session'),
    path('api/sessions/', views.list_sessions_api, name='list_sessions'),
    path('api/send/', views.api_chat_message, name='api_chat_message'),
]
