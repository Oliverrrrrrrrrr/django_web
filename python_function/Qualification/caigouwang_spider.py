import requests
from bs4 import BeautifulSoup
from pip._internal import req
import pandas as pd
from APP.models import CGW_inquire


# import pandas as pd
# import lxml
def get_cgw_data(companyName):
    companyName = companyName

    # 首页1
    url = 'http://www.ccgp.gov.cn/cr/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'
    }
    # companyName = input('enter a companyName:')
    data = {
        'orgName': companyName
    }
    response = requests.post(url=url, data=data, headers=headers)
    res_text = response.text
    trShow = 'trShow'
    tSnum = res_text.count(trShow)
    tSnum1 = tSnum - 1  # 实际查到几条结果

    j = 1;
    a = 5
    if tSnum1 > 3:
        print("-----本次共查询到 " + str(tSnum1) + " 条信息-----")
        print("前三条信息为：")
        soup = BeautifulSoup(res_text, 'html.parser')
        # 获取全部 class 为 trShow 的标签，进行遍历
        a_data = soup.find_all('td')
        for i in range(3):
            #print("-----第" + str(i + 1) + "条信息-----")
            if (j < 22 and a < 26):
                #print("企业名称：" + a_data[j].text)
                #print("处罚结果：" + a_data[a].text)
                companyname = a_data[j].text
                punishresult = a_data[a].text
                columns = ['公司名称', '处罚结果']
                df = pd.DataFrame(columns=columns)
                df.loc[i] = [companyname, punishresult]

                obj = CGW_inquire()
                obj.company_name = df['公司名称'][i]
                obj.penalty = df['处罚结果'][i]
                if not CGW_inquire.objects.filter(company_name=companyname):
                    obj.save()

                j = j + 10
                a = a + 10
                i += 1

    elif tSnum1 == 0:
        req.encoding = "utf-8"
        soup = BeautifulSoup(res_text, 'html.parser')
        resu_item = soup.find('div', class_="alert_info")
        dd = resu_item.text.strip()
        dd = dd.replace("	", "")
        print(dd)
        companyname = companyName
        punishresult = '无查询结果'
        obj = CGW_inquire()
        if not CGW_inquire.objects.filter(company_name=companyname):
            obj.save()

    else:
        print("-----本次共查询到 " + str(tSnum1) + " 条信息-----")
        soup = BeautifulSoup(res_text, 'html.parser')
        # 获取全部 class 为 trShow 的标签，进行遍历
        a_data = soup.find_all('td')
        for i in range(0, tSnum1):
            #print("-------第" + str(i + 1) + "条信息-------")
           # print("企业名称：" + a_data[j].text)
            #print("处罚结果：" + a_data[a].text)

            companyname = a_data[j].text
            punishresult = a_data[a].text
            columns = ['公司名称', '处罚结果']
            df = pd.DataFrame(columns=columns)
            df.loc[i] = [companyname, punishresult]
            obj = CGW_inquire()
            obj.company_name = df['公司名称'][i]
            obj.penalty = df['处罚结果'][i]
            if not CGW_inquire.objects.filter(company_name=companyname):
                obj.save()
            j = j + 10; a = a + 10; i += 1

# get_cgw_data('上海市机械设备成套（集团）有限公司')
