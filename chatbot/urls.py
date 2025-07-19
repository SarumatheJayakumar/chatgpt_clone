from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('upload/', views.upload_document, name='upload_document'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
