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
<<<<<<< HEAD
    path('change_pwd/',views.change_pwd, name='change_pwd'),
    path('addstore/', views.addstore, name='addstore'),
=======
    path('user_change/',views.user_change, name='user_change'),
>>>>>>> d9be01e1c12f6a4c98b50b71b8a4e2c69ae301b8
]