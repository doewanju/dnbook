from django.urls import path
from . import views

urlpatterns = [
    path('listmessage/', views.listMessage, name='listMessage'),
    path('detail/<int:message_id>', views.viewMessage, name='viewMessage'),
    path('send/<int:user_id>', views.sendMessage, name='sendMessage'),
    path('chat/<int:user_id>', views.chat, name='chat'),
]