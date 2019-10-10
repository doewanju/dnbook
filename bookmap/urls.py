from django.urls import path
from . import views

urlpatterns = [
    path('bookstore/', views.bookstore, name='bookstore'),
    path('realmap/', views.realmap, name='realmap'),
    path('store/<int:bookstore_id>', views.detail, name='storedetail'),    
    path('scrap/<int:bookstore_id>', views.scrap, name='scrap'),
    path('reviewcreate/<int:bookstore_id>', views.reviewcreate, name='reviewcreate'),
    path('reviewdelete/<int:review_id>', views.reviewdelete, name='reviewdelete'),
    path('crawling/<int:bookstore_id>', views.crawling, name='crawling'),
]