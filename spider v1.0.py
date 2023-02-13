
from urllib.request import unquote
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

try:
    #chrome driver settings
    chrome_options = webdriver.ChromeOptions()
    #是否无头
    chrome_options.add_argument("--headless")
    #location
    driver_location_mac='/usr/local/bin/chromedriver'
    service = Service(driver_location_mac)

    # driver_location_win=r'C:\Program Files\Google\Chrome\Application\chromedriver'
    # service = Service(driver_location_win)
except:
    print('setting chorme driver failed')
    
    
def search_pages(word):
    driver = Chrome(service=service,options=chrome_options)
    #url:百度新闻
    url = "https://news.baidu.com/"
    driver.get(url)
    driver.find_element(by=By.ID,value="ww").send_keys(word)
    sleep(3)
    driver.find_element(by=By.ID,value="s_btn_wr").click()
    sleep(3)
    #recent 10 news
    urls=[]
    for i in range(1,11):
        xpath='//*[@id="'+str(i)+'"]/div/h3/a'
        try:
            url_tmp=driver.find_element(by=By.XPATH,value=xpath).get_attribute('href')
            urls.append(url_tmp)
        except:
            print ('found all')
    driver.close()
    get_news(urls,word)

def get_news(urls,word):
    if len(urls) == 0:
        return
    else:
        try:
            os.makedirs('result/'+word)
        except:
            pass
        for url in urls:
            # print (url)
            driver = Chrome(service=service,options=chrome_options)
            driver.get(url)
            sleep(1)
            tex=driver.find_element(by=By.XPATH,value='/html/body').text
            title=driver.title
            with open('result/'+word+'/'+title[:10]+'.txt','w') as f:
                f.write(tex)
            driver.close()

def get_words():
    with open ('words.txt','r',encoding='utf-8-sig') as f:
        word=f.read()
        words=word.split('\n')
        try:
            os.mkdir('result')
        except:
            pass
        for word in words:
            search_pages(word)
            print (word+'done!')
            print ('*'*40)


get_words()


