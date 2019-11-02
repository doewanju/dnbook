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
    path('ranking/', views.ranking, name='ranking'),
    path('info/', views.info, name='info'),
    path('stamppush/', views.stamppush, name='stamppush'),
    path('del_user/', views.del_user, name='del_user'),
    path('change_pwd/',views.change_pwd, name='change_pwd'),
    path('addstore/', views.addstore, name='addstore'),
]