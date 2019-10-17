'''
카카오맵 검색후 영업시간, 전화번호, 홈페이지 업데이트
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","DNbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSessionIdException
from webdrivermanager import ChromeDriverManager as ch
import re

i=0
bookstores = BookStore.objects.all()
find_addr = []
find_name = []
find_full = []
for a in bookstores:
    find_addr.append(a.addr)
    find_name.append(a.name)

for a,b in zip(find_name, find_addr):
        if '(' in a:
            a=a.split('(')[0]
        c=b.split(re.findall('[0-9]',b)[0])
        c2=c[0].rstrip()
        if c2[-1]!='길' and c2[-1]!='로':
            c2=c[0].split(" ")[0]
        f=a+" "+c2
        find_full.append(f)

def loading():
    res_hour=[]
    res_hp=[]
    res_phone=[]
    res_addr=[]
    result=[]
    global i
    url="https://map.kakao.com"

    path=ch().get_download_path()+'\chromedriver_'+ch().os_name
    if ch().os_name == 'win':
        path+='32\chromedriver.exe'
    else:
        path+='64\chromedriver'
    
    chromeOptions = webdriver.ChromeOptions()
    prefs={'profile.managed_default_content_settings.images':2, 'disk-cache-size':4096}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--disable-extensions")
    #chromeOptions.add_argument('--headless')
    driver=webdriver.Chrome(path,chrome_options=chromeOptions)
    driver.implicitly_wait(3)
    driver.get(url)
    while True:
        if i==len(find_full):
            driver.quit()
            break
        try:
            driver.find_element_by_class_name('tf_keyword').clear()
            driver.find_element_by_class_name('tf_keyword').send_keys(find_full[i])
            try:
                driver.find_element_by_class_name('ico_search').click()
            except ElementClickInterceptedException:
                driver.find_element_by_class_name('DimmedLayer').click()
                driver.find_element_by_class_name('ico_search').click()
            driver.implicitly_wait(3)
            try:
                time.sleep(3)
                driver.find_element_by_class_name('moreview').click()
                driver.implicitly_wait(3)
            except StaleElementReferenceException:
                driver.refresh()
                continue
            except NoSuchElementException:
                res_hour.append('')
                res_phone.append('')
                res_hp.append('')
                res_addr.append('')
                i+=1
                continue
            driver.switch_to.window(driver.window_handles[-1])
            try:
                addr=driver.find_element_by_class_name('txt_address').text
                res_addr.append(addr)
            except NoSuchElementException:
                res_addr.append('없음')
            try:
                hour1=driver.find_element_by_class_name('fst').text
                h=hour1.split(" ")[0]+" : "
                hour2=driver.find_element_by_class_name('txt_operation').text
                res_hour.append(h+hour2)
            except NoSuchElementException:
                res_hour.append('')
            try:
                phone=driver.find_element_by_class_name('txt_contact').text
                res_phone.append(phone)
            except NoSuchElementException:
                res_phone.append('')
            try:
                hp=driver.find_element_by_class_name('link_homepage').text
                res_hp.append(hp)
            except NoSuchElementException:
                res_hp.append('')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            i+=1
        except InvalidSessionIdException:
            driver.quit()
            break
    result.append(res_hour)
    result.append(res_phone)
    result.append(res_hp)
    result.append(res_addr)
    return result

def load_main():
    #i+1값이 bookstore_id
    global i
    result=[]
    result2=[]
    while True:
        result = loading()
        if i==len(find_full):
            break
    res_hour=result[0]
    res_phone=result[1]
    res_hp=result[2]
    res_addr=result[3]

    for a,elem in enumerate(res_addr):
        if elem=='없음':
            del res_hour[a]
            del res_phone[a]
            del res_hp[a]
            del res_addr[a]
    
    result2.append(res_hour)
    result2.append(res_phone)
    result2.append(res_hp)
    return result2

if __name__=='__main__':
    temp=load_main()
    for j in range(len(temp[0])):
        b=BookStore.objects.get(bookstore_id=j+1)
        if temp[0][j] != '':
            b.openhour=temp[0][j]
        if temp[1][j] != '':
            b.phone_number=temp[1][j]
        if temp[2][j] != '':
            b.site=temp[2][j]
        b.save()       