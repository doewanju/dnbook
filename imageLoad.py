from io import BytesIO
from urllib.request import urlopen
from django.core.files import File
from PIL import Image

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","DNbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

if __name__ == '__main__':
    imgarray = []
    with open('img.txt',"r",encoding='UTF8') as f:
        while True:
            name = f.readline()
            if not name: break
            #name = name.split("_")[1]
            imgarray.append(name.strip())

    print(imgarray)

    stores = BookStore.objects.all()

    for store in stores:
        #print("책방: "+store.name, end="  ")
        for i in range(len(imgarray)):
            temp = imgarray[i].split('_')[1].split('.')[0]
            if temp == store.name:
                #print("이미지 이름: " + imgarray[i])
                store.img = 'store/'+imgarray[i]
                store.save()