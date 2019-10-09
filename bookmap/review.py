from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os;
os.environ["PATH"] += os.pathsep + 'bookmap';
'''
만약 네이버에 등록된 곳이면 그 곳 블로그리뷰 클릭해서 리뷰가져오고
등록안된곳이면 지금 하는거처럼 블로그 상단 세건 가져오도록
만약 등록된곳 가져올수있으면 영업시간도 가져오기
'''

def reviewFuc(name, addr):
    find_name = name
    find_addr = addr
    f=find_name+" "+find_addr.split(" ")[0]

    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)
    driver.implicitly_wait(3)

    naver_url="https://www.naver.com"
    driver.get(naver_url)

    driver.find_element_by_class_name('input_text').clear()
    driver.find_element_by_class_name('input_text').send_keys(f)
    driver.find_element_by_class_name('sch_smit').click()
    driver.find_element_by_class_name('lnb3').click()
    driver.switch_to.window(driver.window_handles[-1])
    url=driver.current_url

    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    li=soup.find_all('li','sh_blog_top')
    res=[]
    for i in range(3):
        title=li[i].find('a','sh_blog_title').get_text()
        content=li[i].find('dd','sh_blog_passage').get_text()
        link=li[i].find('a','sh_blog_title').get('href')
        inf={'title':title, 'content':content, 'link':link}
        res.append(inf)
    return res
