'''
BookStore 모델에 data 비우는 코드
'''
from bs4 import BeautifulSoup
import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","DNbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

if __name__=='__main__':
    BookStore.objects.all().delete()