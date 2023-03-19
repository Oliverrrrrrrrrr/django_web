import os

from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def get_wsw_data(phoneW, password, company_name):
    phoneW = phoneW
    password = password
    company_name = company_name

    bro = webdriver.Edge()
    bro.get('https://wenshu.court.gov.cn/')
    bro.maximize_window()
    login_tag = bro.find_element(By.XPATH,'//*[@id="loginLi"]/a')
    time.sleep(2)
    login_tag.click()
    #登录
    bro.switch_to.frame('contentIframe')
    #账号
    username_path = bro.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
    username_path.send_keys(phoneW)
    #密码
    password_path = bro.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
    password_path.send_keys(password)
    login_in = bro.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[3]/span')
    time.sleep(2)


    #username_path.send_keys('18816512265')
    time.sleep(1)
    #password_path.send_keys('zyldxxN520@')
    time.sleep(1)
    login_in.click()
    time.sleep(2)

    #登录成功来到主页
    bro.switch_to.parent_frame()
    search_input = bro.find_element(By.XPATH,'//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input')
    #company_name = input('Enter a company name:')
    search_input.send_keys('行贿'+company_name)
    btn = bro.find_element(By.XPATH,'//*[@id="_view_1540966814000"]/div/div[1]/div[3]')
    time.sleep(2)
    btn.click()
    time.sleep(10)
    #保存图片到path路径
    path = 'D:\智慧评标\文件\django_web\static\img\wenshuwang'
    #截图保存在path中
    wenshuwang_pic = bro.save_screenshot("行贿"+company_name+".png")
    with open(path, 'wb') as f:
        f.write(wenshuwang_pic)
    f.close()

get_wsw_data('18816512265','zyldxxN520@','上海市机械设备成套（集团）有限公司')
    

