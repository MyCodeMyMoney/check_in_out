# -*- coding: utf-8 -*
import time
import datetime
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from apscheduler.schedulers.blocking import BlockingScheduler

#用户名、密码
py="python"
username = "majunchao"
password = "654321"

url = 'http://192.168.1.100:8890/seeyon/main.do'


# 创建一个logger 
logger = logging.getLogger('mytest')  
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件 
fh = logging.FileHandler('/home/mjc/my-sh/my-log/sign_in.log')
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 给logger添加handler 
logger.addHandler(fh)

def open_web(url,browser):
    browser.get(url)
    logger.debug('open OA')
    browser.maximize_window()  #将浏览器最大化显示S
    logger.debug('max window')

def Login_account(browser,username,password):
    user_elem = browser.find_element_by_id('login_username')
    user_elem.clear()
    user_elem.send_keys(username)
    logger.debug('input username')

    password_elem = browser.find_element_by_id("login_password") 
    password_elem.clear()
    password_elem.send_keys(password)
    logger.debug('input password')


    browser.find_element_by_id("login_button").click()
    logger.debug('login OA')

def find_check_email_and_open(browser):
    browser.find_element_by_id("message").click()
    logger.debug('click message bar')

    browser.find_element_by_xpath("/html/body/div[14]/div[2]/div[4]/div[3]").click()
    logger.debug('view all message')

    time.sleep(3)
    browser.switch_to.frame("main")
    logger.debug('switch iframe to main')
    
    browser.find_element_by_xpath('//*[@id="allType"]/div').click()
    logger.debug('view all email')

    time.sleep(2)
    line_list = browser.find_elements_by_xpath('//*[contains(@title,"请点击进行签到")]')
    logger.debug('find check email')
    line_list[0].click()
    logger.debug('open check email')

def check_in(browser):
    browser.switch_to_default_content() 
    logger.debug('iframe switch to home page')

    browser.switch_to.frame("layui-layer-iframe1")
    logger.debug('switch iframe to layui-layer-iframe1')
    
    browser.switch_to.frame(0)
    logger.debug('switch iframe to iframe index 0')

    browser.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div').click()
    logger.debug('click check in')

def check_out(browser):
    browser.switch_to_default_content() 
    logger.debug('iframe switch to home page')

    browser.switch_to.frame("layui-layer-iframe1")
    logger.debug('switch iframe to layui-layer-iframe1')
    
    browser.switch_to.frame(0)
    logger.debug('switch iframe to iframe index 0')    
    browser.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div').click()
    logger.debug('click sign out')

def work():
    try:

        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(chrome_options=chrome_options) #声明浏览器对象

        open_web(url,browser)
        time.sleep(2)

        Login_account(browser,username,password)
        time.sleep(20)


        find_check_email_and_open(browser)
        time.sleep(2)

        # dt = datetime.datetime.now()
        # time.sleep(3)  
        check_in(browser)
        time.sleep(3)

        #退出浏览器
        browser.quit()

        logger.debug('quit chrome')
        logger.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+": Clock Success!")

    except Exception as e:
        logger.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+": Clock Filed!")
        logger.exception(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ":\r\n"+ str(e))
if __name__ == '__main__':
    work()

