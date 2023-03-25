#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np
import fitz
import os
from APP.models import Seal


def pdf2image(pdfFile, storePath, zoom=2.0):
    doc = fitz.open(pdfFile)
    picName = os.path.splitext(os.path.basename(pdfFile))[0]
    index = 0
    os.makedirs(storePath, exist_ok=True)

    images = []
    print(f"To convert: {pdfFile}")
    for pg in range(doc.page_count):
        page = doc[pg]
        index += 1
        rotate = int(0)
        print(f"\tconvert page {index}")

        # 每个尺寸的缩放系数(提高生成分辨率)
        zoom_x, zoom_y = zoom, zoom
        mat = fitz.Matrix(zoom_x, zoom_y)
        pm = page.get_pixmap(matrix=mat, alpha=False)

        imgName = '{}.png'.format(pg)
        imgFile = os.path.join(storePath, imgName)
        pm.save(imgFile)

        images.append(imgFile)

    doc.close()
    return images


def bianli_pics(pdfFile, path, file_name):
    seal_pages = []
    img_folder = path
    img_list = [os.path.join(nm) for nm in os.listdir(img_folder) if nm[-3:] in ['jpg', 'png', 'gif']]
    # print(img_list) #将所有图像遍历并存入一个列表
    for img in img_list:
        img_path = path + "/" + img
        if not os.path.exists(img_path):
            print("图片不存在")
            continue
        if not check_seal_exist(img_path):  # 判断图片中是否存在印章
            os.remove(img_path)
            print('成功删除文件:', img)
        else:
            i = img.replace(".png", "")
            print("第", i, "页存在印章")
            seal_pages.append(i)
            # 保存到数据库
            seal = Seal()
            seal.file_title = file_name  ## 项目名称
            seal.seal_page = i  ## 印章页码
            seal.path = img_path  ## 印章图片路径
            seal.save()


##判别图片中是否存在红色印章
def check_seal_exist(image):
    img = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_blue = np.array([100, 30, 100])
    upper_blue = np.array([150, 255, 255])

    mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(img, img, mask=mask)
    r, g, b = cv2.split(res)
    r_num = 0
    g_num = 0
    for i in g:
        for j in i:
            if j > 160:
                g_num += 1
    if g_num > 30:
        seal_result = 2
    for i in b:
        for j in i:
            if j > 170:
                r_num += 1

    if r_num > 30:
        # print("该图片有红章")
        seal_result = 1  # "有印章"  ##该图片有红章
    else:
        # print("该图片没有红章")
        seal_result = 0  # "无印章"  ##该图片没有红章
    return seal_result


##红章的提取出来生成图片（只能提取出黑白颜色底的红色印章）
def pick_seal_image(image, image_out):
    np.set_printoptions(threshold=np.inf)
    image = cv2.imread(image)

    hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_range = np.array([150, 103, 100])
    high_range = np.array([180, 255, 255])
    th = cv2.inRange(hue_image, low_range, high_range)
    index1 = th == 255

    img = np.zeros(image.shape, np.uint8)
    img[:, :] = (255, 255, 255)
    img[index1] = image[index1]  # (0,0,255)

    cv2.imwrite(image_out, img)


def pick_original_image(image, image_out):
    image = cv2.imread(image)
    cv2.imwrite(image_out, image)
