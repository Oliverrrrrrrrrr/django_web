import re
import PyPDF2

#写入标准库
def input_standard(name_list,start_list=[1,1,1],end_list=[1000,1000,1000]):# name_list：标准库列表 start_list:开始提取的页数列表 end_list:结束提取的页数列表
    if(len(name_list)==len(start_list) and len(end_list)==len(start_list)):
        standard_str = []
        standard_str_pages = []
        for j in range(len(name_list)):
            pdfFileObj = open(name_list[j]+'.pdf', 'rb') #'上海市水闸维修养护规程.pdf'
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            standard = ''''''
            standard_pages = ''''''
            for i in range(start_list[j] - 1, min(end_list[j],len(pdfReader.pages))):
                pageObj = pdfReader.pages[i]
                standard_pages += '啊啊啊啊啊'+str(i+1)+'哈哈哈'
                standard_pages += pageObj.extract_text()
                standard += pageObj.extract_text()
            pdfFileObj.close()
            standard_str.append(standard)
            standard_str_pages.append(standard_pages)
        return standard_str,standard_str_pages
    else:
        print("输入出错")

#写入查重文件
def input_chachong(name_list,start_list=[1,1,1],end_list=[1000,1000,1000]):# name_list：文件名列表 start_list:开始提取的页数列表 end_list:结束提取的页数列表
    if(len(name_list)==len(start_list) and len(end_list)==len(start_list)):
        list_str = []
        list_str_pages = []
        for j in range(len(name_list)):
            pdfFileObj = open(name_list[j]+'.pdf', 'rb') #'上海市水闸维修养护规程.pdf'
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            standard = ''''''
            standard_pages = ''''''
            for i in range(start_list[j] - 1, min(end_list[j],len(pdfReader.pages))):
                pageObj = pdfReader.pages[i]
                standard_pages += '啊啊啊啊啊'+str(i+1)+'哈哈哈'
                standard_pages += pageObj.extract_text()
                standard += pageObj.extract_text()
            pdfFileObj.close()
            list_str.append(standard)
            list_str_pages.append(standard_pages)
        return list_str,list_str_pages
    else:
        print("输入出错")

# 文本预处理,去掉序号、标点、换行、空格
def pre_processing(string):
    pre_list =string.split('\n')
    pre_str = ""
    for i in pre_list:
        i = i.strip()
        pre_i = i.replace(' ','')
        if(i):
            if(i[0].isdigit()):
                while(i):
                    if '\u4e00' <= i[0] <= '\u9fff':
                        pre_str+=i
                        break
                    else:
                        i = i[1:]
            else:pre_str+=i
    pre_standard = pre_str.replace(' ','')
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    pre_standard = cop.sub('',pre_standard)
    return pre_standard

# 两个字符串的比较

# 将较短的字符串切割，长度为t
def cut_shorter(short_str,t): 
    list_t = []
    for i in range(0,len(short_str)-t+1):
        list_t.append(short_str[i:i+t])
    return(list_t)

# 将切割后的词与第二个字符串匹配
def match(list_t,long_str):
    text = []
    location = []
    for element in list_t:
        res = re.finditer(element, long_str)
        for m in res:
            location.append(m.span())
    if(location == []):
        return (0,0)
    location_all = merge(location)
    for i in location_all:
        text.append(long_str[i[0]:i[1]])
    return (text,location_all)

#合并位置信息
def merge(location):
    location_all = []
    while(location!=[]):
        loc = []
        a = location[0]
        start = a[0]
        end = a[1]
        for i in location:
            if(i[0]<=end and i[1]>=end):
                end = i[1]
                loc.append(i)
        location_all.append((start,end))
        for element in loc:
            location.remove(element)
    return location_all

#处理匹配结果，保留同一位置最长的匹配字符串
def operater(str1,str2,start_number):
    str1 = str1.encode('utf8').decode('utf8')
    str2 = str2.encode('utf8').decode('utf8')
    if (len(str1)<len(str2)):
        short_str = str1
        long_str = str2
    else:
        short_str = str2
        long_str = str1
    list_t = cut_shorter(short_str,start_number)
    is_match = match(list_t,long_str)
    if(is_match[0]):
        return is_match[0],is_match[1]
    return 0,0

#处理多个字符串
def input_str(list_str,list_str_pages,standard_str,standard_str_pages,start_number,standard_number):
    for element1 in range(0,len(list_str)-1):
        for element2 in range(element1+1,len(list_str)):
            str1 = list_str[element1]
            str2 = list_str[element2]
            pages1 = list_str_pages[element1]
            pages2 = list_str_pages[element2]
            is_match,location = operater(str1,str2,start_number)
            if(is_match):
                pp1 = pages(pages1,is_match)
                pp2 = pages(pages2,is_match)
                print(element1+1,'和',element2+1,'\033[1;31m有可能有重复,请与标准库对比\033[0m')
                print('重复页数为：',element1+1,'的页数为',pp1,'     ',element2+1,'的页数为',pp2)
                print('重复内容为：',is_match)
                contrast(is_match,standard_str,standard_str_pages,standard_number)
                print('\n')
            else:
                print(element1+1,'和',element2+1,'没有重复')
                print('\n')

                #计算页数
def pages(pages,is_match):
    res = match(['啊啊啊啊啊'], pages)
    loc = res[1]
    loc.append((len(pages),len(pages)))
    for element in is_match:
        p1 = []
        pp1 = []
        ppp1= []
        text_start = match([element[0:10]], pages)
        text_end = match([element[len(is_match)-6:]], pages)
        start = text_start[1]
        end = text_end[1]
        start = start[0]
        start = start[0]
        end = end[0]
        end = end[1]
        for j in range(0,len(loc)-1):
            t = loc[j]
            tt = loc[j+1]
            if((t[0]>=start and t[1]<=end) or (t[1]<=start and tt[0]>=start) or (t[1]<=end and tt[0]>=end)):
                s = ''
                a = t[1]
                while(pages[a].isdigit()):
                    s += pages[a]
                    a = a+1
                else:
                    p1.append(int(s))
                    continue
                
        for elements in p1:
            if(elements-1 not in p1):
                start_s = elements
            if(elements+1 not in p1):
                end_s = elements
                pp1.append((start_s,end_s))
        ppp1.extend(pp1)
    return ppp1

# 与标准库对比，删除与标准库中相同的元素
def contrast(is_match,standard_str,standard_str_pages,standard_number):
    text_num = []
    delete_all = []
    pp1 = []
    length = 0
    for i in range(0,len(standard_str)):
        for j in range(0,len(is_match)):
            text_delete,location_delete = operater(is_match[j],standard_str[i],standard_number)
            if(text_delete):
                text_num.append(i)
                delete_all.append(text_delete)
                p1 = pages(standard_str_pages[i],text_delete)
                pp1.append(p1)
                for element in text_delete:
                    is_match[j] = is_match[j].replace(element,'')
                
    if(text_num!=[]):
        print('\033[1;31m与标准库对比后:\033[0m')
        for t in range(0,len(text_num)):
            print('存在内容与标准库',text_num[t]+1,'重复，重复内容所在标准库的页数为：',pp1[t])
            print('内容为',delete_all[t])
            print('\n')
        for s in is_match:
            length += len(s)
        print('删除标准库中内容后，剩余内容共',length,'字,剩余内容为')
        print(is_match)
    else:
        print('\033[1;31m与标准库对比后，无合法重复内容\033[0m')


def wrap(start_number,standard_number,standard_name,standard_start,standard_end,name_list,start_list,end_list):
    #写入文件
    list_string,list_string_pages = input_chachong(name_list,start_list,end_list)
    standard_string,standard_string_pages = input_standard(standard_name,standard_start,standard_end)
    list_str = []
    list_str_pages = []
    standard_str = []
    standard_str_pages = []
    for i in list_string:
        pre_str = pre_processing(i)
        list_str.append(pre_str)
    for j in list_string_pages:
        pre_str = pre_processing(j)
        list_str_pages.append(pre_str)
    for t in standard_string:
        pre_str = pre_processing(t)
        standard_str.append(pre_str)
    for s in standard_string_pages:
        pre_str = pre_processing(s)
        standard_str_pages.append(pre_str)
    input_str(list_str,list_str_pages,standard_str,standard_str_pages,start_number,standard_number)

def main():
    start_number = 300 # 匹配字符串的长度下线
    standard_number = 50 # 标准库中有的字符串最低长度
    standard_name =  [ '招标文件-2018年度海塘里程桩、单位分界桩设置(陆域及横沙)（定稿）2018-4-19'] # 标准库文件名称
    standard_start = [1] # 标准库起始页
    standard_end = [49]  # 标准库终止页
    name_list=[ '上海城欣测绘有限公司技术部分', '上海浦海测绘有限公司技术部分', '上海祥阳水利勘测设计有限公司技术部分'] # 查重文件名称
    start_list=[1,1,1] # 查重文件起始页
    end_list=[29,48,27] # 查重文件终止页
    wrap(start_number,standard_number,standard_name,standard_start,standard_end,name_list,start_list,end_list)
    
if __name__ == '__main__':
    main()



