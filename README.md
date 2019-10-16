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
- 실행 시 리뷰 크롤링에 필요한 webdriver도 각자의 os에 맞게 가상환경에 설치해줍니다.
- 이후 $python load_data2.py 입력! (영업시간 입력, 홈페이지와 전화번호 업데이트)
- 실행 시 크롬 브라우저로 자동화 모습이 보이고 약 12분정도 걸립니다....

## 관리자계정 만들기
- $python manage.py createsuperuser