import pdfplumber
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import SparsePCA
from sklearn.pipeline import Pipeline
from pickle import load
import jieba as jb

path = os.getcwd() + '\static\MODEL.pkl'
# print(path)
with open(path, 'rb') as f:
        MODEL = load(f)

#打开MODEL.PKL文件


def extract_text_info(filepath, beg = None, end = None):
    """
    提取PDF中的文字
    @param filepath:文件路径
    @return:
    """
    with pdfplumber.open(filepath) as pdf:
        # 获取第2页数据
        text = ""
        if beg is None:
            beg = 2
        if end is None:
            end = len(pdf.pages)
        for page in pdf.pages[beg:end]:
            text  += page.extract_text()
        if len(text) == 0:
            print(filepath , 'has no text')
        else:
            text = [ j.strip() for j in jb.lcut(text) if j.replace("." , "") not in MODEL['stop_words'] and len(j.replace("." , "").strip()) ]
            text = [" ".join(text)]
    return text 
 
def predict(text):  
    inputs = MODEL['count'].transform(text)
    inputs = MODEL['tf-idf'].transform(inputs).toarray()
    inputs = MODEL['model'].predict_proba(inputs)
    return inputs[: , -1]
# print(predict(extract_text_info(r'上海城欣测绘有限公司技术部分.pdf')))