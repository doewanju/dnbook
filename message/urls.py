from django.urls import path
from . import views

urlpatterns = [
    path('listmessage/', views.listMessage, name='listMessage'),
    path('chat/<int:user_id>', views.chat, name='chat'),
]