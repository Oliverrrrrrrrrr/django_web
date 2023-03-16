#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np


##判别图片中是否存在红色印章
def ckeck_seal_exit(image):
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
        for j in i :
            if j > 160:
                g_num+=1
    if g_num > 30:
        seal_result = 2
        return seal_result

    for i in b:
        for j in i:
            if j > 170:
                r_num += 1

    if r_num > 30:
        # print("该图片有红章")
        seal_result = 1#"有印章"  ##该图片有红章
    else:
        # print("该图片没有红章")
        seal_result = 0#"无印章"  ##该图片没有红章
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
    seal_result = ckeck_seal_exit(image)
    print(seal_result)
    image_out = 'signiture.png'
    pick_seal_image(image, image_out)
