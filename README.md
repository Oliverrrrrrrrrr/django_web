# README

# django_web

投标软件Django框架

## 1. Fork本项目到本地仓库

## 2.链接数据库

- 安装后在菜单栏中找到 MySQL Workbench并打开  
- 登录本地数据库，需要自己设置登陆密码
- 在数据库内create schema，名称为django
- 在终端执行命令pip install mysqlclient
- 在setting.py中的database下面把密码改为本地数据库密码
- 在终端执行python manage.py makemigrations与python manage.py migrate，数据库里就会创建models里的表

## 3.运行项目

- 在终端执行python [manage.py](http://manage.py) runserver,点击终端出现的网址即可

## 4.接入函数

- 在python_function文件夹下已有Qualification和Repeatability两个文件夹，对应资质检测和重复度对比的函数，爬虫放入Qualification下，其他网页对应函数库以同样命名方式在python_function下自建，命名需规范，勿用中文拼音
- 导入函数后，需要在views.py和models.py内新增代码
    - views.py
        - 在网页对应的函数下面接入函数接口
    - models.py
        - 创造新的class
- 修改完这两个文件后需要重新执行makemigration和migrate命令，将新建表移入在数据库中