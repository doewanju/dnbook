import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","DNbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

bookstores = BookStore.objects.all()
if __name__=='__main__':
    for a in bookstores:
        if a.openhour:
            temp = a.openhour.split(" : ")
            if temp[0] == "영업시간":
                a.openhour_tf = True
            elif temp[0] == "휴무일":
                a.openhour_tf = False
            a.openhour = temp[1]
            a.save()
        else:
            pass