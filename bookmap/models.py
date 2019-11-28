from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from main.models import *

# Create your models here.

class BookStore(models.Model):
    bookstore_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default="storename", null=True)
    addr = models.TextField(unique=True)
    phone_regex = RegexValidator(regex=r'^\d{2,3}\-\d{3,4}\-\d{4}$', message="000-0000-0000과 같은 형식으로 입력해주세요.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=13, null=True)
    site = models.URLField(null=True, blank=True)
    img = models.ImageField('외관사진 등록',upload_to='store/', null=True, blank=True)
    insta = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    openhour = models.TextField(null=True, blank=True)
    boss = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, through='Scrap', related_name='%(app_label)s_%(class)s_related')
    saup_regex = RegexValidator(regex=r'^\d{3}\-\d{2}\-\d{5}$', message="000-00-00000 형식에 맞게 입력해주세요.")
    saup = models.CharField(null=True, blank=True, validators=[saup_regex], max_length=12)
    #나중에 가게들 사업자번호 다 등록하면 널이랑 블랭크 지우기
    tag_set = models.ManyToManyField('Tag', blank=True)

    class Meta:
            ordering = ['name']

    def __str__(self):
        return self.name

    def like_count(self):
        return Scrap.objects.filter(store=self).count()

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('storedetail', args=[str(self.pk)])
    
class Crawling(models.Model):
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    link = models.URLField()
    
    def __str__(self):
        return '%s, %s' %(self.store, self.title)

class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to='thema/', null=True, blank=True)

    def __str__(self):
        return self.title

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' %(self.user,self.store)

class Review(models.Model):
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    content = models.CharField(max_length=200)
    star = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s, %s' %(self.store, self.content[:30])

    
class Stamp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return '%s, %s' %(self.user,self.store)