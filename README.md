# DNBOOK
독립서점, 독립출판물 정보 사이트

## 기술
- Django

## pip
- django
- bs4
- simplejson
- django-bootstrap4
- pillow
- requests
- selenium
- webdrivermanager

## 모델 불러오기
- $python manage.py migrate

## 책방 DB 불러오기
- load_data.py 있는 위치에서 $python load_data.py 입력!
- 실행시 리뷰 크롤링에 필요한 webdriver도 각자의 os에 맞게 가상환경에 설치해줍니다.

## 관리자계정 만들기
- $python manage.py createsuperuser