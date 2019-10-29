from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board, name='board'),
    path('guide/', views.guide, name='guide'),
    path('detail/<int:culture_id>', views.detail, name='culturedetail'),
    path('commentcreate/<int:culture_id>', views.commentcreate, name='commentcreate'),
    path('commentdelete/<int:comment_id>', views.commentdelete, name='commentdelete'),
    path('new/', views.new, name='new'),
    path('boardcreate/', views.boardcreate, name='boardcreate'),
]