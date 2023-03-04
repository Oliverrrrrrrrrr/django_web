from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password,check_password

#index
def index(request):
    return render(request,'Home.html')

# register
def register(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 判断用户名是否存在
        try:
            user = User.objects.get(name=name)
            return render(request,'signup.html',{'error':'用户名已存在'},locals())
        except:
            pass
        # 判断两次密码是否一致
        if password == password2:
            password = make_password(password)
            user = User(name=name,password=password)
            user.save()
            return redirect('/login/')
        else:
            return render(request,'signup.html',{'error':'两次密码不一致'},locals())

# login
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user = User.objects.get(name=name)
        except:
            return render(request,'login.html',{'error':'用户名或密码错误'},locals())
        if check_password(password,user.password):
            return redirect('/index/')
        else:
            return render(request,'login.html',{'error':'用户名或密码错误'},locals())

# logout
def logout(request):
    return redirect('/login/')

# change password
def change_password(request):
    if request.method == 'GET':
        return render(request,'change_password.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')
        try:
            user = User.objects.get(name=name)
        except:
            return render(request,'change_password.html',{'error':'用户名不存在'},locals())
        if check_password(password,user.password):
            if password2 == password3:
                password2 = make_password(password2)
                user.password = password2
                user.save()
                return redirect('/login/')
            else:
                return render(request,'change_password.html',{'error':'两次密码不一致'},locals())
        else:
            return render(request,'change_password.html',{'error':'密码错误'},locals())




