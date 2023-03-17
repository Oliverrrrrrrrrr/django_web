
# -*- coding: utf-8 -*-

import fitz
import os

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

if __name__ == '__main__':
    # 1、PDF地址
    # staticc/file/project_file
    pdfFile = r"static/file/project_file/上海联源建设工程有限责任公司技术部分.pdf"
    # 2、需要储存图片的目录
    storePath = r"pdf_picture"
    pdf2image(pdfFile, storePath, zoom=2.0)