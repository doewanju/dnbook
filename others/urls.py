from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board, name='board'),
    path('guide/', views.guide, name='guide'),
    path('detail/<int:culture_id>', views.detail, name='culturedetail'),
]