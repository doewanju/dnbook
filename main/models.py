from django.db import models
from django.contrib.auth.models import User, UserManager
from bookmap.models import BookStore

# Create your models here.

class Normalprofile(models.Model): #일반회원 모델
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10) 
    email = models.EmailField()

    def __str__(self):
        return str(self.user)

class Bossprofile(models.Model): #책방 사장님 모델 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    email = models.EmailField()
    #mystore = models.ForeignKey(BookStore, on_delete=models.CASCADE, null=True)
    introduce = models.TextField(max_length=200)
    # stamp = models

    def __str__(self):
        return str(self.user)


""" 잠시 살려두는 코드
class Bossprofile(models.Model): #책방 사장님 모델
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10) 
    email = models.EmailField()
    # 책방이름은 Bookstore Table에서 가져온다
    # mybookstore = models.CharField(max_length=20)
    introduce = models.TextField(max_length=200)
    # stamp = models.
    def __str__(self):
        return str(self.user)

"""