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


def bianli_pics(pdfFile, path):
    project_name = pdfFile.split('/')[-1].split('.')[0]  # 项目名称
    seal_pages = []
    img_folder = path
    img_list = [os.path.join(nm) for nm in os.listdir(img_folder) if nm[-3:] in ['jpg', 'png', 'gif']]
    # print(img_list) #将所有图像遍历并存入一个列表
    for n in range(len(img_list)):
        i = img_list[n]

        image = path + i  # "pdf_picture/"+i
        # image_out = "Seal Picture/" + i + "_signiture.png"
        flag = 1 - check_seal_exist(image)
        if flag:  # 到数据库中删除原图像
            # delete_original_image(image, image_out)
            # print("第",i,"页",flag)
            file_name = image
            if os.path.exists(file_name):
                os.remove(file_name)
                print('成功删除文件:', file_name)
            else:
                print('未找到此文件:', file_name)
        else:
            # print("第",i,"页",flag)
            # 删除i中的".png"字符串
            i = i.replace(".png", "")
            print("第", i, "页存在印章")
            seal_pages.append(i)

    seal = Seal()
    while os.listdir("static/img/Seal Picture"):
        seal.seal_page = seal_pages  ## 印章页码

    seal.file_title = project_name  ## 项目名称
    seal.save()


##判别图片中是否存在红色印章
def check_seal_exist(image):
    img = cv2.imread(image)
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
        return seal_result

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


if __name__ == '__main__':
    image = 'pdf_picture/26.png'
    seal_result = check_seal_exist(image)
    print(seal_result)
    image_out = 'signiture.png'
    pick_seal_image(image, image_out)
