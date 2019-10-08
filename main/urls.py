from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('signup/boss', views.boss, name='boss'),
    path('signup/normal', views.normal, name='normal'),
    path('signup/boss/bossbook', views.bossbook, name='bossbook'),
]