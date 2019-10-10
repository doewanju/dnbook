from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from webdrivermanager import ChromeDriverManager as ch
from selenium.common.exceptions import NoSuchElementException

def reviewFuc(name, addr):
    find_name = name
    find_addr = addr
    f=find_name+" "+find_addr.split(" ")[0]
    path=ch().get_download_path()+'\chromedriver_'+ch().os_name
    if ch().os_name == 'win':
        path+='32\chromedriver.exe'
    else:
        path+='64\chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(path,chrome_options=options)
    driver.implicitly_wait(3)

    naver_url="https://www.naver.com"
    driver.get(naver_url)

    tf=False
    driver.find_element_by_class_name('input_text').clear()
    driver.find_element_by_class_name('input_text').send_keys(f)
    driver.find_element_by_class_name('sch_smit').click()
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
