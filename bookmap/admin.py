from django.contrib import admin
from .models import BookStore, Scrap, Review, Stamp
# Register your models here.

admin.site.register(BookStore)
admin.site.register(Scrap)
admin.site.register(Review)
admin.site.register(Stamp)