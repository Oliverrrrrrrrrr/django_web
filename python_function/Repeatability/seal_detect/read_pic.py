
# -*- coding: utf-8 -*-

import cv2
from signiture_detect import ckeck_seal_exit
from signiture_detect import pick_original_image
from signiture_detect import pick_seal_image

## 遍历一个文件夹下的所有图像 
def bianli_pics(path):
	import os
	img_folder = path
	img_list = [os.path.join(nm) for nm in os.listdir(img_folder) if nm[-3:] in ['jpg', 'png', 'gif']]
	#print(img_list) #将所有图像遍历并存入一个列表
	for n in range(len(img_list)):  
		i = img_list[n]
		# path=os.path.join(path,i)
		# image = str(cv2.imread(path)) #逐个读取
		image = path + i#"pdf_picture/"+i
		image_out = "seal_signiture/"+ i + "_signiture.png"
		flag = ckeck_seal_exit(image)
		if flag:
			print("第"+i+"页有印章")
			pick_seal_image(image, image_out)
			# pick_original_image(image, image_out)
		# else :
		# 	print("第"+i+"页无印章")
		#print(i+'\n')
	# print(len(img_list))
	

if __name__=="__main__":
	path="pdf_picture/"
	bianli_pics(path)
