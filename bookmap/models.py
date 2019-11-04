from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from main.models import *

# Create your models here.

class BookStore(models.Model):
    bookstore_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default="storename", null=True)
    addr = models.TextField(unique=True)
    phone_number = models.CharField(blank=True, max_length=15, null=True)
    site = models.URLField(null=True, blank=True)
    img = models.ImageField(upload_to='store/', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    openhour = models.TextField(null=True, blank=True)
    openhour_tf = models.BooleanField(null=True, blank=True) #true면 영업시간 false면 휴무일
    boss = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User,through='Scrap', related_name='%(app_label)s_%(class)s_related')

    def __str__(self):
        return self.name

    def like_count(self):
        return Scrap.objects.filter(store=self).count()

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('storedetail', args=[str(self.pk)])

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