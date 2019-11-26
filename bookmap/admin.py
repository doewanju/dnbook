from django.contrib import admin
from .models import BookStore, Scrap, Review, Stamp,Tag
# Register your models here.

admin.site.register(BookStore)
admin.site.register(Tag)
admin.site.register(Scrap)
admin.site.register(Review)
admin.site.register(Stamp)