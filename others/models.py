from django.db import models
from bookmap.models import BookStore
from django.contrib.auth.models import User

#제목, 사진, 기간, 작성날짜, 내용
# Create your models here.
class Culture(models.Model):
    title = models.CharField('제목',max_length=200)
    picture = models.ImageField('이미지 등록',upload_to='Culture/', null=True)
    start_time = models.DateField('시작 날짜')
    finish_time = models.DateField('종료 날짜')
    write_date = models.DateTimeField('작성한 날짜',auto_now=True)
    content = models.TextField('내용')
    ETC = 'ET'
    CONCERT = 'CO'
    ONEDAY = 'ON'
    CLUB = 'CL'
    MOVIE = 'MO'
    GROUP = [
        ('ET', '기타'),
        ('CO', '북콘서트'),
        ('ON', '원데이클래스'),
        ('CL', '소모임'),
        ('MO', '영화상영'),
    ]
    group = models.CharField(
        max_length = 7,
        choices = GROUP,
        default = ETC,
    )
    store = models.ForeignKey(BookStore, null=True, on_delete=models.CASCADE)

class Comment(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' %(self.culture, self.content[:30])
