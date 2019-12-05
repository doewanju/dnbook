from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
from webdrivermanager import ChromeDriverManager as ch
import os

def reviewFuc(name, addr):
    path=ch().get_download_path()+'\chromedriver_'+ch().os_name
    if ch().os_name == 'win':
        path+='32\chromedriver.exe'
    else:
        path+='64\chromedriver'
    if not os.path.exists(path):
        ch().download_and_install()
    chromeOptions = webdriver.ChromeOptions()
    prefs={'profile.managed_default_content_settings.images':2}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(path,chrome_options=chromeOptions)
    driver.implicitly_wait(3)

    naver_url="https://www.naver.com"
    driver.get(naver_url)

    find_name = name
    find_addr = addr
    f=find_name+" "+find_addr.split(" ")[0]
    tf=False
    #driver.find_element_by_class_name('input_text').clear()
    driver.find_element_by_class_name('input_text').send_keys(f)
    driver.find_element_by_class_name('input_text').send_keys(Keys.ENTER)
    try:
        driver.find_element_by_class_name('review').click()
    except NoSuchElementException:
        driver.find_element_by_class_name('lnb3').click()
        tf=True
    driver.switch_to.window(driver.window_handles[-1])
    url=driver.current_url

    res=[]
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    ran=5
    if (tf==True):
        li=soup.find_all('li','sh_blog_top')
        if len(li)<5: ran=len(li)
        for i in range(ran):
            title=li[i].find('a','sh_blog_title').get_text()
            content=li[i].find('dd','sh_blog_passage').get_text()
            link=li[i].find('a','sh_blog_title').get('href')
            inf={'title':title, 'content':content, 'link':link}
            res.append(inf)
    else:
        li=soup.find_all('li','type_review')
        if len(li)<5: ran=len(li)
        for i in range(ran):
            title=li[i].find('a','name').get_text()
            content=li[i].find('div','ellp2').get_text()
            link=li[i].find('a','name').get('href')
            inf={'title':title, 'content':content, 'link':link}
            res.append(inf)

    return res