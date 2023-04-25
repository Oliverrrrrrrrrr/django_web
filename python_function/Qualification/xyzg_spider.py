import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from django.conf import settings
import os
import django
from APP.models import CreditChina


# 封装函数
def get_creditChina(companyname):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
    django.setup()
    op = Options()
    op.add_argument('-headless')
    browser = webdriver.Firefox(options=op)

    M = []
    N = []
    try:
        browser.get('https://www.creditchina.gov.cn/')
        wait = WebDriverWait(browser, 20)
        inputt = wait.until(EC.presence_of_element_located((By.ID, 'search_input')))
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                     'body > div.header > div.header-mid > div > div.header-search > div > input.search_btn')))
        print(inputt)
        print(btn)
        companyname = companyname
        inputt.send_keys(companyname)
        time.sleep(1)
        btn.click()
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[1])
        result = browser.page_source
        # print(result)
        # print(browser.page_source)
        # uuid = 'uuid'
        Cuuid = result.count('uuid')

        if Cuuid == 0:
            print('没有找到相关信息')
        elif Cuuid > 3:
            print('找到了' + str(Cuuid) + '条相关信息')
            print("前三条信息为：")

            soup = BeautifulSoup(result, 'html.parser')
            lis = soup.find_all('li', class_='company-item')
            uuids_list = []
            entityNames_list = []
            entityCodes_list = []

            for li in lis:
                data_message = li['data-message']
                data_dict = eval(data_message)
                uuids = data_dict['uuid']
                entityNames = data_dict['accurate_entity_name']
                entityCodes = data_dict['accurate_entity_code']
                uuids_list.append(uuids)
                entityNames_list.append(entityNames)
                entityCodes_list.append(entityCodes)

            for i in range(0, 6):
                if i == 0 or i == 1 or i == 2:
                    uuid = uuids_list[i]
                    entityName = entityNames_list[i]
                    entityCode = entityCodes_list[i]
                    # print(uuid)
                    print(entityName)
                    M.append(entityName)
                    # print(entityCode)
                    browser.get(
                        'https://www.creditchina.gov.cn/xinyongxinxixiangqing/xyDetail.html?searchState=1&entityType=1&keyword=' + entityName + '&uuid=' + uuid + '&tyshxydm=' + entityCode)
                    wait = WebDriverWait(browser, 20)
                    time.sleep(5)
                    browser.switch_to.window(browser.window_handles[1])
                    result1 = browser.page_source
                    # print(result1)
                    soup = BeautifulSoup(result1, 'html.parser')
                    ems = soup.find_all('em')

                    # 整理数据
                    # 基础信息
                    td_list = soup.find_all('td')
                    for td in td_list:
                        N.append(td.string.strip())
                    # 展示信息
                    ems = soup.find_all('em')
                    for em in ems:
                        M.append(em.get_text())
                        # print(em.get_text())
                    print('------------------')

                    # li_text = soup.find('li', id='permissionBtn').contents[0].strip()
                    # print(li_text)
                    # em_text = soup.find('em', id='permissionNum').text.strip()
                    # print(em_text)
                    # 保存在数据库
                    pattern = r'<em.*?>(\d+)</em>'
                    matches = re.findall(pattern, result1)  # 匹配所有符合条件的字符串，返回一个列表，列表中的每个元素是一个元组
                    M.append(matches)
                columns = ['行政管理', '诚实守信', '严重失信主体名单', '经营异常', '信用承诺', '信用评价', '司法判决',
                           '其他']
                df = pd.DataFrame(matches, columns=columns)
                for i in range(len(df)):
                    info = CreditChina()
                    info.administrative_management = df['行政管理'][i]
                    info.creditworthy = df['诚实守信'][i]
                    info.serious_credit = df['严重失信主体名单'][i]
                    info.business_abnormal = df['经营异常'][i]
                    info.credit_commitment = df['信用承诺'][i]
                    info.credit_evaluation = df['信用评价'][i]
                    info.judicial_judgment = df['司法判决'][i]
                    info.other = df['其他'][i]
                    info.entityName = entityName
                    # 若数据库已有则不保存
                    if not CreditChina.objects.filter(entityName=entityName):
                        info.save()
        # -------------------------------------------
        else:
            print('找到了' + str(Cuuid) + '条相关信息')
            soup = BeautifulSoup(result, 'html.parser')
            lis = soup.find_all('li', class_='company-item')
            uuids_list = []
            entityNames_list = []
            entityCodes_list = []

            for li in lis:
                data_message = li['data-message']
                data_dict = eval(data_message)
                uuids = data_dict['uuid']
                entityNames = data_dict['accurate_entity_name']
                entityCodes = data_dict['accurate_entity_code']
                uuids_list.append(uuids)
                entityNames_list.append(entityNames)
                entityCodes_list.append(entityCodes)

            for i in range(0, Cuuid):
                uuid = uuids_list[i]
                entityName = entityNames_list[i]
                entityCode = entityCodes_list[i]
                # print(uuid)
                print(entityName)
                M.append(entityName)
                # print(entityCode)
                browser.get(
                    'https://www.creditchina.gov.cn/xinyongxinxixiangqing/xyDetail.html?searchState=1&entityType=1&keyword=' + entityName + '&uuid=' + uuid + '&tyshxydm=' + entityCode)
                wait = WebDriverWait(browser, 20)
                time.sleep(5)
                browser.switch_to.window(browser.window_handles[1])
                result1 = browser.page_source
                # print(result1)
                soup = BeautifulSoup(result1, 'html.parser')
                # 整理数据
                # 基础信息
                td_list = soup.find_all('td')
                for td in td_list:
                    N.append(td.string.strip())
                    print(N)
                # 展示信息（行政信息）
                ems = soup.find_all('em')
                for em in ems:
                    M.append(em.get_text())
                    # print(em.get_text())
                # # 保存在数据库
                pattern = r'<em.*?>(\d+)</em>'
                matches = re.findall(pattern, result1, re.S)
                print(matches)
        columns = ['行政管理', '诚实守信', '严重失信主体名单', '经营异常', '信用承诺', '信用评价', '司法判决', '其他']
        df = pd.DataFrame(matches, columns=columns)
        for i in range(len(df)):
            info = CreditChina()
            info.administrative_management = df['行政管理'][i]
            info.creditworthy = df['诚实守信'][i]
            info.serious_credit = df['严重失信主体名单'][i]
            info.business_abnormal = df['经营异常'][i]
            info.credit_commitment = df['信用承诺'][i]
            info.credit_evaluation = df['信用评价'][i]
            info.judicial_judgment = df['司法判决'][i]
            info.other = df['其他'][i]
            info.entityName = entityName
            # 若数据库已有则不保存
            if not CreditChina.objects.filter(entityName=entityName):
                info.save()

    except TimeoutException as e:
        print("Time out")
        print(e.msg)
    finally:
        browser.close()

    print(M)
    return M
