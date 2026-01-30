from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('knowledge/delete/<int:pk>/', views.delete_knowledge, name='delete_knowledge'),
]
