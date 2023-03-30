from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from python_function.Qualification.caigouwang_spider import get_cgw_data
from python_function.Qualification.tianyancha_spider import tianyancha_spider
from python_function.Repeatability.seal_detect.signiture_detect import bianli_pics, pdf2image
from .models import User, Project, Main_person, Tianyancha_User, UploadProjectFile, UploadTestFile, \
    Shareholder_information, Seal, Qualification_person, Register_person


# index
def index(request):
    return render(request, 'Home.html')


# register
def register(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 注册成功跳转到到登录页面，注册加判断已经存在提示改用用户已存在
        users = User.objects.all()
        for i in users:
            if name == i.name:
                return HttpResponse("用户名已存在")
        if password == password2:
            try:
                User.objects.create(name=name, password=password)
            except Exception as e:
                print(e)
                return HttpResponse("注册失败")
        else:
            return HttpResponse("两次密码不一致")
        return redirect('/login/')


# login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 登录失败时需要提示是用户名不存在还是密码错误
        try:  # 存放可能出现异常的代码 查询数据多个条件时默认是并且的关系
            user = User.objects.get(name=name)
            # 当输入的用户名在数据库里查询不到，说明try里面的代码存在异常
            # 执行万能异常里面的语句
        except Exception as e:  # 捕获异常将异常存到e里
            print(e)
            return HttpResponse("用户名不存在")

        # 如果用户名对，就判断密码有没有输入正确
        if password != user.password:
            return HttpResponse("用户名和密码不匹配")
        return redirect('/')


# logout
def logout(request):
    return redirect('/login/')


# change password
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')
        try:
            user = User.objects.get(name=name)
        except:
            return HttpResponse("用户名不存在")
        if check_password(password, user.password):
            if password2 == password3:
                password2 = make_password(password2)
                user.password = password2
                user.save()
                return redirect('/login/')
            else:
                return HttpResponse("两次密码不一致")
        else:
            return HttpResponse("原密码错误")


# upload file
def import_data(request):
    if request.method == 'GET':
        return render(request, 'import.html')
    elif request.method == 'POST':
        type = request.POST.get('type')
        if type in ['招标文件', '投标文件']:
            project_name = request.POST.get('project name')
            project_file = request.FILES.get('project file')
            if project_file:
                # 查询是否已上传过该文件
                if UploadProjectFile.objects.filter(title=project_file.name):
                    return HttpResponse("该文件已上传")
                # 保存项目信息
                f = UploadProjectFile(type=type, project_name=project_name, title=project_file.name, path=project_file)
                f.save()
                return render(request, 'import.html', {'msg': '上传成功'})
            else:
                return HttpResponse("上传失败")
        else:
            test_file = request.FILES.get('test file')
            if test_file:
                if UploadTestFile.objects.filter(title=test_file.name):
                    return HttpResponse("该文件已上传")
                f = UploadTestFile(type=type, title=test_file.name, path=test_file)
                f.save()
                return render(request, 'import.html', {'msg': '上传成功'})
            else:
                return HttpResponse("上传失败")


def Qualification(request):
    if request.method == 'GET':
        return render(request, 'Qualification.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        companyname = request.POST.get('companyname')

        # 天眼查
        if Tianyancha_User.objects.filter(phone=phone):
            tianyancha_user = Tianyancha_User.objects.get(phone=phone)
        else:
            tianyancha_user = Tianyancha_User.objects.create(phone=phone, password=password)
        # 若数据库中无该公司数据则爬取
        # if not Main_person.objects.filter(company_name=companyname):
        try:
            tianyancha_spider(phone, password, companyname)
        except Exception as e:
            print(e)
            return HttpResponse("天眼查爬取失败")
        # 找到数据库中对应企业的数据
        all_main_person = Main_person.objects.filter(company_name=companyname)
        all_project = Project.objects.filter(company_name=companyname)
        all_shareholder = Shareholder_information.objects.filter(company_name=companyname)
        all_qualification = Qualification_person.objects.filter(company_name=companyname)
        all_register_person = Register_person.objects.filter(company_name=companyname)
        # # 采购网
        # try:
        #     get_cgw_data(companyname)
        # except Exception as e:
        #     print(e)
        #     return HttpResponse("采购网爬取失败")

        return render(request, 'Qualification.html', {
            'all_main_person': all_main_person,
            'all_project': all_project,
            'all_shareholder': all_shareholder,
            'all_qualification': all_qualification,
            'all_register_person': all_register_person
        })


def Repeatability(request):
    # 印章检测函数接口
    if request.method == 'GET':
        return render(request, 'Repeatability.html')
    elif request.method == 'POST':
        filename = request.POST.get('project name')
        # 查看数据库中是否已有检测结果
        if not Seal.objects.filter(file_title=filename):
            # 调取数据库里的pdf
            try:
                file = UploadProjectFile.objects.get(title=filename + ".pdf")
            except:
                return HttpResponse("文件不存在")
            # 未检测过则进行检测
            pdfFile = file.path.path  # 设置pdf路径
            storePath = r"Media/Seal_Picture" + "/" + filename  # 设置存储路径
            try:
                pdf2image(pdfFile, storePath, zoom=2.0)  # pdf转图片
                bianli_pics(pdfFile, storePath, filename)  # 遍历图片并对有印章的图片进行输出页码和提取
            except Exception as e:
                print(e)
                return HttpResponse("检测失败")
        all_seal = Seal.objects.filter(file_title=filename)
        # 将所有页码拼接成字符串
        pages = ""
        for seal in all_seal:
            pages += seal.seal_page + ","
        return render(request, 'Repeatability.html', {'all_seal': all_seal, 'pages': pages})


def Predict(request):
    return render(request, 'Predict.html')
