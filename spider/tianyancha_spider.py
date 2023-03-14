# %%
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from APP.models import Main_person, Project

# 封装函数
def get_data(phone, password,companyname):
    # 输入账号密码以及公司名称
    phone = phone
    password = password
    companyname = companyname
    url = 'https://www.tianyancha.com/login?from=http%3A%2F%2Fwww.tianyancha.com%2Fusercenter%2FmodifyInfo'

    # 打开页面
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    # 点击账号密码跳转到输入账号密码页面
    time.sleep(2)
    driver.execute_script("loginObj.toggleQrcodeAndPwd();")
    # 跳转到输入账号密码登录页面
    time.sleep(2)
    driver.execute_script("loginObj.changeCurrent(1);")
    # 输入账号
    time.sleep(2)
    inputuid = driver.find_element(By.XPATH, '//*[@id="mobile"]')
    inputuid.send_keys(phone)

    # 输入密码
    time.sleep(2)
    inputpassword = driver.find_element(By.XPATH, '//*[@id="password"]')
    inputpassword.send_keys(password)

    # 同意书
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="agreement-checkbox-account"]').click()

    # 点击登录
    time.sleep(2)
    driver.execute_script("loginObj.loginByPhone(event);")  # 由于获取不到登录按钮，于是直接执行登录按钮对应的js代码

    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-company-search"]')))
    # 开始爬取信息
    input = driver.find_element(By.ID, 'header-company-search')
    input.clear()
    input.send_keys(companyname)
    driver.find_element(By.XPATH, '//*[@class="input-group-btn btn -sm btn-primary component"]').click()
    driver.find_element(By.XPATH,
                        '//div[@class="index_list-wrap___axcs"]/div[1]//a[@class="index_alink__zcia5 link-click"]').click()
    driver.switch_to.window(driver.window_handles[-1])
    #%%
    # 透视图下载
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div[3]/span')))
    # driver.find_element(By.XPATH,
    #                     '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div[3]/span').click()

    # 主要人员
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[5]/div')))
    main_person = \
    driver.find_elements(By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[5]/div')[0].text
    main_person = re.sub(r'\n最终受益人', '', main_person)
    print(main_person)
    pattern = r'\d+\s*\S+\s*(\S+)\s*.*?\s*(\S+)\s*-\s*-'
    main_person_match = re.findall(pattern, main_person)
    columns = ['主要人员', '职位']
    df = pd.DataFrame(main_person_match, columns=columns)
    # df.to_excel('股东信息.xlsx', index=False)
    # 保存到数据库
    for i in range(len(df)):
        person = Main_person()
        person.company_name = df['主要人员'][i]
        person.position = df['职位'][i]


    # %%
    # 股东信息
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[6]/div')))
    stocker = driver.find_elements(By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[6]/div')[
        0].text
    pattern = r'(?P<name>\S+)\s*.*?\s*.*?\s*(?P<percent1>\d+.\d+%)\s*(?P<percent2>\d+.\d+%)\s*[\S\s]*?(?P<num>\d+\.\d+万元)\s*(?P<data>\d{4}-\d{2}-\d{2})'
    print(stocker)
    matches = re.findall(pattern, stocker)
    columns = ['股东（发起人）', '持股比例', '最终受益股份', '认缴出资额', '认缴出资日期']
    df = pd.DataFrame(matches, columns=columns)
    # df.to_excel('股东信息.xlsx', index=False)

    # %%
    # 建筑资质
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div')))
    text = driver.find_elements(By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div')[
        0].text
    text = re.sub(r'\n', ' ', text)
    pattern = r'b资质资格\b|\b注册人员\b|\b工程项目\b'
    text = re.split(pattern, text)
    print(text[0])
    pattern = r'\s*(\d{4}-\d{2}-\d{2})\s*(\d{4}-\d{2}-\d{2})\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)'
    matches = re.findall(pattern, text[0])
    print(matches)
    columns = ['发证日期', '证书有效期', '资质类别', '资质证书号', '资质名称', '资质名称', '资质名称', '资质名称',
               '发证机关']
    df = pd.DataFrame(matches, columns=columns)
    # df.to_excel('资质.xlsx', index=False)

    # %%
    # 注册人员
    print(text[1])
    text[1] = re.sub(r'序号', ' ', text[1])
    pattern = r'\s*\d\s*\S+\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)'
    matches = re.findall(pattern, text[1])
    columns = matches[0]
    df = pd.DataFrame(matches[1:], columns=columns)
    # df.to_excel('注册人员.xlsx', index=False)

    # %%
    # 工程项目
    # 第一页
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]')))
    project = driver.find_elements(By.XPATH,
                                   '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]')[
        0].text
    project = re.sub(r'\n', ' ', project)
    project = re.sub(r'全部项目 序号', '', project)
    project = re.sub(r'\s*\d+(\s+\d+)*$', '', project)
    project = re.sub(r'详情', '', project)
    project_all = project

    # %%
    # 工程项目分页
    page_div = driver.find_element(By.XPATH,
                                   '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]/div[2]/div/div/div/div')
    total_page = len(page_div.find_elements(By.CLASS_NAME, 'num')) - 1

    for i in range(2, total_page + 1):
        # 点击第二页
        if i == 2:
            driver.find_element(By.XPATH,
                                '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]/div[2]/div/div/div/div/div[2]').click()
        # 点击第三页及之后页面
        else:
            driver.find_element(By.XPATH,
                                '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]/div[2]/div/div/div/div/div[' + str(
                                    i + 1) + ']').click()
        # 获取当前页面的工程项目信息
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]')))
        project = driver.find_elements(By.XPATH,
                                       '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[16]/div/div[2]/div[3]')[
            0].text
        # 整理数据
        project = re.sub(r'\n', ' ', project)
        project = re.sub(r'工程项目 28 全部项目 序号 项目编号 项目名称 项目属地 项目类别 建设单位 操作 ', '', project)
        project = re.sub(r'\s*\d+(\s+\d+)*$', '', project)
        project = re.sub(r'详情', '', project)
        # 将每页的工程项目信息合并
        project_all = project_all + project

    # %%
    pattern = r'\s*\d+\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)'
    matches = re.findall(pattern, project_all)
    columns = matches[0]
    df = pd.DataFrame(matches[1:], columns=columns)
    # df.to_excel('工程项目.xlsx', index=False)
    #将工程项目信息存入数据库
    for i in range(len(df)):
        Project = Project()
        Project.ProjectNumber = df['项目编号'][i]
        Project.ProjectName = df['项目名称'][i]
        Project.ProjectLocation = df['项目属地'][i]
        Project.ProjectType = df['项目类别'][i]
        Project.ConstructionUnit = df['建设单位'][i]
        Project.save()
