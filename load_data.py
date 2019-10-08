'''
서울책보고 크롤링 -> BookStore 모델에 저장
'''
from bs4 import BeautifulSoup
import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","DNbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

def parse_addr():
    result=[]
    addr=[]
    name=[]
    phone=[]
    hp=[]
    url="http://www.seoulbookbogo.kr/front/index.php?g_page=guide&m_page=guide02_02"
    page=requests.get(url)
    html=page.text
    soup=BeautifulSoup(html,'html.parser')
    mb30=soup.find_all('div','mb30')

    for i in mb30:
        li=i.find_all('li')
        strong=i.find_all('strong')
        h3=i.find_all('h3')
        span=i.find_all('span')
        
        for j in range(len(strong)):
            tmp=strong[j].get_text()
            addr.append(tmp.replace('\t',''))
            name.append(h3[j].get_text())
            phone.append(span[j].get_text())

        for j in li:
            if (j.find('a','weblink')):
                tmp=j.find('a','weblink')
                hp.append(tmp.get('href'))
            else:
                hp.append('홈페이지없음')
    result.append(name)
    result.append(addr)
    result.append(phone)
    result.append(hp)
    return result

if __name__=='__main__':
    temp=parse_addr()
    for a in range(len(temp[0])):
        BookStore.objects.create(
        name=temp[0][a],
        addr=temp[1][a],
        phone_number=temp[2][a],
        site=temp[3][a],)