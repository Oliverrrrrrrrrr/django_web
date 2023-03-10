from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .models import User, Project, Main_person, Tianyancha_User
from spider.tianyancha_spider import get_data

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


def import_data(request):
    return render(request, 'import.html')


def Qualification(request):
    if request.method == 'GET':
        return render(request, 'Qualification.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        companyname = request.POST.get('companyname')
        if Tianyancha_User.objects.filter(phone=phone):
            tianyancha_user = Tianyancha_User.objects.get(phone=phone)
        else:
            tianyancha_user = Tianyancha_User.objects.create(phone=phone, password=password)
        try:
            get_data(phone, password, companyname)
        except Exception as e:
            print(e)
            return HttpResponse("爬取失败")
        return render(request, 'Qualification.html')

def Repeatability(request):
    return render(request, 'Repeatability.html')


def Predict(request):
    return render(request, 'Predict.html')


# def tianyancha_spider(request):
#     phone = request.POST.get('phone')
#     password = request.POST.get('password')
#     companyname = request.POST.get('companyname')
#     tianyancha_user = Tianyancha_User.objects.get(phone=phone)
#     try:
#         spider.get_data(phone, password, companyname)
#     except Exception as e:
#         print(e)
#         return HttpResponse("爬取失败")
#     return render(request, 'Qualification.html')


def project_view(request):
    all_project = Project.objects.all()
    return render(request, 'Qualification.html', {
        'all_project': all_project
    })


def main_person(request):
    all_main_person = Main_person.objects.all()
    return render(request, 'Qualification.html', {
        'all_main_person': all_main_person
    })
